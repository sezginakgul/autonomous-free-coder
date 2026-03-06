import { useState } from "react";
import { FiCoffee, FiCake, FiGlass } from "lucide-react";

const categories = [
  { id: 1, name: "Kahveler", icon: <FiCoffee size={20} /> },
  { id: 2, name: "Tatlılar", icon: <FiCake size={20} /> },
  { id: 3, name: "Soğuk İçecekler", icon: <FiGlass size={20} /> },
];

const Sidebar = ({ setSelectedCategory }) => {
  const [selectedCategory, setSelectedCategoryState] = useState(null);

  const handleCategoryClick = (category) => {
    setSelectedCategoryState(category);
    setSelectedCategory(category);
  };

  return (
    <div className="flex flex-col gap-4 p-4">
      {categories.map((category) => (
        <button
          key={category.id}
          className={`flex items-center gap-2 p-2 rounded-xl hover:shadow-md ${
            selectedCategory === category ? "bg-slate-200" : ""
          }`}
          onClick={() => handleCategoryClick(category)}
        >
          {category.icon}
          <span>{category.name}</span>
        </button>
      ))}
    </div>
  );
};

export default Sidebar;