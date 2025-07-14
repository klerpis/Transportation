// SmoothMarker.jsx
import { useEffect, useState } from "react";
import { Marker, Popup } from "react-leaflet";
import L from "leaflet";

function interpolate(from, to, factor) {
  return from + (to - from) * factor;
}

export default function SmoothMarker({ to, icon, duration = 1000, popupText = "" }) {
  const [position, setPosition] = useState(to);

  useEffect(() => {
    let animationFrame;
    let start = null;

    const animate = (timestamp) => {
      if (!start) start = timestamp;
      const elapsed = timestamp - start;
      const progress = Math.min(elapsed / duration, 1);

      const lat = interpolate(position[0], to[0], progress);
      const lng = interpolate(position[1], to[1], progress);

      setPosition([lat, lng]);

      if (progress < 1) {
        animationFrame = requestAnimationFrame(animate);
      }
    };

    animationFrame = requestAnimationFrame(animate);

    return () => cancelAnimationFrame(animationFrame);
  }, [to]);

  return (
    <Marker position={position} icon={icon}>
      <Popup>{popupText}</Popup>
    </Marker>
  );
}
