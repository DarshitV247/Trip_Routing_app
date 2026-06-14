# Truck Routing & HOS Compliance Planner

## Overview

Truck Routing & HOS Compliance Planner is a full-stack logistics management application designed to help trucking companies, dispatchers, and fleet managers efficiently plan routes while maintaining FMCSA Hours of Service (HOS) compliance.

The system calculates optimized trip routes, estimates fuel stops, generates HOS-compliant schedules, creates ELD log sheets, and exports professional PDF reports for driver records and compliance documentation.

---

# Features

## Route Planning

* Current Location → Pickup → Dropoff route calculation
* Route distance estimation
* Travel duration estimation
* Turn-by-turn route instructions
* Route summary generation
* Interactive route map visualization

## Fuel Stop Planning

* Automatic fuel stop calculation
* Fuel stop placement based on trip distance
* Fuel stop markers displayed on map
* Fuel stop timeline generation

## Hours of Service (HOS)

* FMCSA-compliant trip scheduling
* Driving hour calculations
* Rest break planning
* Off-duty scheduling
* Sleeper berth scheduling
* Multi-day trip planning
* Cycle hour tracking

## Trip Timeline

* Current location
* Pickup location
* Fuel stops
* Rest stops
* Dropoff location

Presented in a clear chronological timeline.

## ELD Log Generation

Generate electronic logging device (ELD) records including:

* Carrier Name
* Truck Number
* Odometer Reading
* Route Information
* Daily Activity Logs
* Duty Status Records

## FMCSA Log Sheets

Automatic generation of:

* Daily log sheets
* Duty status graphs
* Activity summaries
* Printable records

## PDF Export

Generate downloadable trip packets including:

* Daily ELD logs
* FMCSA-style duty status charts
* Multi-day reports
* PDF documentation

## Dashboard Analytics

* Total trips
* Total distance traveled
* Fuel stop count
* Rest stop count
* Trip statistics

## Trip History

* View previous trips
* Retrieve trip details
* Access generated ELD reports
* Review route summaries

---

# Technology Stack

## Frontend

* React.js
* Vite
* Tailwind CSS
* Axios
* React Hot Toast
* Lucide React
* Leaflet Maps
* React Leaflet

## Backend

* Django
* Django REST Framework
* Python

## Mapping & Routing

* OpenRouteService API
* Geopy
* Polyline

## PDF & Log Generation

* ReportLab
* Pillow (PIL)

## Database

* SQLite (Development)
* PostgreSQL (Production Ready)

---

# Project Structure

backend/

├── config/

├── trips/

│ ├── models.py

│ ├── views.py

│ ├── urls.py

│ ├── serializers.py

│ └── services/

│ ├── hos_service.py

│ ├── route_service.py

│ ├── log_service.py

│ └── pdf_service.py

│

├── assets/

│ ├── blank_logs/

│ ├── generated_logs/

│ └── generated_pdfs/

│

└── db.sqlite3

frontend/

├── src/

│ ├── components/

│ ├── pages/

│ ├── services/

│ └── App.jsx

│

└── public/

---

# Installation

## Backend Setup

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Start Backend Server

```bash
python manage.py runserver
```

Backend runs at:

```text
http://127.0.0.1:8000
```

---

# Frontend Setup

Install Dependencies

```bash
npm install
```

Run Development Server

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

# Environment Variables

Create a `.env` file inside backend:

```env
ORS_API_KEY=YOUR_OPENROUTESERVICE_API_KEY
```

---

# API Endpoints

## Health Check

```http
GET /api/health/
```

## Calculate HOS

```http
POST /api/calculate-hos/
```

## Calculate Trip

```http
POST /api/calculate-trip/
```

## Generate Complete Trip

```http
POST /api/generate-complete-trip/
```

## Trip History

```http
GET /api/trip-history/
```

## Trip Details

```http
GET /api/trip/<trip_id>/
```

## Dashboard Summary

```http
GET /api/dashboard-summary/
```

## Generate ELD Log

```http
POST /api/generate-eld-log/
```

## Download PDF

```http
GET /api/download-pdf/<filename>/
```

---

# Future Enhancements

* User Authentication
* Driver Login Portal
* Fleet Management Dashboard
* Real-Time GPS Tracking
* Driver Scorecards
* Fuel Cost Estimation
* Maintenance Scheduling
* AI-Based Route Optimization
* Multi-Carrier Support
* Mobile Application
* Cloud Storage Integration
* Role-Based Access Control

---

# Use Cases

* Trucking Companies
* Fleet Operators
* Dispatch Teams
* Logistics Providers
* Freight Brokers
* Compliance Managers
* Transportation Startups

---
"# TripRouting" 
