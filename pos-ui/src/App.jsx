import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import ProductGrid from "./components/ProductGrid";
import Cart from "./components/Cart";
import { mockMenu } from "./data/mockMenu";

function App() {
  const [selectedCategory, setSelectedCategory] = useState("Kahveler");
  const [cart, setCart] = useState([]);

  const handleSelectCategory = (category: string) => {
    setSelectedCategory(category);
  };

  const handleAddToCart = (product: any) => {
    const existingProduct = cart.find((item) => item.id === product.id);
    if (existingProduct) {
      setCart(
        cart.map((item) =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        )
      );
    } else {
      setCart([...cart, { ...product, quantity: 1 }]);
    }
  };

  const handleRemoveFromCart = (product: any) => {
    setCart(
      cart.filter((item) => item.id !== product.id)
    );
  };

  return (
    <div className="grid grid-cols-3 gap-4 p-4">
      <Sidebar
        selectedCategory={selectedCategory}
        onSelectCategory={handleSelectCategory}
      />
      <ProductGrid
        selectedCategory={selectedCategory}
        products={mockMenu}
        onAddToCart={handleAddToCart}
      />
      <Cart cart={cart} onRemoveFromCart={handleRemoveFromCart} />
    </div>
  );
}

export default App;