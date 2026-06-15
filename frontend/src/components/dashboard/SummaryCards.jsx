import {
  Route,
  Clock3,
  Fuel,
  Calendar,
  Coffee
} from "lucide-react";

export default function SummaryCards({ summary }) {

  if (!summary) {
  summary = {
    total_distance: 0,
    driving_hours: 0,
    fuel_stops: 0,
    trip_days: 0,
    rest_stops: 0
  };
}

  const cards = [
    {
      title: "Distance",
      value: `${summary.total_distance} miles`,
      icon: Route
    },
    {
      title: "Driving Hours",
      value: `${summary.driving_hours} hrs`,
      icon: Clock3
    },
    {
      title: "Fuel Stops",
      value: summary.fuel_stops,
      icon: Fuel
    },
    {
      title: "Trip Days",
      value: summary.trip_days,
      icon: Calendar
    },
    {
      title: "Rest Stops",
      value: summary.rest_stops,
      icon: Coffee
    }
  ];

  return (
    <div
      className="
        grid
        grid-cols-2
        md:grid-cols-3
        xl:grid-cols-5
        gap-4
      "
    >
      {cards.map((card) => {

        const Icon = card.icon;

        return (
          <div
            key={card.title}
            className="
              bg-white
              rounded-2xl
              p-5
              border
              shadow-sm
              hover:shadow-lg
              transition-all
              duration-300
            "
          >
            {/* Title Row */}
            <div className="flex items-center gap-2 mb-3">

              <Icon
                size={18}
                className="text-blue-600"
              />

              <span
                className="
                  text-sm
                  md:text-base
                  font-medium
                  text-slate-500
                "
              >
                {card.title}
              </span>

            </div>

            {/* Value */}
            <h2
              className="
                text-2xl
                md:text-3xl
                font-bold
                text-slate-800
                break-words
              "
            >
              {card.value}
            </h2>

          </div>
        );
      })}
    </div>
  );
}