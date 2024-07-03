import React, { useState, useEffect } from "react";
import "./SearchBar";
import Logo from "../img/EZpark-logo-nobg.png";
import { AiFillSetting } from "react-icons/ai";
import axios from 'axios';
import SearchBar from "./SearchBar";

const Menu: React.FC = () => {
    return (
        <menu>
            <div className="logo">
                <ul> 
                    <li>
                        <a href="http://localhost:3000/"><img src={Logo} alt="EZpark Logo" /></a> 
                    </li>
                </ul>
            </div>
            <SearchBar /> 
            <ul id="mainMenu">
                <li>
                    <Icon icon={<AiFillSetting />} className="settings" /> 
                </li>
            </ul>
        </menu>
    );
}

interface IconProps {
    icon: React.ReactNode;
    className?: string;
}

const Icon: React.FC<IconProps> = ({ icon, className }) => {
    return (
        <li className={className}>
            <a href="#">{icon}</a>
        </li>
    );
}

export default Menu;



// interface Item {
//     id: number;
//     name: string;
// }

// const EntryForm: React.FC = () => {
//     const [items, setItems] = useState<Item[]>([]);
//     const [name, setName] = useState<string>("");

//     useEffect(() => {
//         fetchItems();
//     }, []);

//     const fetchItems = async () => {
//         const response = await axios.get<Item[]>('http://localhost:8000/items/');
//         setItems(response.data);
//     };

//     const addItem = async () => {
//         if (name) {
//             try {
//                 await axios.post('http://localhost:8000/items/', { name }, {
//                     headers: {
//                         'Content-Type': 'application/json'
//                     }
//                 });
//                 setName("");
//                 fetchItems();
//             } catch (error) {
//                 console.error("There was an error adding the item!", error);
//             }
//         }
//     };

//     return (
//         <div className="entry-form">
//             <input
//                 type="text"
//                 value={name}
//                 onChange={(e) => setName(e.target.value)}
//                 placeholder="Enter park coords"
//             />
//             <button onClick={addItem}>Add Coordinates</button>
            
//         </div>
//     );
// };



// import React from "react"; 
// import Logo from "../img/EZpark-logo-nobg.png";
// import { AiFillSetting } from "react-icons/ai";
// import SearchBar from "./SearchBar";

// const Menu: React.FC = () => {
//   return (
//     <div className="menu">
//       <img src={Logo} alt="EZpark Logo" />
//       <div className="search">
//         <SearchBar />
//       </div>
//       <div className="settings">
//         <Icon icon={<AiFillSetting />} className="settings" />
//       </div>
//     </div>
//   );
// };

// interface IconProps {
//   icon: React.ReactNode;
//   className?: string;
// }

// const Icon: React.FC<IconProps> = ({ icon, className }) => {
//   return (
//     <li className={className}>
//       <a href="#">{icon}</a>
//     </li>
//   );
// };

// export default Menu;
