import React from 'react';

/**
 * Receipt Component optimized for 80mm Thermal Printers.
 * Uses CSS Media Queries to handle print-only visibility.
 */
const Receipt = ({ cart, total, transactionId }) => {
  
  // Triggers the browser's native print dialog
  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="receipt-wrapper">
      {/* Inline styles for thermal printer compatibility */}
      <style>{`
        /* Styles applied only during printing */
        @media print {
          body * { visibility: hidden; } /* Hide everything else on the page */
          .thermal-receipt, .thermal-receipt * { visibility: visible; } /* Show only receipt */
          .thermal-receipt { 
            position: absolute; 
            left: 0; 
            top: 0; 
            width: 80mm; /* Standard thermal paper width */
          }
          .no-print-btn { display: none; } /* Hide the print button on the actual paper */
        }

        /* General UI styles for the receipt preview */
        .thermal-receipt {
          width: 80mm;
          padding: 10px;
          background: #fff;
          font-family: 'Courier New', Courier, monospace; /* Classic receipt font */
          border: 1px solid #eee;
          margin: 0 auto;
          color: #000;
        }
        .center-text { text-align: center; }
        .dashed-line { border-bottom: 1px dashed #000; margin: 10px 0; }
        .receipt-table { width: 100%; font-size: 13px; border-collapse: collapse; }
        .receipt-table td { padding: 5px 0; }
        .total-section { font-weight: bold; font-size: 16px; margin-top: 10px; }
      `}</style>

      {/* The Printable Area */}
      <div className="thermal-receipt">
        <div className="center-text">
          <h2 style={{ margin: '0' }}>RETAIL POS</h2>
          <p style={{ fontSize: '12px' }}>Professional Assessment Project</p>
          <div className="dashed-line"></div>
          <p style={{ fontSize: '11px' }}>Date: {new Date().toLocaleString()}</p>
          {transactionId && <p style={{ fontSize: '11px' }}>Trans ID: {transactionId}</p>}
        </div>

        <table className="receipt-table">
          <thead>
            <tr style={{ borderBottom: '1px solid #000' }}>
              <th align="left">Description</th>
              <th align="right">Amount</th>
            </tr>
          </thead>
          <tbody>
            {cart.map((item, index) => (
              <tr key={index}>
                <td>{item.name}</td>
                <td align="right">{item.price.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>

        <div className="dashed-line"></div>

        <div className="total-section">
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>GRAND TOTAL</span>
            <span>Rs. {total.toLocaleString()}</span>
          </div>
        </div>

        <div className="center-text" style={{ marginTop: '20px', fontSize: '12px' }}>
          <p>*** THANK YOU ***</p>
          <p>Please come again!</p>
        </div>
      </div>

      {/* Print Action Button - Hidden during actual printing */}
      <div className="center-text no-print-btn" style={{ marginTop: '20px' }}>
        <button 
          onClick={handlePrint}
          style={{
            padding: '10px 25px',
            backgroundColor: '#2563eb',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontWeight: 'bold'
          }}
        >
          🖨️ Print to Thermal Printer
        </button>
      </div>
    </div>
  );
};

export default Receipt;