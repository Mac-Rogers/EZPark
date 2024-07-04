import React from 'react';
import { FaLocationArrow } from 'react-icons/fa';

const LocationButton: React.FC = () => {
    const handleClick = () => {
        console.log('Location icon clicked');
    };

    return (
        <button onClick={handleClick} className="location-button">
            <div className="location">
                <FaLocationArrow />
            </div>
        </button>
    );
};

export default LocationButton;
