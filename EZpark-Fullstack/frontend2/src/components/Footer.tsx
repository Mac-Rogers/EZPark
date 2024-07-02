import React, { useState } from 'react';
import { FaLocationArrow } from 'react-icons/fa';

const Footer: React.FC = () => {
  const [coordinates, setCoordinates] = useState<[number, number] | null>(null);
  const [markerCoordinates, setMarkerCoordinates] = useState<[number, number][]>([]);

  const handleClick = async () => {
    try {
      const response = await fetch('http://localhost:8000/gps-coordinates');
      const data = await response.json();
      const currentCoordinates: [number, number] = [data.longitude, data.latitude];
      setCoordinates(currentCoordinates);
      const db_response = await fetch('http://localhost:8000/items');
      const db_coords = await db_response.json();
      const coords: [number, number][] = db_coords.map((item: { latitude: number, longitude: number }) => [item.longitude, item.latitude]);
      console.log("closest", coords.length)
      setMarkerCoordinates(coords);
      if (coords.length) {
        const closestCoordinate = findClosestCoordinate(currentCoordinates, coords); // Calculate the closest coordinate
        //send coords to backend
        try {
          const response = await fetch('http://localhost:8000/set-coordinates', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              end: closestCoordinate,
            }),
          });
          console.log('Sending:', closestCoordinate);
          const data = await response.json();
          console.log('Response from server:', data);
        } catch (error) {
          console.error('Error sending coordinates:', error);
        }
      } else {
        fetch('http://localhost:8000/set-coordinates', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            end: [0,0],
          }),
        });
      }
    } catch (error) {
      console.error('Error fetching coordinates:', error);
    }
  };

  // Haversine formula to calculate distance between two points on the Earth's surface
  const calculateDistance = ([lng1, lat1]: [number, number], [lng2, lat2]: [number, number]) => {
    const toRadians = (degrees: number) => degrees * (Math.PI / 180);
    const R = 6371; // Radius of the Earth in kilometers
    const dLat = toRadians(lat2 - lat1);
    const dLng = toRadians(lng2 - lng1);
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(toRadians(lat1)) * Math.cos(toRadians(lat2)) *
      Math.sin(dLng / 2) * Math.sin(dLng / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const distance = R * c; // Distance in kilometers
    return distance;
  };

  // Find the closest coordinate from the list
  const findClosestCoordinate = (currentCoordinates: [number, number], coordinates: [number, number][]) => {
    let closestCoordinate = coordinates[0];
    let closestDistance = calculateDistance(currentCoordinates, coordinates[0]);

    coordinates.forEach(coord => {
      const distance = calculateDistance(currentCoordinates, coord);
      if (distance < closestDistance) {
        closestDistance = distance;
        closestCoordinate = coord;
      }
    });

    return closestCoordinate;
  };

  return (
    <div className="footer">
      <button className="find-park" onClick={handleClick}>Find Me A Park</button>
      <div className="location">
        <FaLocationArrow />
      </div>
    </div>
  );
};

export default Footer;
