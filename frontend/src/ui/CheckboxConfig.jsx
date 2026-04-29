import React from "react";

const CheckboxConfig = ({ checked, onChange, label }) => {
  return (
    <label className="relative flex items-center gap-3 cursor-pointer select-none">

      <input
        type="checkbox"
        checked={checked}
        onChange={onChange}
        className="absolute opacity-0"
      />

      
      <div
        className={`
          w-[20px] h-[20px]
          border-2 border-[#323232]
          rounded-[5px]
          shadow-[2px_2px_0_#323232]
          transition-all duration-300
          ${checked ? "bg-blue-500" : "bg-[#ccc]"}
          relative
        `}
      >
        
        {checked && (
          <div className="absolute top-[0px] left-[4px] w-[7px] h-[15px] border-white border-r-[2.5px] border-b-[2.5px] rotate-45" />
        )}
      </div>

      <span className="text-white">{label}</span>
    </label>
  );
};

export default CheckboxConfig;