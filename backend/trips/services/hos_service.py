import math

# FMCSA Assumptions
AVERAGE_SPEED = 55
MAX_DRIVING_HOURS = 11
BREAK_AFTER_HOURS = 8
BREAK_DURATION = 0.5


def create_day_timeline(
    day_number,
    driving_hours,
    daily_miles,
    is_first_day,
    is_last_day
):

    activities = []

    # Midnight to 6 AM = Off Duty
    activities.append({
        "type": "off_duty",
        "start": 0,
        "end": 6
    })

    current_time = 6.0

    # Pickup
    if is_first_day:

        activities.append({
            "type": "on_duty",
            "start": current_time,
            "end": current_time + 1
        })

        current_time += 1

    # First driving block
    first_drive = min(BREAK_AFTER_HOURS,driving_hours)

    activities.append({
        "type": "driving",
        "start": current_time,
        "end": current_time + first_drive
    })

    current_time += first_drive
    remaining_drive = driving_hours - first_drive

    # 30-minute break after 8 hours driving
    if driving_hours >= BREAK_AFTER_HOURS:

        activities.append({
            "type": "off_duty",
            "start": current_time,
            "end": current_time + BREAK_DURATION
        })

        current_time += BREAK_DURATION

    # Remaining driving
    if remaining_drive > 0:

        activities.append({
            "type": "driving",
            "start": current_time,
            "end": current_time + remaining_drive
        })

        current_time += remaining_drive

    # Dropoff
    if is_last_day:

        activities.append({
            "type": "on_duty",
            "start": current_time,
            "end": current_time + 1
        })

        current_time += 1

    # End of day
    if current_time < 24:

        activities.append({
            "type": "off_duty",
            "start": current_time,
            "end": 24
        })

    return {
        "day": day_number,
        "daily_miles": round(daily_miles, 2),
        "activities": activities
    }


def calculate_trip_schedule(distance_miles,cycle_used_hours):

    total_driving_hours = round(distance_miles / AVERAGE_SPEED,2)
    remaining_drive = total_driving_hours
    day_plans = []

    while remaining_drive > 0:

        today_drive = min(MAX_DRIVING_HOURS,remaining_drive)
        day_plans.append(today_drive)
        remaining_drive -= today_drive

    timeline_days = []
    remaining_distance = distance_miles

    for index, hours in enumerate(day_plans):

        daily_miles = min(remaining_distance,hours * AVERAGE_SPEED)

        timeline_days.append(
            create_day_timeline(
                day_number=index + 1,
                driving_hours=hours,
                daily_miles=daily_miles,
                is_first_day=(index == 0),
                is_last_day=(index == len(day_plans) - 1)
            )
        )

        remaining_distance -= daily_miles

    fuel_stops = max(0,math.ceil(distance_miles / 1000) - 1)

    return {
        "distance_miles": distance_miles,
        "total_driving_hours": total_driving_hours,
        "fuel_stops": fuel_stops,
        "cycle_used_hours": cycle_used_hours,
        "days": timeline_days
    }