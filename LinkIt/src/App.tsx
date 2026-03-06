import React from 'react';
import HapticButton from './components/HapticButton';

function App() {
  const handleClick = () => {
    console.log('Butona tıklandı');
  };

  return (
    <div className="flex justify-center items-center h-screen">
      <HapticButton onClick={handleClick}>Tıkla</HapticButton>
    </div>
  );
}

export default App;