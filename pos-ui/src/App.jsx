import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import ProductGrid from "./components/ProductGrid";
import Cart from "./components/Cart";
import { mockMenu } from "./data/mockMenu";

function App() {
  const [selectedCategory, setSelectedCategory] = useState("Kahveler");
  const [cart, setCart] = useState([]);
  const [products, setProducts] = useState(mockMenu);

  const onSelectCategory = (category) => {
    setSelectedCategory(category);
    setProducts(mockMenu.filter((product) => product.category === category));
  };

  const onAddToCart = (product) => {
    const existingProduct = cart.find((item) => item.id === product.id);
    if (existingProduct) {
      setCart(
        cart.map((item) =>
          item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
        )
      );
    } else {
      setCart([...cart, { ...product, quantity: 1 }]);
    }
  };

  const onRemoveFromCart = (product) => {
    setCart(cart.filter((item) => item.id !== product.id));
  };

  const onIncreaseQuantity = (product) => {
    setCart(
      cart.map((item) =>
        item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
      )
    );
  };

  const onDecreaseQuantity = (product) => {
    if (product.quantity > 1) {
      setCart(
        cart.map((item) =>
          item.id === product.id ? { ...item, quantity: item.quantity - 1 } : item
        )
      );
    } else {
      onRemoveFromCart(product);
    }
  };

  return (
    <div className="flex h-screen">
      <Sidebar
        onSelectCategory={onSelectCategory}
        selectedCategory={selectedCategory}
      />
      <ProductGrid products={products} onAddToCart={onAddToCart} />
      <Cart
        cart={cart}
        onRemoveFromCart={onRemoveFromCart}
        onIncreaseQuantity={onIncreaseQuantity}
        onDecreaseQuantity={onDecreaseQuantity}
      />
    </div>
  );
}

export default App;