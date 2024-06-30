import React from "react";
import EntryForm from "./components/EntryForm";
import MapComponent from "./components/MapComponent";
import "./App.css";
import Menu from "./components/Menu";

const App: React.FC = () => {
  const user = {
    name: "Mac Rogers",
    email: "macrogers@email.com",
    phone: "04123456789"
  };

  return (
    <div className="App">
          <Menu />
          {/* <h1>EZPark</h1> */}
          {/* <EntryForm /> */}
          
        <MapComponent />

    </div>
  );
};

export default App;
