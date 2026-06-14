import os
import requests
from dotenv import load_dotenv
import polyline
from geopy.distance import geodesic
load_dotenv()

ORS_API_KEY = os.getenv("ORS_API_KEY")


def get_coordinates(place_name):

    url = "https://api.openrouteservice.org/geocode/search"

    headers = {"Authorization": ORS_API_KEY}

    params = {"text": place_name,"size": 1}

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    response.raise_for_status()
    data = response.json()
    features = data.get("features", [])

    if not features:
        raise Exception(
            f"Location not found: {place_name}"
        )

    return (
        features[0]
        ["geometry"]
        ["coordinates"]
    )

def calculate_fuel_stops(
    geometry,
    stop_interval_miles=1000
):
    route_points = polyline.decode(geometry)

    fuel_stops = []

    accumulated = 0

    next_stop = stop_interval_miles

    for i in range(1, len(route_points)):

        prev_point = route_points[i - 1]
        current_point = route_points[i]

        segment_distance = geodesic(
            prev_point,
            current_point
        ).miles

        accumulated += segment_distance

        if accumulated >= next_stop:

            fuel_stops.append({
                "type": "fuel_stop",
                "number": len(fuel_stops) + 1,
                "lat": current_point[0],
                "lng": current_point[1],
                "mile_marker": round(accumulated, 2)
            })

            next_stop += stop_interval_miles
    return fuel_stops

def get_route_info(
    current_location,
    pickup_location,
    dropoff_location
):

    current = get_coordinates(current_location)

    pickup = get_coordinates(pickup_location)

    dropoff = get_coordinates(dropoff_location)

    url = (
        "https://api.openrouteservice.org"
        "/v2/directions/driving-car"
    )

    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [current,pickup, dropoff],
        "radiuses": [5000,5000,5000]
    }

    response = requests.post(
        url,
        json=body,
        headers=headers
    )

    response.raise_for_status()

    data = response.json()

    route = data["routes"][0]

    summary = route["summary"]

    # Real route geometry
    geometry = route["geometry"]
    fuel_stop_locations = calculate_fuel_stops(geometry)

    distance_meters = summary["distance"]

    duration_seconds = summary["duration"]

    distance_miles = round(distance_meters * 0.000621371,2)

    duration_hours = round(duration_seconds / 3600,2)

    fuel_stops = int(distance_miles // 1000)

    instructions = []

    for segment in route["segments"]:

        for step in segment["steps"]:

            instructions.append({
                "instruction": step.get("instruction",""),
                "distance_meters": round(
                    step.get("distance",0),2
                ),
                "duration_seconds": round(
                    step.get("duration",0),2
                )
            })

    stops = [
        {
            "type": "current",
            "location": current_location
        },
        {
            "type": "pickup",
            "location": pickup_location
        },
        {
            "type": "dropoff",
            "location": dropoff_location
        }
    ]

    return {
        "current_location": current_location,
        "pickup_location": pickup_location,
        "dropoff_location": dropoff_location,
        "fuel_stop_locations": fuel_stop_locations,
        "distance_miles": distance_miles,
        "duration_hours": duration_hours,
        "fuel_stops": fuel_stops,

        # Needed for real map route
        "geometry": geometry,

        "waypoints": [
            current,
            pickup,
            dropoff
        ],

        "stops": stops,

        "instructions": instructions,

        "route_summary": [
            f"Start from {current_location}",
            f"Travel to pickup location {pickup_location}",
            f"Fuel stops required: {fuel_stops}",
            f"Continue towards {dropoff_location}",
            "Arrive at destination"
        ]
    }