import { useEffect, useRef } from 'react';

const COLORS = ['#4ade80', '#2dd4bf', '#a3e635', '#86efac'];

export default function BgParticles() {
  const ref = useRef(null);

  useEffect(() => {
    const container = ref.current;
    if (!container) return;
    const count = 25;
    for (let i = 0; i < count; i++) {
      const p = document.createElement('div');
      p.className = 'particle';
      const size = Math.random() * 14 + 4;
      Object.assign(p.style, {
        width:             `${size}px`,
        height:            `${size}px`,
        left:              `${Math.random() * 100}%`,
        bottom:            `-${size}px`,
        background:        COLORS[Math.floor(Math.random() * COLORS.length)],
        animationDuration: `${Math.random() * 18 + 12}s`,
        animationDelay:    `${Math.random() * 10}s`,
      });
      container.appendChild(p);
    }
  }, []);

  return <div className="bg-particles" ref={ref} />;
}
