import React, { useState } from 'react';

const Calculator = () => {
  const [num1, setNum1] = useState(0);
  const [num2, setNum2] = useState(0);
  const [result, setResult] = useState(0);
  const [operation, setOperation] = useState('+');

  const handleNum1Change = (e) => {
    setNum1(parseInt(e.target.value));
  };

  const handleNum2Change = (e) => {
    setNum2(parseInt(e.target.value));
  };

  const handleOperationChange = (e) => {
    setOperation(e.target.value);
  };

  const calculateResult = () => {
    switch (operation) {
      case '+':
        setResult(num1 + num2);
        break;
      case '-':
        setResult(num1 - num2);
        break;
      case '*':
        setResult(num1 * num2);
        break;
      case '/':
        if (num2 !== 0) {
          setResult(num1 / num2);
        } else {
          setResult('Hata: Sıfıra bölünme');
        }
        break;
      default:
        setResult(0);
    }
  };

  return (
    <div>
      <h1>Hesap Makinesi</h1>
      <input
        type="number"
        value={num1}
        onChange={handleNum1Change}
        placeholder="1. Sayı"
      />
      <select value={operation} onChange={handleOperationChange}>
        <option value="+">+</option>
        <option value="-">-</option>
        <option value="*">*</option>
        <option value="/">/</option>
      </select>
      <input
        type="number"
        value={num2}
        onChange={handleNum2Change}
        placeholder="2. Sayı"
      />
      <button onClick={calculateResult}>=</button>
      <p>Sonuç: {result}</p>
    </div>
  );
};

export default Calculator;