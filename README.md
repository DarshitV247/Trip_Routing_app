# Truck Routing & HOS Compliance Planner

## Overview

Truck Routing & HOS Compliance Planner is a full-stack logistics and compliance management platform designed to help trucking companies, dispatchers, and fleet operators plan trips while maintaining FMCSA Hours of Service (HOS) compliance.

The application calculates routes, generates HOS-compliant schedules, creates FMCSA-style ELD log sheets, tracks fuel and rest stops, and exports downloadable PDF trip packets for compliance documentation.

---

# Features

## Trip Planning

* Current Location → Pickup → Dropoff route planning
* Route distance calculation
* Estimated travel duration
* Multi-day trip scheduling
* Route summary generation

## Hours of Service (HOS)

* FMCSA-compliant scheduling
* Daily driving hour calculations
* Mandatory break scheduling
* Off-duty management
* Sleeper berth scheduling
* Cycle hour tracking
* Multi-day trip support

## Fuel Stop Planning

* Automatic fuel stop estimation
* Fuel stop count generation
* Fuel stop timeline integration

## Rest Stop Planning

* Automatic break scheduling
* HOS-compliant rest periods
* Rest stop tracking

## Trip Timeline

Generate a complete trip timeline including:

* Current Location
* Pickup Location
* Fuel Stops
* Rest Stops
* Dropoff Location

## ELD Log Generation

Generate FMCSA-style ELD logs containing:

* Carrier Name
* Truck Number
* Trailer Number
* Shipping Document Information
* Odometer Reading
* Daily Activity Records
* Duty Status Logs

## FMCSA Daily Log Sheets

Automatically generates:

* Daily Log Sheets
* Duty Status Graphs
* Driver Activity Timelines
* Printable Compliance Records

## PDF Export

Generate downloadable PDF trip packets containing:

* Daily ELD Logs
* FMCSA Duty Status Charts
* Multi-Day Driver Logs
* Compliance Documentation

## Dashboard Analytics

* Total Trips
* Total Distance
* Fuel Stop Count
* Rest Stop Count
* Trip Statistics

## Trip History

* View Historical Trips
* Access Trip Details
* Review Generated Reports
* Retrieve Route Summaries

---

# Technology Stack

## Frontend

* React.js
* Vite
* Tailwind CSS
* Axios
* React Hot Toast
* Lucide React

## Backend

* Django
* Django REST Framework
* Python

## Routing Services

* OpenRouteService API
* Geopy

## PDF & Log Generation

* ReportLab
* Pillow (PIL)

## Database

* SQLite

---

# System Architecture

Frontend (Vercel)

↓

Django REST API (Render)

↓

SQLite Database

↓

PDF & Log Generation Services

---

# Project Structure

backend/

├── config/

├── trips/

│ ├── models.py

│ ├── views.py

│ ├── urls.py

│ ├── services/

│ │ ├── hos_service.py

│ │ ├── route_service.py

│ │ ├── log_service.py

│ │ └── pdf_service.py

│

├── assets/

│ ├── blank_logs/

│ ├── generated_logs/

│ └── generated_pdfs/

│

├── manage.py

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
python manage.py migrate
```

### Start Backend

```bash
python manage.py runserver
```

Backend URL:

```text
http://127.0.0.1:8000
```

---

## Frontend Setup

### Install Dependencies

```bash
npm install
```

### Run Frontend

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

# Environment Variables

Create a `.env` file inside the backend folder:

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

## Trip Detail

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

# Deployment

## Frontend

Hosted on Vercel

## Backend

Hosted on Render

---

# Future Enhancements

* User Authentication
* Fleet Management Dashboard
* Driver Portal
* Real-Time GPS Tracking
* Driver Scorecards
* Fuel Cost Estimation
* Maintenance Scheduling
* AI-Based Route Optimization
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

