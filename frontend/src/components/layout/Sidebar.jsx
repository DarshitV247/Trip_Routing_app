import {
  LayoutDashboard,
  Route,
  History,
  FileText,
  Settings
} from "lucide-react";

export default function Sidebar() {

  const menuItems = [
    {
      name: "Dashboard",
      icon: LayoutDashboard
    },
    {
      name: "New Trip",
      icon: Route
    },
    {
      name: "Trip History",
      icon: History
    },
    {
      name: "Documents",
      icon: FileText
    },
    {
      name: "Settings",
      icon: Settings
    }
  ];

  return (
    <aside className="w-72 bg-white border-r border-slate-200 hidden lg:flex flex-col">

      <div className="p-6 border-b">

        <h1 className="text-2xl font-bold text-blue-600">
          Truck Planner
        </h1>

      </div>

      <div className="p-4 space-y-2">

        {menuItems.map((item) => {

          const Icon = item.icon;

          return (
            <button
              key={item.name}
              className="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-slate-100 transition"
            >
              <Icon size={20} />

              <span>{item.name}</span>
            </button>
          );
        })}
      </div>
    </aside>
  );
}