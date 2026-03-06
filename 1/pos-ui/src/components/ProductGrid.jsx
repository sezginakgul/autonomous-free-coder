function ProductGrid({ products, addToCart }) {
  return (
    <div className="grid grid-cols-3 gap-4">
      {products.map((product) => (
        <div
          key={product.id}
          className="bg-white shadow-sm hover:shadow-md rounded-xl p-4"
          onClick={() => addToCart(product)}
        >
          <img src={product.image} alt={product.name} className="w-full h-48 object-cover mb-4" />
          <h3 className="text-lg font-bold mb-2">{product.name}</h3>
          <p className="text-lg font-bold">{product.price} TL</p>
        </div>
      ))}
    </div>
  );
}

export default ProductGrid;