export default function RouteSummary({ summary }) {
  if (!summary) return null;

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h2 className="text-xl font-bold mb-5">
        Route Summary
      </h2>

      <div className="space-y-4">
        {summary.map((step, index) => (
          <div
            key={index}
            className="flex items-center gap-3"
          >
            <div className="w-3 h-3 rounded-full bg-blue-600" />

            <p className="text-slate-700">
              {step}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}