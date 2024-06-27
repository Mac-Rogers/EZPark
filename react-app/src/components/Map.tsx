// Map.tsx
import React, { useEffect } from 'react';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

const Map: React.FC = () => {
  useEffect(() => {
    const map = new maplibregl.Map({
      container: 'map',
      style: 'https://api.maptiler.com/maps/streets/style.json?key=get_your_own_OpIi9ZULNHzrESv6T2vL',
      center: [12.550343, 55.665957],
      zoom: 8
    });

    new maplibregl.Marker()
      .setLngLat([12.550343, 55.665957])
      .addTo(map);
  }, []);

  return <div id="map" style={{ width: '100%', height: '100%' }} />;
};

export default Map;
