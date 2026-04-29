import React from "react";

const ButtonConfig = ({ children, onClick, variant = "primary"}) => {

const colors = {
    primary: "bg-emerald-500",
    danger: "bg-red-500",
}

    return (
    <div
      onClick={onClick}
      className={`cursor-pointer select-none border-4 border-black ${colors[variant]} pb-1 active:pb-0 active:translate-y-[6px] transition-all duration-100 w-[100px]`}
    >
      <div className="bg-[#dddddd] border-4 border-white px-2 py-[2px] text-center">
        <span className="text-sm tracking-wide text-black font-semibold">
          {children}
        </span>
      </div>
    </div>
  );

}

export default ButtonConfig