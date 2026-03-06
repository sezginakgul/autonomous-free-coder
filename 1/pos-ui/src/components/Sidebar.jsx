import { FiChevronRight } from 'lucide-react';

function Sidebar({ categories, selectedCategory, setSelectedCategory }) {
  return (
    <div className="h-screen bg-slate-100 p-4 rounded-xl">
      <h2 className="text-lg font-bold mb-4">Kategoriler</h2>
      <ul>
        {categories.map((category) => (
          <li
            key={category}
            className={`py-2 px-4 hover:bg-slate-200 ${selectedCategory === category ? 'bg-slate-200' : ''} rounded-xl`}
            onClick={() => setSelectedCategory(category)}
          >
            <span className="mr-2">{category}</span>
            <FiChevronRight size={16} />
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Sidebar;