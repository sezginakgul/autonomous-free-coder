import React from "react";

interface CartProps {
  cart: any[];
  onRemoveFromCart: (product: any) => void;
}

const Cart: React.FC<CartProps> = ({ cart, onRemoveFromCart }) => {
  return (
    <div className="w-64 bg-white p-4 rounded-xl shadow-sm">
      <h2 className="text-lg font-bold mb-2">Sepet</h2>
      <ul>
        {cart.map((product) => (
          <li key={product.id} className="py-2">
            {product.name} x {product.quantity}
            <button
              className="py-1 px-2 rounded-xl bg-gray-200 hover:bg-gray-300 ml-2"
              onClick={() => onRemoveFromCart(product)}
            >
              Kaldır
            </button>
          </li>
        ))}
      </ul>
      <p className="text-lg font-bold mt-4">Toplam: {cart.reduce((acc, product) => acc + product.price * product.quantity, 0)} TL</p>
    </div>
  );
};

export default Cart;