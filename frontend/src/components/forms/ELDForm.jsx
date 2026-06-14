import { useState } from "react";
import { generateEldLog } from "../../services/api";
import toast from "react-hot-toast";

export default function ELDForm({tripId, onGenerate}) {

  const [formData, setFormData] =
    useState({
      carrier_name: "",
      truck_number: "",
      odometer_start: "",
    });

const handleSubmit = async (e) => {
  e.preventDefault();

  try {

    const payload = {...formData,trip_id: tripId,};
    const response = await generateEldLog(payload);
    const filename = response.data.pdf_file.split("/").pop();
    const link = document.createElement("a");

    link.href = `http://127.0.0.1:8000/api/download-pdf/${filename}/`;
    link.setAttribute("download",filename);

    document.body.appendChild(link);
    link.click();

    document.body.removeChild(link);
    toast.success("ELD Log Generated");

    onGenerate(response.data);

  } catch (error) {

    console.error(error);
    toast.error(error.response?.data?.error ||error.message ||"Failed to generate ELD");
  }
};

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h2 className="text-xl font-bold mb-5">ELD Information</h2>

      <form onSubmit={handleSubmit} className="grid md:grid-cols-2 gap-4">

        <input
          placeholder="Carrier Name"
          className="border p-3 rounded"
          onChange={(e) =>setFormData({...formData,carrier_name:e.target.value,})}
        />

        <input
          placeholder="Truck Number"
          className="border p-3 rounded"
          onChange={(e) =>setFormData({...formData,truck_number:e.target.value,})
          }
        />

        <input
          placeholder="Starting Odometer"
          className="border p-3 rounded"
          type="number"
          onChange={(e) =>setFormData({...formData, odometer_start:e.target.value,})
          }
        />

        <button type="submit" className="bg-blue-600 text-white rounded p-3 col-span-2">
          Generate ELD Log
        </button>
      </form>
    </div>
  );
}