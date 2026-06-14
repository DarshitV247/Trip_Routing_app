export default function ELDLogSheet({days,eldInfo,}) {
  if (!days?.length) return null;

  const statuses = [
    {
      key: "off_duty",
      label: "Off Duty",
    },
    {
      key: "sleeper",
      label: "Sleeper",
    },
    {
      key: "driving",
      label: "Driving",
    },
    {
      key: "on_duty",
      label: "On Duty",
    },
  ];

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">

      <h2 className="text-2xl font-bold mb-6">ELD Log Sheets</h2>
      <div className="grid grid-cols-1 2xl:grid-cols-2 gap-6">

        {days.map((day) => (

          <div key={day.day} className="border rounded-xl p-5 bg-white">
            <h3 className="text-xl font-bold mb-4">Day {day.day}</h3>

            {eldInfo && (
              <div className="grid md:grid-cols-3 gap-3 mb-4 text-sm bg-slate-50 p-3 rounded">
                <div>Carrier: {eldInfo.carrier_name}</div>
                <div>Truck: {eldInfo.truck_number}</div>
                <div>Trailer: {eldInfo.trailer_number}</div>
                <div>Shipping: {eldInfo.shipping_document}</div>
                <div>Odometer: {eldInfo.odometer_start}</div>
              </div>
            )}

            <div className="overflow-x-auto">
              <div className="min-w-[900px]">

                {/* Header */}
                <div className="grid grid-cols-[150px_repeat(24,minmax(0,1fr))] border">
                  <div className="border-r p-2 font-bold">Status</div>

                  {Array.from({ length: 24 }).map(
                    (_, hour) => (
                      <div key={hour} className="text-center text-xs border-r py-2 font-medium">
                        {hour}
                      </div>
                    )
                  )}
                </div>

                {/* Status Rows */}
                {statuses.map((status) => (

                  <div key={status.key} className="grid grid-cols-[150px_repeat(24,minmax(0,1fr))] border-x border-b">
                    <div className="border-r p-2 font-medium bg-slate-50"> {status.label}</div>
                    {Array.from({ length: 24 }).map((_, hour) => {

                        const active = day.activities.some(
                            (activity) => activity.type === status.key &&
                              hour >= Math.floor(activity.start) &&
                              hour < Math.ceil(activity.end)
                            );

                        return (
                          <div key={hour} className={`h-10 border-r
                              ${
                                active
                                  ? "bg-blue-500"
                                  : "bg-white"
                              }
                            `}
                          />
                        );
                      }
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Activity Details */}
            <div className="mt-5">
              <h4 className="font-semibold mb-2">Activity Details</h4>
              <div className="space-y-2">
                {day.activities.map((activity, index) => (

                    <div key={index} className="text-sm bg-slate-50 p-2 rounded">
                      <strong>{activity.type.replace("_"," ")}</strong>
                      {" : "}
                      {activity.start}h
                      {" - "}
                      {activity.end}h
                    </div>
                  )
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}