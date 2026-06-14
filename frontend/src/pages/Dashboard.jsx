import { useEffect, useState } from "react";
import { getDashboardSummary } from "../services/api";
import Sidebar from "../components/layout/Sidebar";
import Navbar from "../components/layout/Navbar";
import HeroBanner from "../components/dashboard/HeroBanner";
import SummaryCards from "../components/dashboard/SummaryCards";
import TripForm from "../components/forms/TripForm";
import TripTimeline from "../components/dashboard/TripTimeline";
import RouteSummary from "../components/dashboard/RouteSummary";
import RouteMap from "../components/dashboard/RouteMap";
import ELDLogSheet from "../components/dashboard/ELDLogSheet";
import ELDForm from "../components/forms/ELDForm";

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [tripData, setTripData] = useState(null);
  const [eldInfo, setEldInfo] = useState(null);
  const [eldId, setEldId] = useState(null);

  const fetchSummary = async () => {
    try {
      const response = await getDashboardSummary();
      setSummary(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    fetchSummary();
  }, []);

  const handleTripCalculated = (data) => {
    setTripData(data);

    if (data.dashboard_summary) {
      setSummary(data.dashboard_summary);
    }
  };

  return (
    <div className="flex min-h-screen bg-slate-50">
      {/* <Sidebar /> */}

      <div className="flex-1 flex flex-col">
        <Navbar />

        <main className="flex-1 p-6">
          <div className="max-w-7xl mx-auto space-y-6">
            <HeroBanner />
            <SummaryCards summary={summary} />
            <TripForm onTripCalculated={handleTripCalculated}/>
              {tripData && (
                <>
                  <ELDForm tripId={tripData.trip_id} onGenerate={(data) => {
                    setEldInfo(data);
                    setEldId(data.eld_id);
                    }}
                  /> 
                  <RouteMap routeInfo={tripData.route_info}/>
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <TripTimeline timeline={tripData.trip_timeline}/>
                    <RouteSummary summary={tripData.route_summary}/>
                    {/* <ELDLogSheet days={tripData.hos_result.days}/> */}
                  </div>
                </>
              )}
          </div>
        </main>
      </div>
    </div>
  );
}