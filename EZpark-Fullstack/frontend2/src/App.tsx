import React from "react";
import EntryForm from "./components/EntryForm";
import MapComponent from "./components/MapComponent";
import "./App.css";
import Menu from "./components/Menu";

const App: React.FC = () => {
  return (
    <div className="App">
      {/* <div className="SearchBar">
        <div>SearchBar</div>
        <div>SearchResults</div>
      </div> */}
          <Menu />
          {/* <h1>EZPark</h1> */}
          {/* <EntryForm /> */}
          
        <MapComponent />

    </div>
  );
};

export default App;
