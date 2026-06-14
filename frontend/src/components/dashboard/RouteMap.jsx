import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline,
  useMap
} from "react-leaflet";
import { useEffect } from "react";
import L from "leaflet";
import polyline from "@mapbox/polyline";

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

const fuelIcon = L.divIcon({
  html: `
    <div style="
      font-size:28px;
      display:flex;
      align-items:center;
      justify-content:center;
    ">
      ⛽
    </div>
  `,
  className: "",
  iconSize: [30, 30],
  iconAnchor: [15, 15],
});

function FitBounds({ points }) {
  const map = useMap();

  useEffect(() => {
    if (points.length > 0) {
      map.fitBounds(points);
    }
  }, [map, points]);

  return null;
}

export default function RouteMap({ routeInfo }) {
    console.log("Fuel Stops:", routeInfo.fuel_stop_locations);
  if (!routeInfo) return null;

  const points = routeInfo.waypoints.map(
    ([lng, lat]) => [lat, lng]
  );

  const routeLine = routeInfo.geometry
    ? polyline.decode(routeInfo.geometry)
    : points;

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h2 className="text-xl font-bold mb-4">
        Route Map
      </h2>

      <MapContainer
        center={points[0]}
        zoom={5}
        style={{
          height: "500px",
          width: "100%",
          borderRadius: "12px",
        }}
      >
        <FitBounds points={points} />

        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />

        {/* Current / Pickup / Dropoff Markers */}
        {points.map((point, index) => (
          <Marker
            key={index}
            position={point}
          >
            <Popup>
              {routeInfo.stops[index]?.location}
            </Popup>
          </Marker>
        ))}

        {/* Fuel Stop Markers */}
        {routeInfo.fuel_stop_locations?.map((stop) => (
          <Marker
            key={`fuel-${stop.number}`}
            position={[
              stop.lat,
              stop.lng
            ]}
            icon={fuelIcon}
          >
            <Popup>
              <div>
                <strong>
                  Fuel Stop #{stop.number}
                </strong>
                <br />
                Mile Marker: {stop.mile_marker}
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Route Line */}
        <Polyline
          positions={routeLine}
          pathOptions={{
            color: "#2563eb",
            weight: 5,
          }}
        />
      </MapContainer>
    </div>
  );
}