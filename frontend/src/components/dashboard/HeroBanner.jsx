import truck from "../../assets/truck.png";
import tree from "../../assets/tree.png";

export default function HeroBanner() {
  return (
    <section className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-blue-700 via-blue-600 to-indigo-600 min-h-[340px] md:min-h-[380px]">

      {/* Trees */}
      <div className="absolute bottom-8 left-0 w-full h-full overflow-hidden pointer-events-none">

        <img
          src={tree}
          alt=""
          className="absolute left-0 bottom-0 tree-1 h-40 md:h-56 opacity-25"
        />

        <img
          src={tree}
          alt=""
          className="absolute left-0 bottom-0 tree-2 h-52 md:h-72 opacity-25"
        />

        <img
          src={tree}
          alt=""
          className="absolute left-0 bottom-0 tree-3 h-48 md:h-64 opacity-25"
        />

        <img
          src={tree}
          alt=""
          className="absolute left-0 bottom-0 tree-4 h-60 md:h-80 opacity-25"
        />

      </div>

      {/* Road */}
      <div className="absolute bottom-0 left-0 w-full h-8 bg-slate-900 z-10">

        <div className="road-line h-1 mt-3"></div>

      </div>

      {/* Content */}
      <div className="relative z-20 flex h-full items-center px-6 md:px-10 py-8 md:py-10">

        {/* Left Content */}
        <div className="max-w-2xl text-white relative z-50">

          <p className="uppercase tracking-[3px] text-blue-100 text-xs md:text-sm mb-4">
            Logistics Management Platform
          </p>

          <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold leading-tight mb-5">
            Truck Routing & HOS Planner
          </h1>

          <p className="text-blue-100 text-base md:text-lg leading-relaxed max-w-xl">
            Plan optimized routes, manage driver hours,
            visualize stops, calculate fuel breaks and
            generate FMCSA compliant log sheets.
          </p>

          <button
            className="
              relative
              z-50
              mt-8
              px-6
              py-3
              bg-white
              text-blue-700
              rounded-xl
              font-semibold
              shadow-lg
              hover:scale-105
              transition
            "
          >
            Create New Trip
          </button>

        </div>

      </div>

      {/* Truck */}
      <div
        className="
    hidden
    md:block
    absolute
    bottom-[-55px]
    right-12
    z-30
  " 
      >
        <img
          src={truck}
          alt="Truck"
          className="
            w-[220px]
            sm:w-[240px]
            md:w-[340px]
            xl:w-[430px]
            truck
          "
        />
      </div>

    </section>
  );
}