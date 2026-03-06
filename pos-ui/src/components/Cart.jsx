import { useState } from "react";

const Cart = ({ cartProducts, increaseQuantity, decreaseQuantity }) => {
  const total = cartProducts.reduce(
    (acc, product) => acc + product.price * product.quantity,
    0
  );

  return (
    <div className="flex flex-col gap-4 p-4">
      <h2 className="text-lg">Sepet</h2>
      {cartProducts.map((product) => (
        <div key={product.id} className="flex justify-between">
          <span>{product.name}</span>
          <span>
            {product.quantity} x {product.price} TL
          </span>
          <button
            className="px-2 py-1 rounded-xl hover:shadow-md"
            onClick={() => increaseQuantity(product)}
          >
            +
          </button>
          <button
            className="px-2 py-1 rounded-xl hover:shadow-md"
            onClick={() => decreaseQuantity(product)}
          >
            -
          </button>
        </div>
      ))}
      <p className="text-slate-500">Toplam: {total} TL</p>
      <button className="px-4 py-2 rounded-xl bg-slate-200 hover:shadow-md">
        Ödeme Yap
      </button>
    </div>
  );
};

export default Cart;