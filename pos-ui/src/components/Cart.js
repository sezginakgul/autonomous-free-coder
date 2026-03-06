import React from "react";
import { useState } from "react";

const Cart = ({ cart, onRemoveFromCart, onIncreaseQuantity, onDecreaseQuantity }) => {
  const [total, setTotal] = useState(0);

  React.useEffect(() => {
    setTotal(
      cart.reduce((acc, product) => acc + product.price * product.quantity, 0)
    );
  }, [cart]);

  return (
    <div className="h-screen w-64 bg-slate-100 p-4">
      <h2 className="text-lg">Sepet</h2>
      <ul>
        {cart.map((product) => (
          <li key={product.id} className="py-2 px-4 border-b border-gray-200">
            <div className="flex justify-between">
              <span>{product.name}</span>
              <span>
                {product.quantity} x {product.price} TL
              </span>
            </div>
            <div className="flex justify-between">
              <button
                className="text-gray-500 hover:text-gray-900"
                onClick={() => onDecreaseQuantity(product)}
              >
                -
              </button>
              <span className="text-gray-500">{product.quantity}</span>
              <button
                className="text-gray-500 hover:text-gray-900"
                onClick={() => onIncreaseQuantity(product)}
              >
                +
              </button>
            </div>
          </li>
        ))}
      </ul>
      <p className="text-lg">Toplam: {total} TL</p>
      <button className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-xl">
        Ödeme Yap
      </button>
    </div>
  );
};

export default Cart;