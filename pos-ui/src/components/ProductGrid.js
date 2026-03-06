import React from "react";

interface ProductGridProps {
  selectedCategory: string;
  products: any[];
  onAddToCart: (product: any) => void;
}

const ProductGrid: React.FC<ProductGridProps> = ({
  selectedCategory,
  products,
  onAddToCart,
}) => {
  return (
    <div className="grid grid-cols-1 gap-4">
      {products
        .filter((product) => product.category === selectedCategory)
        .map((product) => (
          <div
            key={product.id}
            className="bg-white p-4 rounded-xl shadow-sm hover:shadow-md"
          >
            <h2 className="text-lg font-bold mb-2">{product.name}</h2>
            <p className="text-gray-600 mb-4">{product.price} TL</p>
            <button
              className="py-2 px-4 rounded-xl bg-gray-200 hover:bg-gray-300"
              onClick={() => onAddToCart(product)}
            >
              Sepete Ekle
            </button>
          </div>
        ))}
    </div>
  );
};

export default ProductGrid;