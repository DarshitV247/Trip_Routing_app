from rest_framework.decorators import api_view
from rest_framework.response import Response
from trips.models import (Trip,ELDLog)
from .services.route_service import get_route_info
from .services.hos_service import calculate_trip_schedule
from .services.log_service import generate_logs_from_trip
from django.contrib.auth.models import User
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from django.conf import settings
import io
import os




@api_view(["GET"])
def health_check(request): 
    return Response({"status": "Backend Working"})

@api_view(["POST"])
def calculate_hos(request):

    try:

        distance_miles = float(request.data.get("distance_miles",0))
        cycle_used_hours = float(request.data.get("cycle_used_hours",0))
        result = calculate_trip_schedule(
            distance_miles=distance_miles,
            cycle_used_hours=cycle_used_hours
        )
        return Response(result)

    except Exception as e:
        return Response({"error": str(e)},status=400)

@api_view(["GET"])
def download_pdf(request, filename):

    file_path = os.path.join(
        settings.MEDIA_ROOT,
        "generated_pdfs",
        filename
    )

    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename=filename
    )
    
@api_view(["GET"])
def export_eld_pdf(request, eld_id):

    try:
        eld = ELDLog.objects.get(id=eld_id)
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer,pagesize=letter)
        width, height = letter
        template_path = os.path.join(
            settings.BASE_DIR,
            "assets",
            "blank_logs",
            "fmcsa_log_template.png"
        )
        template = ImageReader(template_path)
        pdf.drawImage(template,0,0,width=width,height=height)
        pdf.setFont("Helvetica",9)
        pdf.drawString(315,690,eld.carrier_name)
        pdf.drawString(55,650,eld.truck_number)
        pdf.drawString(55,430,eld.shipping_document or "")
        pdf.drawString(55,705,str(eld.created_at.month))
        pdf.drawString(95,705,str(eld.created_at.day))
        pdf.drawString(130,705,str(eld.created_at.year))

        day = eld.eld_data["days"][0]
        row_y = {
            "off_duty": 592,
            "sleeper": 576,
            "driving": 560,
            "on_duty": 544
        }
        grid_start = 58
        hour_width = 16.5

        pdf.setLineWidth(2)

        for activity in day["activities"]:
            status = activity["type"]

            if status not in row_y: continue
            y = row_y[status]
            x1 = (grid_start+ activity["start"] * hour_width)
            x2 = (grid_start+ activity["end"] * hour_width)
            pdf.line(x1,y,x2,y)

        pdf.setFont("Helvetica",8)
        pdf.drawString(130,395,
            f"Route: "
            f"{eld.trip.current_location} -> "
            f"{eld.trip.pickup_location} -> "
            f"{eld.trip.dropoff_location}"
        )
        pdf.drawString(130,380,f"Distance: {eld.trip.distance_miles} miles")
        pdf.drawString(130,365,f"Fuel Stops: {eld.trip.fuel_stops}")
        pdf.drawString(130,350,f"Trip Days: {eld.trip.trip_days}")
        pdf.save()
        buffer.seek(0)

        return FileResponse(
            buffer,
            as_attachment=True,
            filename=f"eld_log_{eld.id}.pdf"
        )

    except Exception as e:
        return Response({"error": str(e)},status=400)
    
