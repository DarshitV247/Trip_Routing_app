from django.db import models


class Trip(models.Model):

    current_location = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    cycle_used_hours = models.FloatField()
    distance_miles = models.FloatField()
    duration_hours = models.FloatField()
    fuel_stops = models.IntegerField(default=0)
    rest_stops = models.IntegerField(default=0)
    trip_days = models.IntegerField(default=1)
    trip_status = models.CharField(max_length=50)
    route_data = models.JSONField(null=True, blank=True)
    hos_data = models.JSONField(null=True, blank=True)
    timeline_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "current_location",
                    "pickup_location",
                    "dropoff_location",
                    "cycle_used_hours"
                ],
                name="unique_trip"
            )
        ]

    def __str__(self):
        return (
            f"{self.pickup_location}"
            f" → "
            f"{self.dropoff_location}"
        )
        
class ELDLog(models.Model):

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="eld_logs"
    )

    carrier_name = models.CharField(
        max_length=255
    )

    truck_number = models.CharField(
        max_length=100
    )

    trailer_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    shipping_document = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    odometer_start = models.IntegerField()

    eld_data = models.JSONField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Trip #{self.trip.id}"