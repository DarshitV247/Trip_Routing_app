import {
  MapPin,
  Package,
  Fuel,
  Coffee
} from "lucide-react";

export default function TripTimeline({ timeline }) {
  if (!timeline) return null;

  const getIcon = (type) => {
    switch (type) {
      case "current_location":
        return <MapPin size={18} />;

      case "pickup":
        return <Package size={18} />;

      case "fuel_stop":
        return <Fuel size={18} />;

      case "rest_stop":
        return <Coffee size={18} />;

      case "dropoff":
        return <MapPin size={18} />;

      default:
        return <MapPin size={18} />;
    }
  };

  const getLabel = (item) => {
    switch (item.type) {
      case "current_location":
        return `Current Location: ${item.location}`;

      case "pickup":
        return `Pickup: ${item.location}`;

      case "fuel_stop":
        return `Fuel Stop no.${item.number}`;

      case "rest_stop":
        return `Rest Stop Day ${item.day}`;

      case "dropoff":
        return `Destination: ${item.location}`;

      default:
        return item.type;
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h2 className="text-xl font-bold mb-6">
        Trip Timeline
      </h2>

      <div className="space-y-4">
        {timeline.map((item, index) => (
          <div
            key={index}
            className="flex items-center gap-4 border-l-2 border-blue-500 pl-4"
          >
            <div className="text-blue-600">
              {getIcon(item.type)}
            </div>

            <div>
              <p className="font-medium">
                {getLabel(item)}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}