import React, { useEffect } from 'react';
import 'maplibre-gl/dist/maplibre-gl.css';
import maplibregl from 'maplibre-gl';

const MapComponent: React.FC = () => {
  useEffect(() => {
    const map = new maplibregl.Map({
      container: 'map',
      style: 'https://api.maptiler.com/maps/streets/style.json?key=get_your_own_OpIi9ZULNHzrESv6T2vL',
      center: [121.2, 38.9],
      zoom: 8
    });

    new maplibregl.Marker()
      .setLngLat([121.2, 38.9])
      .addTo(map);
  }, []);

  return <div id="map" style={{ height: '100%', width: '100%' }}></div>;
};

export default MapComponent;
