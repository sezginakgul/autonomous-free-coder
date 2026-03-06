function Cart({ cart, increaseQty, decreaseQty }) {
  return (
    <div className="bg-white shadow-md rounded-xl p-4">
      <h2 className="text-lg font-bold mb-4">Sepetim</h2>
      <ul>
        {cart.map((item) => (
          <li key={item.id} className="py-2 px-4 border-b border-slate-200">
            <span className="mr-2">{item.name}</span>
            <span className="mr-2">x{item.qty}</span>
            <span className="mr-2">{item.price * item.qty} TL</span>
            <button className="text-lg font-bold mr-2" onClick={() => decreaseQty(item.id)}>
              -
            </button>
            <button className="text-lg font-bold" onClick={() => increaseQty(item.id)}>
              +
            </button>
          </li>
        ))}
      </ul>
      <p className="text-lg font-bold mt-4">Toplam Tutar: {cart.reduce((acc, item) => acc + item.price * item.qty, 0)} TL</p>
      <button className="bg-slate-900 text-white py-2 px-4 rounded-xl mt-4">Ödeme Yap</button>
    </div>
  );
}

export default Cart;