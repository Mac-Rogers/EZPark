import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Item {
    id: number;
    name: string;
}

const EntryForm: React.FC = () => {
    const [items, setItems] = useState<Item[]>([]);
    const [name, setName] = useState<string>("");

    useEffect(() => {
        fetchItems();
    }, []);

    const fetchItems = async () => {
        const response = await axios.get<Item[]>('http://localhost:8000/items/');
        setItems(response.data);
    };

    const addItem = async () => {
        if (name) {
            try {
                await axios.post('http://localhost:8000/items/', { name }, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                setName("");
                fetchItems();
            } catch (error) {
                console.error("There was an error adding the item!", error);
            }
        }
    };

    return (
        <div>
            <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter park coords"
            />
            <button onClick={addItem}>Add Coordinates</button>
            <ul>
                {items.map((item) => (
                    <li key={item.id}>{item.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default EntryForm;
