import React from 'react';

interface HapticButtonProps {
  onClick: () => void;
  children: React.ReactNode;
}

const HapticButton: React.FC<HapticButtonProps> = ({ onClick, children }) => {
  const handleTouchStart = () => {
    // Titreşim efektini buraya ekleyebilirsiniz
    console.log('Titreşim başlattı');
  };

  return (
    <button
      type="button"
      onClick={onClick}
      onTouchStart={handleTouchStart}
      className="p-4 bg-orange-500 text-white rounded-lg"
    >
      {children}
    </button>
  );
};

export default HapticButton;