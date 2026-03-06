import React from "react";
import { FiCoffee, FiCake, FiGlass } from "lucide-react";

const Sidebar = ({ onSelectCategory, selectedCategory }) => {
  return (
    <div className="h-screen w-64 bg-slate-100 p-4">
      <ul>
        <li
          className={`py-2 px-4 cursor-pointer rounded-xl ${
            selectedCategory === "Kahveler" ? "bg-slate-200" : ""
          }`}
          onClick={() => onSelectCategory("Kahveler")}
        >
          <FiCoffee size={20} className="mr-2" />
          Kahveler
        </li>
        <li
          className={`py-2 px-4 cursor-pointer rounded-xl ${
            selectedCategory === "Tatlılar" ? "bg-slate-200" : ""
          }`}
          onClick={() => onSelectCategory("Tatlılar")}
        >
          <FiCake size={20} className="mr-2" />
          Tatlılar
        </li>
        <li
          className={`py-2 px-4 cursor-pointer rounded-xl ${
            selectedCategory === "Soğuk İçecekler" ? "bg-slate-200" : ""
          }`}
          onClick={() => onSelectCategory("Soğuk İçecekler")}
        >
          <FiGlass size={20} className="mr-2" />
          Soğuk İçecekler
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;