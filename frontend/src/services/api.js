import axios from "axios";

const API = axios.create({
  baseURL: "https://trip-routing-app.onrender.com/api",
});

export const getDashboardSummary = () => API.get("/dashboard-summary/");

export const calculateTrip = (data) => API.post("/calculate-trip/", data);

export const getTrips = () => API.get("/trips/");

export const generateEldLog = (data) => API.post("/generate-eld-log/",data);  