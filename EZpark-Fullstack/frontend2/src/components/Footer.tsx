import React from 'react';
import { FaLocationArrow } from 'react-icons/fa';

const Footer: React.FC = () => {
  const handleClick = () => {
    console.log('Find Me A Park button clicked');
  };

  return (
    <div className="footer">
      <button className="find-park" onClick={handleClick}>Find Me A Park</button>
      <div className="location">
        <FaLocationArrow />
      </div>
    </div>
  );
};

export default Footer;
