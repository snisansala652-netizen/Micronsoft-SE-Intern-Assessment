import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import Receipt from './Receipt'; // Make sure Receipt.jsx exists in your src folder

/**
 * Main application component for the POS System.
 * Optimized for transactional integrity and professional UI.
 */
function App() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showReceipt, setShowReceipt] = useState(false); // State to control Receipt visibility
  const [lastTransaction, setLastTransaction] = useState(null); // Stores data for the printed receipt

  // Initial load - Mocking product data for the assessment
  useEffect(() => {
    setProducts([
      { id: 1, name: 'Smart Watch Series 7', price: 12000, stock: 15 },
      { id: 2, name: 'Bluetooth Headphones', price: 4500, stock: 24 },
      { id: 3, name: 'Mechanical Keyboard', price: 8900, stock: 10 },
      { id: 4, name: 'Gaming Mouse', price: 3200, stock: 40 },
    ]);
  }, []);

  // Adds a selected product to the cart state
  const addToCart = (product) => {
    setCart([...cart, product]);
  };

  // Calculates the total price of all items currently in the cart
  const totalPrice = cart.reduce((sum, item) => sum + item.price, 0);

  /**
   * Processes the entire cart in one request to ensure atomicity.
   * On success, it triggers the Thermal Receipt display.
   */
  const handleCheckout = async () => {
    if (cart.length === 0) return;

    setIsProcessing(true);
    try {
      // POST request to the atomic checkout endpoint in Django
      const response = await axios.post('http://127.0.0.1:8000/api/checkout/', {
        items: cart
      });

      // Save transaction details and clear the cart
      setLastTransaction({
        items: [...cart],
        total: totalPrice,
        transactionId: response.data.transaction_id || "TRX-" + Math.floor(Math.random() * 9999)
      });

      setCart([]);
      
      setShowReceipt(true); // Show the Receipt Component
      alert("✅ Checkout Successful!"); // Adds the alert back
    } catch (error) {
      // Handle server-side errors (e.g., Insufficient stock)
      const errorMessage = error.response?.data?.error || "Transaction failed. Please try again.";
      alert("❌ Checkout Error: " + errorMessage);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="App">
      {/* Professional Header Section */}
      <header className="header">
        <div className="header-content">
          <h1>Retail <span style={{ color: '#2563eb' }}>POS</span></h1>
          <div className="status-indicator">
            <span className="dot"></span> System Operational
          </div>
        </div>
        
      </header>

      <main className="main-container">
        <div className="pos-grid">
          {/* Inventory Listing Section */}
          <section className="inventory-section">
            <div className="section-header">
              <h2>Inventory Items</h2>
              <span className="count-badge">{products.length} Products Available</span>
            </div>
            
            <div className="products-grid">
              {products.map((product) => (
                <div key={product.id} className="product-card">
                  <div className="card-body">
                    <h3>{product.name}</h3>
                    <span className="price">Rs. {product.price.toLocaleString()}</span>
                    <p className="stock-info">Available Stock: <strong>{product.stock}</strong></p>
                  </div>
                  <button 
                    className="add-btn" 
                    onClick={() => addToCart(product)}
                    disabled={product.stock === 0}
                  >
                    {product.stock === 0 ? "Out of Stock" : "Add to Bill"}
                  </button>
                </div>
              ))}
            </div>
          </section>

          {/* Billing / Cart Sidebar */}
          <aside className="billing-sidebar">
            <div className="sidebar-header">
              <h2>Current Bill</h2>
              <button 
                className="clear-btn" 
                onClick={() => setCart([])} 
                disabled={cart.length === 0}
              >
                Clear
              </button>
            </div>

            <div className="cart-list">
              {cart.length === 0 ? (
                <div className="empty-cart">
                  <p>No items selected in the current session.</p>
                </div>
              ) : (
                cart.map((item, index) => (
                  <div key={index} className="cart-item">
                    <span className="item-name">{item.name}</span>
                    <span className="item-price">Rs. {item.price.toLocaleString()}</span>
                  </div>
                ))
              )}
            </div>

            {/* Checkout Summary Footer */}
            <div className="total-container">
              <div className="total-row grand-total">
                <span>Total Amount</span>
                <span>Rs. {totalPrice.toLocaleString()}</span>
              </div>
              
              <button 
                className="checkout-btn" 
                onClick={handleCheckout} 
                disabled={isProcessing || cart.length === 0}
              >
                {isProcessing ? "Processing Atomic Transaction..." : "Complete Order"}
              </button>
              <p className="security-note">🔒 Secured by Django transaction.atomic</p>
            </div>
          </aside>
        </div>
      </main>

      {/* Professional Receipt Modal (Triggered after checkout) */}
      {showReceipt && (
        <div className="receipt-overlay">
          <div className="receipt-modal-inner">
            <button className="close-btn" onClick={() => setShowReceipt(false)}>× Close</button>
            <Receipt 
              cart={lastTransaction.items} 
              total={lastTransaction.total} 
              transactionId={lastTransaction.transactionId}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;