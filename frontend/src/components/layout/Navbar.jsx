import {
  Bell,
  UserCircle2,
  Truck
} from "lucide-react";

export default function Navbar() {
  return (
    <header className="bg-white border-b px-8 h-20 flex items-center justify-between sticky top-0 z-50">
      {/* Left Side */}
      <div className="flex items-center gap-4">

        <div className=" h-12 w-12 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white flex items-center justify-center shadow-lg">
          <Truck size={24} />
        </div>

        <div>
          <h1 className="text-2xl font-bold text-slate-800">Truck Routing Dashboard</h1>

          <p className="text-sm text-slate-500">
            Route Planning • HOS Tracking • ELD Management
          </p>
        </div>
      </div>

      {/* Right Side */}
      <div className="flex items-center gap-5">

        <div className="flex items-center gap-3 bg-slate-100 px-4 py-2 rounded-xl">
          <UserCircle2
            size={36}
            className="text-slate-700"
          />

          <div>
            <p className="font-semibold text-sm">Dispatcher</p>

            <p className="text-xs text-slate-500">Operations Manager</p>
          </div>
        </div>
      </div>
    </header>
  );
}