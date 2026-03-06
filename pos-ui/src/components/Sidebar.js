import React from "react";
import { FiCoffee } from "lucide-react";

interface SidebarProps {
  selectedCategory: string;
  onSelectCategory: (category: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({
  selectedCategory,
  onSelectCategory,
}) => {
  return (
    <div className="w-64 bg-white p-4 rounded-xl shadow-sm">
      <h2 className="text-lg font-bold mb-2">Kategoriler</h2>
      <ul>
        <li>
          <button
            className={`py-2 px-4 rounded-xl ${
              selectedCategory === "Kahveler"
                ? "bg-gray-200 text-gray-900"
                : "hover:bg-gray-100"
            }`}
            onClick={() => onSelectCategory("Kahveler")}
          >
            <FiCoffee className="mr-2" />
            Kahveler
          </button>
        </li>
        <li>
          <button
            className={`py-2 px-4 rounded-xl ${
              selectedCategory === "Tatlılar"
                ? "bg-gray-200 text-gray-900"
                : "hover:bg-gray-100"
            }`}
            onClick={() => onSelectCategory("Tatlılar")}
          >
            Tatlılar
          </button>
        </li>
        <li>
          <button
            className={`py-2 px-4 rounded-xl ${
              selectedCategory === "Soğuk İçecekler"
                ? "bg-gray-200 text-gray-900"
                : "hover:bg-gray-100"
            }`}
            onClick={() => onSelectCategory("Soğuk İçecekler")}
          >
            Soğuk İçecekler
          </button>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;