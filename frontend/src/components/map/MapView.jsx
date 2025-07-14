
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { useEffect, useState } from "react";
import axios from "../../api/axios";
import { Snackbar, Alert, Box, Typography, LinearProgress } from "@mui/material";
import SmoothMarker from "../SmoothMarker";




import L from "leaflet";

const getBusIcon = (status = "on route") => {
  let color = "blue";

  switch (status.toLowerCase()) {
    case "arrived":
      color = "green";
      break;
    case "delayed":
      color = "red";
      break;
    case "waiting":
    case "pending":
      color = "gray";
      break;
    default:
      color = "blue";
  }

  return L.icon({
    iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-${color}.png`,
    iconSize: [30, 42],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png",
    shadowSize: [41, 41]
  });
};




export default function MapView({ coordinates, tripId }) {
  const [lat, lng] = coordinates || [6.5244, 3.3792]; // fallback default
  const [tripData, setTripData] = useState(null);
  const [busPosition, setBusPosition] = useState(null);
  const [showAlert, setShowAlert] = useState(false);

  useEffect(() => {
    if (!tripId) return;

    const fetchTrip = async () => {
      try {
        const res = await axios.get(`/trips/live/${tripId}/`);
        const { latitude, longitude, origin_lat, origin_lng, dest_lat, dest_lng } = res.data;

        setTripData(res.data);
        setBusPosition([latitude, longitude]);

        const dist = getDistanceKm(latitude, longitude, dest_lat, dest_lng);
        if (dist < 1 && !showAlert) {
          setShowAlert(true);
        }
      } catch (err) {
        console.error("Failed to fetch trip location:", err);
      }
    };

    fetchTrip();
    const interval = setInterval(fetchTrip, 10000); // every 10s
    return () => clearInterval(interval);

  }, [tripId]);

  // Geometry helpers
  function getDistanceKm(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const dLat = ((lat2 - lat1) * Math.PI) / 180;
    const dLon = ((lon2 - lon1) * Math.PI) / 180;
    const a =
      Math.sin(dLat / 2) ** 2 +
      Math.cos((lat1 * Math.PI) / 180) *
        Math.cos((lat2 * Math.PI) / 180) *
        Math.sin(dLon / 2) ** 2;
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  }

  function calculateProgress(bus, origin, destination) {
  const total = getDistanceKm(origin[0], origin[1], destination[0], destination[1]);
  const done = getDistanceKm(origin[0], origin[1], bus[0], bus[1]);
  const progress = Math.min(100, Math.floor((done / total) * 100));
  return progress;
}


  // If only coordinates, no trip
  if (!tripId) {
    return (
      <>
      <MapContainer center={[lat, lng]} zoom={13} style={{ height: '400px', width: '100%' }}>
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={[lat, lng]}>
          <Popup>You're here.</Popup>
        </Marker>
      </MapContainer>
      <Box mt={3}>
        <Typography variant="subtitle2">Legend:</Typography>
        <ul style={{ listStyleType: "none", paddingLeft: 0 }}>
          <li>🟦 Blue – On Route</li>
          <li>🟩 Green – Arrived</li>
          <li>🟥 Red – Delayed</li>
          <li>⬜ Gray – Pending/Waiting</li>
        </ul>
      </Box>
    </>
);
  }

  // If trip is live
  if (!tripData) return <p>Loading trip data...</p>;

  const origin = [tripData.origin_lat, tripData.origin_lng];
  const destination = [tripData.dest_lat, tripData.dest_lng];
  const bus = busPosition;

  return (
    <>
      <MapContainer center={bus || origin} zoom={13} style={{ height: '400px', width: '100%' }}>
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <Marker position={origin}><Popup>🧭 Origin</Popup></Marker>
        <Marker position={destination}><Popup>🏁 Destination</Popup></Marker>
        {bus && <SmoothMarker
          to={bus} icon={getBusIcon(tripData.journey_status)}
          popupText="🚌 Current Position"/>
        }
        {tripData.stops?.map((stop, i) => (
          <Marker key={i} position={[stop.lat, stop.lng]}>
            <Popup>🛑 {stop.name}</Popup>
          </Marker>
        ))}

        <Polyline positions={[origin, bus, destination]} color="blue" />
      </MapContainer>
      <Box mt={3}>
        <Typography variant="subtitle2">Legend:</Typography>
        <ul style={{ listStyleType: "none", paddingLeft: 0 }}>
          <li>🟦 Blue – On Route</li>
          <li>🟩 Green – Arrived</li>
          <li>🟥 Red – Delayed</li>
          <li>⬜ Gray – Pending/Waiting</li>
        </ul>
      </Box>


      {bus && (
        <Box mt={2}>
          <Typography gutterBottom>Trip Progress</Typography>
          <LinearProgress variant="determinate" value={calculateProgress(bus, origin, destination)} />
        </Box>
      )}

      <Snackbar open={showAlert} autoHideDuration={6000} onClose={() => setShowAlert(false)}>
        <Alert severity="info" sx={{ width: '100%' }}>
          🛑 You are approaching your destination!
        </Alert>
      </Snackbar>
    </>
  );
}


// import { MapContainer, TileLayer, Marker, Popup, Polyline 
//         } from 'react-leaflet';
// import 'leaflet/dist/leaflet.css';
// import { useEffect, useState } from "react";
// import axios from "../../api/axios";

// import { Snackbar, Alert } from "@mui/material";



// function getDistanceKm(lat1, lon1, lat2, lon2) {
//   const R = 6371; // Earth radius in km
//   const dLat = ((lat2 - lat1) * Math.PI) / 180;
//   const dLon = ((lon2 - lon1) * Math.PI) / 180;
//   const a =
//     Math.sin(dLat / 2) * Math.sin(dLat / 2) +
//     Math.cos((lat1 * Math.PI) / 180) *
//       Math.cos((lat2 * Math.PI) / 180) *
//       Math.sin(dLon / 2) *
//       Math.sin(dLon / 2);
//   const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
//   return R * c;
// }



// export default function MapView({ coordinates, tripId }) {
//   const [lat, lng] = coordinates;
//   const [tripData, setTripData] = useState(null);
//   const [busPosition, setBusPosition] = useState(null);
//   const [showAlert, setShowAlert] = useState(false);

//   // const tripId = "some-trip-id"; // You can pass this as a prop or route param
//   useEffect(() => {
//     const fetchTrip = async () => {
//       const res = await axios.get(`/trips/live/${tripId}/`);
//       const { latitude, longitude, dest_lat, dest_lng } = res.data;

//       setTripData(res.data);
//       setBusPosition([res.data.latitude, res.data.longitude]);
      
//       const distanceToDest = getDistanceKm(latitude, longitude, dest_lat, dest_lng);
//       if (distanceToDest < 1.0) {
//         alert("🛑 You're nearing your destination!");
//       }
//       if (distanceToDest < 1.0 && !showAlert) {
//         setShowAlert(true);
//       }

    
//     };

//     if (tripId) {
//       fetchTrip();
//       const interval = setInterval(fetchTrip, 10000); // refresh every 10s
//       return () => clearInterval(interval);

//     }
    
//   });
//   // }, [tripId]);

//   if (tripId) {
//     if (!tripData) return <p>Loading trip...</p>;
    
//   }
//   const origin = tripId  ? [tripData.origin_lat, tripData.origin_lng] : '';
//   const destination = tripId  ? [tripData.dest_lat, tripData.dest_lng] : '';
//   const bus = tripId  ? busPosition : '';


//   return (
//       <>

//     <MapContainer center={[lat, lng]} zoom={13} style={{ height: '400px', width: '100%' }}>
//       <TileLayer
//         attribution='&copy; OpenStreetMap contributors'
//         url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
//       />
//       { tripId && (
//         <>
//           <Marker position={origin}><Popup>Origin</Popup></Marker>
//           <Marker position={destination}><Popup>Destination</Popup></Marker>
//         </>)

//       }

//       {tripId && bus && (
//         <Marker position={bus}>
//           <Popup>🚌 Bus Location</Popup>
//         </Marker>
//       )}

//       {tripId && <Polyline positions={[origin, bus, destination]} color="blue" />} 
       
      
      
//       {/* <Marker position={[lat, lng]}>
//         <Popup>You're here.</Popup>
//       </Marker> */}

      
//     </MapContainer>

//       <Snackbar open={showAlert} autoHideDuration={6000} onClose={() => setShowAlert(false)}>
//             <Alert severity="info" onClose={() => setShowAlert(false)} sx={{ width: '100%' }}>
//               🛑 You are approaching your destination!
//             </Alert>
//       </Snackbar>
//     </>
//   );
// }


// // export default function MapView({ coordinates }) {
// //   const [lat, lng] = coordinates;

// //   return (
// //     <MapContainer center={[lat, lng]} zoom={13} style={{ height: '400px', width: '100%' }}>
// //       <TileLayer
// //         attribution='&copy; OpenStreetMap contributors'
// //         url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
// //       />
// //       <Marker position={[lat, lng]}>
// //         <Popup>You're here.</Popup>
// //       </Marker>
// //     </MapContainer>
// //   );
// // }

