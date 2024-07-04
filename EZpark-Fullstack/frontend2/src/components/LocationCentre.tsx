// import React from "react";
// import { FaLocationArrow } from "react-icons/fa";

// const LocationCentre = () => {

//     return (
//         <div className="Location">
//             <FaLocationArrow />
//         </div>
//     );
// };

// export default LocationCentre;


import React from "react";
import { FaLocationArrow } from "react-icons/fa";

const LocationCentre: React.FC = () => {

    const handleClick = () => {
        console.log("Icon clicked");
        // Add your logic here
    };

    return (
        <div className="Location">
            <button onClick={handleClick} style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 0 }}>
                <FaLocationArrow size={24} color="black" />
            </button>
        </div>
    );
};

export default LocationCentre;
