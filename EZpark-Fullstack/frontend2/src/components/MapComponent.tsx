import React, { useEffect, useState } from 'react';
import 'maplibre-gl/dist/maplibre-gl.css';
import maplibregl from 'maplibre-gl';

const MapComponent: React.FC = () => {
  const [coordinates, setCoordinates] = useState<[number, number] | null>(null);
  const [markerCoordinates, setMarkerCoordinates] = useState<[number, number][]>([]);
  const [map, setMap] = useState<maplibregl.Map | null>(null);

  useEffect(() => {
    const fetchCoordinates = async () => {
      try {
        const response = await fetch('http://localhost:8000/gps-coordinates');
        const data = await response.json();
        setCoordinates([data.longitude, data.latitude]);
        console.log([data.longitude, data.latitude])
        const response2 = await fetch('http://localhost:8000/items');
        const data2 = await response2.json();
        const coords = data2.map((item: { latitude: number, longitude: number }) => [item.longitude, item.latitude]);
        setMarkerCoordinates(coords);
      } catch (error) {
        console.error('Error fetching GPS coordinates:', error);
      }
    };

    fetchCoordinates();
  }, []);

  useEffect(() => {
    if (coordinates && !map) {
      const mapInstance = new maplibregl.Map({
        container: 'map',
        style: 'https://api.maptiler.com/maps/streets/style.json?key=get_your_own_OpIi9ZULNHzrESv6T2vL',
        center: coordinates,
        zoom: 12,
      });

      setMap(mapInstance);

      const redMarker = document.createElement('div');
      redMarker.innerHTML = `
        <svg width="30" height="41" viewBox="0 0 30 41" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M15 0C6.71573 0 0 6.71573 0 15C0 26.25 15 41 15 41C15 41 30 26.25 30 15C30 6.71573 23.2843
         0 15 0ZM15 21C11.6863 21 9 18.3137 9 15C9 11.6863 11.6863 9 15 9C18.3137 9 21 11.6863 21 15C21 18.3137 18.3137 21 15 21Z" fill="#DE0007"/>
        <circle cx="15" cy="15" r="6" fill="white"/>
        </svg>`;
      redMarker.style.width = '30px';
      redMarker.style.height = '41px';

      new maplibregl.Marker({ element: redMarker })
        .setLngLat(coordinates)
        .addTo(mapInstance);
    }
  }, [coordinates, map]);

  useEffect(() => {
    if (map) {
      markerCoordinates.forEach(coord => {
        new maplibregl.Marker()
          .setLngLat(coord)
          .addTo(map);
      });
    }
  }, [markerCoordinates, map]);

  return <div id="map" style={{ height: '100%', width: '100%' }}></div>;
};

export default MapComponent;
