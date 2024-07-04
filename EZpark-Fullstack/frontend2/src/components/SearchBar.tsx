import React, { useState, ChangeEvent, KeyboardEvent } from 'react';
import { FaSearch } from "react-icons/fa";

const SearchBar: React.FC = () => {
  const [input, setInput] = useState<string>('');

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    setInput(event.target.value);
  };

  const handleKeyPress = async (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      console.log(input);
      const response = await fetch('http://localhost:8000/convert-ip', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          "location": input,
        }),
      });
      const data = await response.json();
      console.log(data); // Log the response data
      //setInput(''); // Uncomment this line if you want to clear the search bar after sending the request
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
        onKeyDown={handleKeyPress}
      />
    </div>
  );
};

export default SearchBar;