@api_view(["POST"])
def generate_eld_log(request):

    try:

        trip = Trip.objects.get(id=request.data.get("trip_id"))
        eld = ELDLog.objects.create(
            trip=trip,
            carrier_name=request.data.get("carrier_name"),
            truck_number=request.data.get("truck_number"),
            odometer_start=int(
                request.data.get("odometer_start",0)
            ),
            eld_data=trip.hos_data
        )

        trip_info = {

            "carrier_name":request.data.get("carrier_name"),
            "truck_number":request.data.get("truck_number"),
            "from_location":trip.pickup_location,
            "to_location":
            trip.dropoff_location,

            "remarks":
            f"{trip.pickup_location} to "
            f"{trip.dropoff_location}",

            "odometer":
            int(
                request.data.get(
                    "odometer_start",
                    0
                )
            )
        }

        generated_logs = generate_logs_from_trip(

            distance_miles=
            trip.distance_miles,

            cycle_used_hours=
            trip.cycle_used_hours,

            trip_info=
            trip_info
        )

        return Response({

            "message":
            "ELD Generated",

            "eld_id":
            eld.id,

            "pdf_file":
            generated_logs["pdf_file"],

            "generated_files":
            generated_logs["generated_files"]
        })

    except Exception as e:

        return Response(
            {
                "error": str(e)
            },
            status=400
        )



@api_view(["POST"])
def calculate_trip(request):

    try:

        current_location = request.data.get("current_location")
        pickup_location = request.data.get("pickup_location")
        dropoff_location = request.data.get("dropoff_location")

        cycle_used_hours = float(
            request.data.get("cycle_used_hours", 0)
        )

        route_info = get_route_info(
            current_location,
            pickup_location,
            dropoff_location
        )

        hos_result = calculate_trip_schedule(
            distance_miles=route_info["distance_miles"],
            cycle_used_hours=cycle_used_hours
        )

        rest_stops = []

        for day in hos_result["days"]:
            for activity in day["activities"]:

                if (
                    activity["type"] == "off_duty"
                    and (activity["end"] - activity["start"]) == 0.5
                ):

                    rest_stops.append({
                        "day": day["day"],
                        "start": activity["start"],
                        "end": activity["end"],
                        "duration_minutes": 30
                    })

        dashboard_summary = {
            "trip_days": len(hos_result["days"]),
            "total_distance": route_info["distance_miles"],
            "driving_hours": hos_result["total_driving_hours"],
            "fuel_stops": hos_result["fuel_stops"],
            "rest_stops": len(rest_stops),
        }

        trip_timeline = [
            {
                "type": "current_location",
                "location": current_location
            },
            {
                "type": "pickup",
                "location": pickup_location
            }
        ]

        for i in range(hos_result["fuel_stops"]):

            trip_timeline.append({
                "type": "fuel_stop",
                "number": i + 1,
                "mile_marker": (i + 1) * 1000
            })

        for stop in rest_stops:

            trip_timeline.append({
                "type": "rest_stop",
                "day": stop["day"],
                "start": stop["start"],
                "end": stop["end"],
                "duration_minutes": stop["duration_minutes"]
            })

        trip_timeline.append({
            "type": "dropoff",
            "location": dropoff_location
        })

        route_summary = [
            f"Start from {current_location}",
            f"Travel to pickup location {pickup_location}",
            f"Fuel stops required: {hos_result['fuel_stops']}",
            f"Continue towards {dropoff_location}",
            "Arrive at destination"
        ]

        # Prevent duplicate trips
        trip, created = Trip.objects.get_or_create(

            current_location=current_location,
            pickup_location=pickup_location,
            dropoff_location=dropoff_location,
            cycle_used_hours=cycle_used_hours,

            defaults={
                "distance_miles": route_info["distance_miles"],
                "duration_hours": route_info["duration_hours"],
                "fuel_stops": hos_result["fuel_stops"],
                "rest_stops": len(rest_stops),
                "trip_days": len(hos_result["days"]),
                "trip_status": "Completed",
                "route_data": route_info,
                "hos_data": hos_result,
                "timeline_data": trip_timeline,
            }
        )

        if not created:
            return Response({
                "message": "Trip already exists",
                "trip_id": trip.id,
                "duplicate": True
            })
        map_stops = []
        return Response({

            "trip_id": trip.id,
            "duplicate": False,

            "current_location": current_location,
            "route_info": route_info,
            "hos_result": hos_result,
            "rest_stops": rest_stops,
            "dashboard_summary": dashboard_summary,
            "trip_timeline": trip_timeline,
            "route_summary": route_summary
        })

    except Exception as e:

        return Response(
            {"error": str(e)},
            status=400
        )

