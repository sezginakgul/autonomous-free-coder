import { useState } from "react";
import Sidebar from "./components/Sidebar";
import ProductGrid from "./components/ProductGrid";
import Cart from "./components/Cart";

const App = () => {
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [cartProducts, setCartProducts] = useState([]);
  const [quantity, setQuantity] = useState(1);

  const addProductToCart = (product) => {
    const existingProduct = cartProducts.find(
      (cartProduct) => cartProduct.id === product.id
    );
    if (existingProduct) {
      setCartProducts(
        cartProducts.map((cartProduct) =>
          cartProduct.id === product.id
            ? { ...cartProduct, quantity: cartProduct.quantity + 1 }
            : cartProduct
        )
      );
    } else {
      setCartProducts([...cartProducts, { ...product, quantity: 1 }]);
    }
  };

  const increaseQuantity = (product) => {
    setCartProducts(
      cartProducts.map((cartProduct) =>
        cartProduct.id === product.id
          ? { ...cartProduct, quantity: cartProduct.quantity + 1 }
          : cartProduct
      )
    );
  };

  const decreaseQuantity = (product) => {
    setCartProducts(
      cartProducts.map((cartProduct) =>
        cartProduct.id === product.id
          ? { ...cartProduct, quantity: cartProduct.quantity - 1 }
          : cartProduct
      )
    );
  };

  return (
    <div className="flex flex-col gap-4 p-4">
      <Sidebar setSelectedCategory={setSelectedCategory} />
      <ProductGrid
        selectedCategory={selectedCategory}
        addProductToCart={addProductToCart}
      />
      <Cart
        cartProducts={cartProducts}
        increaseQuantity={increaseQuantity}
        decreaseQuantity={decreaseQuantity}
      />
    </div>
  );
};

export default App;