import React, { FC, ChangeEvent } from "react";
import { FaSearch } from "react-icons/fa";

const SearchBar: FC = () => {
    const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
        // Handle the input change if needed
    };

    return (
        <div className="InputWrapper">
            <FaSearch />
            <input 
                type="text"
                placeholder="Type to find parking"
                onChange={handleInputChange}
                aria-label="Search for parking"
            />
        </div>
    );
};

export default SearchBar;
