from django.urls import path
from .views import download_pdf

from .views import (
    health_check,
    calculate_hos,
    generate_trip_logs,
    calculate_trip,
    generate_complete_trip,
    trip_history,
    trip_detail,
    dashboard_summary,
    generate_eld_log,
    export_eld_pdf,
)

urlpatterns = [

    path("health/",health_check,name="health_check"),

    path("calculate-hos/",calculate_hos,name="calculate_hos"),

    path("generate-trip-logs/",generate_trip_logs,name="generate_trip_logs"),

    path("calculate-trip/",calculate_trip,name="calculate_trip"),

    path("generate-complete-trip/",generate_complete_trip,name="generate_complete_trip"),

    path("trip-history/",trip_history,name="trip_history"),

    path("trip/<int:trip_id>/",trip_detail,name="trip_detail"),

    path("dashboard-summary/",dashboard_summary,name="dashboard_summary"),

    path("generate-eld-log/",generate_eld_log,name="generate_eld_log"),

    path("export-eld-pdf/<int:eld_id>/",export_eld_pdf,name="export_eld_pdf"),
    
    path("download-pdf/<str:filename>/",download_pdf,name="download_pdf"),
]