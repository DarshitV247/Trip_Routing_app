import Dashboard from "./pages/Dashboard";
import { Toaster, toast } from "react-hot-toast";

function App() {
  return (
    <>
      <Toaster
        position="top-right"
        gutter={12}
        toastOptions={{
          duration: 5000,

          style: {
            minWidth: "500px",
            minHeight: "80px",
            padding: "20px 24px",
            fontSize: "16px",
            fontWeight: "600",
            borderRadius: "14px",
            boxShadow: "0 10px 25px rgba(0,0,0,0.15)",
          },

          success: {
            style: {
              background: "#16a34a",
              color: "#ffffff",
            },
            iconTheme: {
              primary: "#ffffff",
              secondary: "#16a34a",
            },
          },

          error: {
            style: {
              background: "#dc2626",
              color: "#ffffff",
            },
            iconTheme: {
              primary: "#ffffff",
              secondary: "#dc2626",
            },
          },
        }}
      />

      <Dashboard />
    </>
  );
}

export default App;