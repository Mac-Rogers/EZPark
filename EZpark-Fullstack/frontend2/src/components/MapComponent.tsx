import React, { useEffect, useState, useRef } from 'react';
import 'maplibre-gl/dist/maplibre-gl.css';
import MapLibreGlDirections, { LoadingIndicatorControl } from "@maplibre/maplibre-gl-directions";
import maplibregl, { LngLat } from 'maplibre-gl';

const MapComponent: React.FC = () => {
  const [coordinates, setCoordinates] = useState<[number, number] | null>(null);
  const [markerCoordinates, setMarkerCoordinates] = useState<[number, number][]>([]);
  const [map, setMap] = useState<maplibregl.Map | null>(null);
  const [directions, setDirections] = useState<MapLibreGlDirections | null>(null);
  const markersRef = useRef<maplibregl.Marker[]>([]);  // To keep track of the markers
  const [localRecentreCount, setLocalRecentreCount] = useState(0);

  useEffect(() => {
    const fetchCoordinates = async () => {
      try {
        const response = await fetch('http://localhost:8000/gps-coordinates');
        const data = await response.json();
        setCoordinates([data.longitude, data.latitude]);
        //console.log([data.longitude, data.latitude])
        const db_response = await fetch('http://localhost:8000/items');
        const db_coords = await db_response.json();
        const coords = db_coords.map((item: { latitude: number, longitude: number }) => [item.longitude, item.latitude]);
        setMarkerCoordinates(coords);
        fetch('http://localhost:8000/set-coordinates', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            end: [0, 0],
          }),
        });
        
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

      mapInstance.on('load', () => {
        const directionsInstance = new MapLibreGlDirections(mapInstance);
        setDirections(directionsInstance);
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
    const intervalId = setInterval(() => {
      const updateMap = async () => {
        try {
          if (map && coordinates) {
          const local_recentre = await fetch('http://localhost:8000/recentre_check');
          const recentre_count = await local_recentre.json();
          //console.log("local:", localRecentreCount, "remote:", recentre_count.count)
          if (localRecentreCount < recentre_count.count) {
            setLocalRecentreCount(prevCount => prevCount + 1);
            map.flyTo({
              center: new maplibregl.LngLat(coordinates[0], coordinates[1])
            });
          }

          const db_response = await fetch('http://localhost:8000/items');
          const db_coords = await db_response.json();
          const coords = db_coords.map((item: { latitude: number, longitude: number }) => [item.longitude, item.latitude]);

          // Add new markers
          const newMarkers = coords.map((coord: maplibregl.LngLatLike) => {
            const marker = new maplibregl.Marker().setLngLat(coord).addTo(map!);
            return marker;
          });

          // Remove old markers
          markersRef.current.forEach(marker => marker.remove());
          markersRef.current = newMarkers;

          setMarkerCoordinates(coords);
          //console.log(markerCoordinates);

          
            coords.map((coord: maplibregl.LngLatLike) => {
              const marker = new maplibregl.Marker().setLngLat(coord).addTo(map);
              markersRef.current.push(marker);
              return marker;
            });
          

            const response = await fetch('http://localhost:8000/get-coordinates');
            const data = await response.json();
            if (directions && data.dest_coords[0] && coordinates) {
              //console.log("desstcorrds: ", data.dest_coords)

              directions.setWaypoints([
                coordinates,
                data.dest_coords,
              ]);
            }
          }
          //setCoordinates([data.longitude, data.latitude]);
        } catch (error) {
          console.error('Error updating map:', error);
        }
      };
      updateMap();
    }, 1000); // Poll every 3 seconds
    return () => clearInterval(intervalId);
  }, [map, coordinates, directions, markerCoordinates, localRecentreCount]);
  


  return <div id="map" style={{ height: '100%', width: '100%' }}></div>;
};

export default MapComponent;
