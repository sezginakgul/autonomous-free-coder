import React from "react";
import { useState } from "react";

const ProductGrid = ({ products, onAddToCart }) => {
  return (
    <div className="grid grid-cols-3 gap-4">
      {products.map((product) => (
        <div
          key={product.id}
          className="bg-white shadow-sm rounded-xl p-4 cursor-pointer"
          onClick={() => onAddToCart(product)}
        >
          <img src={product.image} alt={product.name} />
          <h2 className="text-lg">{product.name}</h2>
          <p className="text-gray-500">{product.price} TL</p>
        </div>
      ))}
    </div>
  );
};

export default ProductGrid;