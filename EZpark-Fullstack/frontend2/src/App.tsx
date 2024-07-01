import React from "react";
import EntryForm from "./components/EntryForm";
import MapComponent from "./components/MapComponent";
import "./App.css";
import Menu from "./components/Menu";
import Footer from "./components/Footer";

const App: React.FC = () => {
  return (
    <div className="App">
      <Menu />
      <MapComponent />
      <Footer />

    </div>
  );
};

export default App;