@api_view(["POST"])
def generate_complete_trip(request):

    try:

        current_location = request.data.get("current_location")
        pickup_location = request.data.get("pickup_location")
        dropoff_location = request.data.get("dropoff_location")
        cycle_used_hours = float(
            request.data.get("cycle_used_hours",0)
        )
        trip_info = {

            "from_location": pickup_location,
            "to_location": dropoff_location,
            "carrier_name": request.data.get(
                "carrier_name",
                "Unknown Carrier"
            ),
            "truck_number": request.data.get(
                "truck_number",
                "N/A"
            ),
            "odometer": int(
                request.data.get("odometer",0)
            )
        }

        route_info = get_route_info(
            current_location,
            pickup_location,
            dropoff_location
        )

        result = generate_logs_from_trip(
            distance_miles=route_info["distance_miles"],
            cycle_used_hours=cycle_used_hours,
            trip_info=trip_info
        )

        return Response({
            "route_info": route_info,
            "trip_result": result
        })

    except Exception as e:

        return Response({"error": str(e)},status=400)
        
@api_view(["GET"])
def trip_history(request):

    trips = (
        Trip.objects
        .all()
        .order_by("-created_at")
    )

    data = []

    for trip in trips:

        data.append({

            "id": trip.id,
            "current_location":trip.current_location,
            "pickup_location":trip.pickup_location,
            "dropoff_location":trip.dropoff_location,
            "distance_miles":trip.distance_miles,
            "trip_days":trip.trip_days,
            "trip_status":trip.trip_status,
            "created_at":trip.created_at
        })

    return Response(data)

@api_view(["GET"])
def trip_detail(request, trip_id):

    trip = Trip.objects.get(id=trip_id)

    return Response({

        "id": trip.id,
        "current_location":trip.current_location,
        "pickup_location":trip.pickup_location,
        "dropoff_location":trip.dropoff_location,
        "route_info":trip.route_data,
        "hos_result":trip.hos_data,
        "timeline":trip.timeline_data,
        "trip_status":trip.trip_status
    }) 
    
@api_view(["GET"])
def dashboard_summary(request):

    trips = Trip.objects.all()

    total_distance = sum(
        trip.distance_miles
        for trip in trips
    )

    total_fuel_stops = sum(
        trip.fuel_stops
        for trip in trips
    )

    total_rest_stops = sum(
        trip.rest_stops
        for trip in trips
    )

    total_trip_days = sum(
        trip.trip_days
        for trip in trips
    )

    total_driving_hours = sum(
        trip.hos_data.get(
            "total_driving_hours",
            0
        )
        for trip in trips
    )

    return Response({
        "total_distance": round(
            total_distance,
            2
        ),
        "fuel_stops": total_fuel_stops,
        "rest_stops": total_rest_stops,
        "trip_days": total_trip_days,
        "driving_hours": round(
            total_driving_hours,
            2
        )
    }) 


@api_view(["POST"])
def generate_trip_logs(request):

    try:

        distance_miles = float(
            request.data.get("distance_miles",0)
        )

        cycle_used_hours = float(
            request.data.get("cycle_used_hours",0)
        )

        trip_info = {

            "from_location": request.data.get(
                "from_location",
                "Unknown"
            ),

            "to_location": request.data.get(
                "to_location",
                "Unknown"
            ),

            "carrier_name": request.data.get(
                "carrier_name",
                "Unknown Carrier"
            ),

            "truck_number": request.data.get(
                "truck_number",
                "N/A"
            ),

            "odometer": int(
                request.data.get("odometer",0)
            )
        }

        result = generate_logs_from_trip(
            distance_miles=distance_miles,
            cycle_used_hours=cycle_used_hours,
            trip_info=trip_info
        )

        return Response(result)

    except Exception as e:
        return Response({"error": str(e)},status=400)