from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from .hos_service import calculate_trip_schedule
from .pdf_service import generate_trip_pdf

BASE_DIR = Path(__file__).resolve().parent.parent.parent
IMAGE_PATH = (BASE_DIR /"assets" /"blank_logs" /"fmcsa_log_template.png")
GENERATED_DIR = (BASE_DIR /"assets" /"generated_logs")
GENERATED_DIR.mkdir(parents=True,exist_ok=True)
GRID_LEFT = 64
GRID_RIGHT = 452
PIXELS_PER_HOUR = (GRID_RIGHT - GRID_LEFT) / 24
ROWS = {
    "off_duty": 191,
    "sleeper": 208,
    "driving": 225,
    "on_duty": 242,
    "break": 191
}

def hour_to_x(hour):
    return round(GRID_LEFT +(hour * PIXELS_PER_HOUR))


def write_header(draw, day_data ,trip_info):
    today = datetime.now()
    try:
        font = ImageFont.truetype("arial.ttf", 10)
        small_font = ImageFont.truetype("arial.ttf", 8)

    except Exception:

        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Month
    draw.text((179, 8),today.strftime("%m"),fill="black",font=font)

    # Day
    draw.text((225, 8),today.strftime("%d"),fill="black",font=font)

    # Year
    draw.text((260, 8),today.strftime("%Y"),fill="black",font=font)
    
    # CARRIER NAME
    draw.text((317, 66),trip_info["carrier_name"],fill="black",font=font)

    # TOTAL MILES
    daily_miles = day_data["daily_miles"]

    draw.text((80, 70),str(round(daily_miles)),fill="black",font=font)

    # Total Mileage Today (Odometer)
    draw.text((160, 70),str(trip_info["odometer"]),fill="black",font=font)

    # TRUCK NUMBER
    draw.text((100, 106),trip_info["truck_number"],fill="black",font=small_font)
    
    # FROM
    draw.text((92, 35),trip_info["from_location"],fill="black",font=font)

    # TO
    draw.text((276, 35),trip_info["to_location"],fill="black",font=font)

    # REMARKS
    draw.text((28, 287),f"{trip_info['from_location']} to {trip_info['to_location']}",fill="black",font=font)

def draw_activity(
    draw,
    activity_type,
    start_hour,
    end_hour
):

    row_type = activity_type

    if activity_type == "break": row_type = "off_duty"

    y = ROWS[row_type]
    x1 = hour_to_x(start_hour)
    x2 = hour_to_x(end_hour)

    draw.line(
        [(int(x1), int(y)),(int(x2), int(y))],
        fill="black",
        width=2
    )


def draw_transition(
    draw,
    from_status,
    to_status,
    at_hour
):

    if from_status == "break": from_status = "off_duty"
    if to_status == "break":to_status = "off_duty"
    x = hour_to_x(at_hour)
    y1 = ROWS[from_status]
    y2 = ROWS[to_status]

    draw.line([(int(x), int(y1)),(int(x), int(y2))],fill="black",width=2)

def generate_day_log(day_data, trip_info):

    image = Image.open(IMAGE_PATH).convert("RGB")
    draw = ImageDraw.Draw(image)
    write_header(draw,day_data ,trip_info)  
    activities = day_data["activities"]

    # Draw Activities

    for activity in activities:

        draw_activity(
            draw,
            activity["type"],
            activity["start"],
            activity["end"]
        )

    # Draw Transitions

    for i in range(len(activities) - 1):
        current_activity = activities[i]
        next_activity = activities[i + 1]

        draw_transition(
            draw,
            current_activity["type"],
            next_activity["type"],
            current_activity["end"]
        )

    output_file = (GENERATED_DIR /f"day_{day_data['day']}_log.png")
    image.save(output_file)

    return (f"/media/generated_logs/"f"day_{day_data['day']}_log.png")

def generate_logs_from_trip(
    distance_miles,
    cycle_used_hours,
    trip_info=None
):

    # Default values only for testing
    if trip_info is None:
        trip_info = {
            "from_location": "Unknown",
            "to_location": "Unknown",
            "carrier_name": "Unknown Carrier",
            "truck_number": "N/A",
            "odometer": 0
        }

    trip_data = calculate_trip_schedule(
        distance_miles=distance_miles,
        cycle_used_hours=cycle_used_hours
    )

    generated_files = []
    current_odometer = int(trip_info.get("odometer", 0))

    # Generate log images
    for day in trip_data["days"]:

        day_trip_info = trip_info.copy()
        day_trip_info["odometer"] = current_odometer
        file_path = generate_day_log(day,day_trip_info)
        generated_files.append(file_path)
        current_odometer += round(day["daily_miles"])

    # Generate PDF after all images are created
    pdf_file = generate_trip_pdf(
    [
        str(
            GENERATED_DIR /
            f"day_{day['day']}_log.png"
        )
        for day in trip_data["days"]
    ]
)

    return {
    "trip_summary": trip_data,
    "trip_info": trip_info,
    "generated_files": generated_files,
    "pdf_file": pdf_file
}