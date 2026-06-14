import { Loader2 } from "lucide-react";
import { useState } from "react";
import { calculateTrip } from "../../services/api";
import toast from "react-hot-toast";

export default function TripForm({ onTripCalculated }) {
  const [formData, setFormData] = useState({
    current_location: "",
    pickup_location: "",
    dropoff_location: "",
    cycle_used_hours: "",
  });

  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));

    // Clear error when user starts typing
    if (errors[e.target.name]) {
      setErrors((prev) => ({
        ...prev,
        [e.target.name]: "",
      }));
    }
  };

  const validate = () => {
    let newErrors = {};

    if (!formData.current_location.trim()) {
      newErrors.current_location = "Current location is required";
    }

    if (!formData.pickup_location.trim()) {
      newErrors.pickup_location = "Pickup location is required";
    }

    if (!formData.dropoff_location.trim()) {
      newErrors.dropoff_location = "Dropoff location is required";
    }

    if (formData.cycle_used_hours === "") {
      newErrors.cycle_used_hours = "Cycle used hours is required";
    }

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };

 const handleSubmit = async (e) => {
  e.preventDefault();

  if (!validate()) return;

  try {
    setLoading(true);

    const response = await calculateTrip(formData);

if (response.data.duplicate) {
  toast((t) => (
  <div className="flex items-center justify-between w-full">
    <span>Trip already exists!</span>

    <button
      onClick={() => toast.dismiss(t.id)}
      className="ml-4 text-white font-bold text-lg cursor-pointer"
    >
      ✕
    </button>
  </div>
), {
  style: {
    background: "#dc2626",
    color: "#fff",
    minWidth: "450px",
    minHeight: "70px",
    padding: "20px",
    borderRadius: "12px",
  },
});
  return;
}

if (typeof onTripCalculated === "function") {
  onTripCalculated(response.data);
}

toast((t) => (
  <div className="flex items-center justify-between w-full">
    <span>Trip calculated successfully!</span>

    <button
      onClick={() => toast.dismiss(t.id)}
      className="ml-4 text-white font-bold text-lg cursor-pointer"
    >
      ✕
    </button>
  </div>
), {
  style: {
    background: "#16a34a",
    color: "#fff",
    minWidth: "450px",
    minHeight: "70px",
    padding: "20px",
    borderRadius: "12px",
  },
});

    setErrors({});
  } catch (error) {
    console.error(error);
    toast.error("Failed to calculate trip");
  } finally {
  setLoading(false);

  setFormData({
    current_location: "",
    pickup_location: "",
    dropoff_location: "",
    cycle_used_hours: "",
  });

  setErrors({});
}
};

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <div className="border-b pb-4 mb-5">
        <h2 className="text-2xl font-bold flex items-center gap-2">
          Calculate New Trip
        </h2>
      </div>

      <form
        onSubmit={handleSubmit}
        className="grid grid-cols-1 md:grid-cols-2 gap-5"
      >
        <div>
          <input
            name="current_location"
            value={formData.current_location}
            onChange={handleChange}
            placeholder="Current Location"
            className="border rounded-lg p-3 w-full"
          />
          {errors.current_location && (
            <p className="text-red-500 text-sm mt-1">
              {errors.current_location}
            </p>
          )}
        </div>

        <div>
          <input
            name="pickup_location"
            value={formData.pickup_location}
            onChange={handleChange}
            placeholder="Pickup Location"
            className="border rounded-lg p-3 w-full"
          />
          {errors.pickup_location && (
            <p className="text-red-500 text-sm mt-1">
              {errors.pickup_location}
            </p>
          )}
        </div>

        <div>
          <input
            name="dropoff_location"
            value={formData.dropoff_location}
            onChange={handleChange}
            placeholder="Dropoff Location"
            className="border rounded-lg p-3 w-full"
          />
          {errors.dropoff_location && (
            <p className="text-red-500 text-sm mt-1">
              {errors.dropoff_location}
            </p>
          )}
        </div>

        <div>
          <input
            type="number"
            name="cycle_used_hours"
            value={formData.cycle_used_hours}
            onChange={handleChange}
            placeholder="Cycle Used Hours"
            className="border rounded-lg p-3 w-full"
          />
          {errors.cycle_used_hours && (
            <p className="text-red-500 text-sm mt-1">
              {errors.cycle_used_hours}
            </p>
          )}
        </div>

        <div className="md:col-span-2 flex justify-center">
          <button
  type="submit"
  disabled={loading}
  className="
    px-10 py-3
    bg-blue-600
    hover:bg-blue-700
    active:scale-95
    text-white
    font-semibold
    rounded-lg
    shadow-md
    hover:shadow-lg
    transition-all
    duration-200
    cursor-pointer
    flex items-center gap-2
    disabled:opacity-50
    disabled:cursor-not-allowed
    disabled:hover:bg-blue-600
  "
>
  {loading ? (
    <>
      <Loader2 size={18} className="animate-spin" />
      Calculating...
    </>
  ) : (
    "Calculate Trip"
  )}
</button>
        </div>
      </form>
    </div>
  );
}