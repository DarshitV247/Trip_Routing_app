import math

# FMCSA Assumptions
AVERAGE_SPEED = 55          # mph
MAX_DRIVING_HOURS = 11      # per day
BREAK_AFTER_HOURS = 8       # hours
BREAK_DURATION = 0.5        # 30 minutes


def calculate_trip_schedule(distance_miles, cycle_used_hours):
    """
    Simplified FMCSA calculation.

    Assumptions:
    - Average speed = 55 mph
    - Max driving = 11 hrs/day
    - Break after 8 hrs driving
    - Pickup = 1 hr
    - Dropoff = 1 hr
    - Fuel stop every 1000 miles
    """

    driving_hours = round(distance_miles / AVERAGE_SPEED,2)
    remaining_drive = driving_hours

    days = []
    day_number = 1

    while remaining_drive > 0:

        today_drive = min(MAX_DRIVING_HOURS,remaining_drive)

        day_plan = {
            "day": day_number,
            "pickup_hours": 1 if day_number == 1 else 0,
            "driving_hours": round(today_drive, 2),
            "break_hours": BREAK_DURATION if today_drive >= BREAK_AFTER_HOURS else 0,
            "dropoff_hours": 1 if remaining_drive <= MAX_DRIVING_HOURS else 0,
        }

        days.append(day_plan)
        remaining_drive -= today_drive
        day_number += 1

    fuel_stops = max(0,math.ceil(distance_miles / 1000) - 1)

    return {
        "distance_miles": distance_miles,
        "total_driving_hours": driving_hours,
        "fuel_stops": fuel_stops,
        "days": days,
        "cycle_used_hours": cycle_used_hours,
    }