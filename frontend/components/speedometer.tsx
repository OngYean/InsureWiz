"use client";

import { motion } from "framer-motion";

const Speedometer = ({ value }: { value: number }) => {
  const normalizedValue = Math.max(0, Math.min(100, value));
  const rotation = (normalizedValue / 100) * 180 - 90;

  const getBackgroundColor = (val: number) => {
    if (val < 40) return "bg-red-500";
    if (val < 70) return "bg-yellow-500";
    return "bg-green-500";
  };

  return (
    <div className="relative w-64 h-32 overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-full">
        <div className="absolute bottom-0 left-0 w-full h-[200%] rounded-t-full border-t-[60px] border-l-[60px] border-r-[60px] border-b-0 border-gray-200 dark:border-gray-700"></div>
        <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-4 h-4 bg-white dark:bg-gray-800 rounded-full z-10"></div>
      </div>

      <motion.div
        className="absolute bottom-0 left-1/2 w-1 h-28 origin-bottom"
        animate={{ rotate: rotation }}
        transition={{ type: "spring", stiffness: 260, damping: 20 }}
      >
        <div
          className={`w-full h-full rounded-t-full ${getBackgroundColor(
            normalizedValue
          )}`}
        ></div>
      </motion.div>

      <div className="absolute bottom-2 left-1/2 -translate-x-1/2 text-center">
        <div className="text-3xl font-bold">{normalizedValue.toFixed(0)}%</div>
        <div className="text-sm text-muted-foreground">Confidence</div>
      </div>
    </div>
  );
};

export default Speedometer;
