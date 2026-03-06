import { useState } from "react";
import mockMenu from "../data/mockMenu";

const ProductGrid = ({ selectedCategory, addProductToCart }) => {
  const filteredProducts = mockMenu.filter(
    (product) => product.category === selectedCategory.name
  );

  return (
    <div className="grid grid-cols-1 gap-4 p-4">
      {filteredProducts.map((product) => (
        <div
          key={product.id}
          className="flex flex-col gap-2 p-4 rounded-xl shadow-sm hover:shadow-md"
          onClick={() => addProductToCart(product)}
        >
          <img src={product.image} alt={product.name} className="w-full" />
          <h2 className="text-lg">{product.name}</h2>
          <p className="text-slate-500">{product.price} TL</p>
        </div>
      ))}
    </div>
  );
};

export default ProductGrid;