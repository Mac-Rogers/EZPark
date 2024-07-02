import React, { useState, ChangeEvent, KeyboardEvent } from 'react';
import { FaSearch } from "react-icons/fa";

const SearchBar: React.FC = () => {
  const [input, setInput] = useState<string>('');

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    setInput(event.target.value);
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      console.log(input);
      //setInput(''); //clears the search bar 
    }
  };

  return (
    <div className="input-wrapper">
        <FaSearch />
      <input
        type="text"
        placeholder="Type to search..."
        value={input}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
      />
    </div>
  );
};

export default SearchBar;

