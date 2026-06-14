import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000/api",
});

export const getDashboardSummary = () => API.get("/dashboard-summary/");

export const calculateTrip = (data) => API.post("/calculate-trip/", data);

export const getTrips = () => API.get("/trips/");

export const generateEldLog = (data) => API.post("/generate-eld-log/",data);