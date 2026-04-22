import { useEffect, useRef, useState } from 'react';

const TYPE_MAP = { Healthy: 'healthy', Disease: 'disease', Pest: 'pest', Virus: 'virus' };
const RANK_CLASS = ['r1', 'r2', 'r3'];

function animateNumber(setter, from, to, duration) {
  const start = performance.now();
  function step(now) {
    const t = Math.min((now - start) / duration, 1);
    const ease = 1 - Math.pow(1 - t, 3);
    setter(Math.round(from + (to - from) * ease));
    if (t < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

function SpectralBar({ label, value, colorClass }) {
  const [width, setWidth] = useState(0);
  const clamped = Math.min(100, Math.max(0, value));
  useEffect(() => {
    const t = setTimeout(() => setWidth(clamped), 150);
    return () => clearTimeout(t);
  }, [clamped]);
  return (
    <div className="spectral-row">
      <div className="spectral-label">
        <span>{label}</span>
        <span className="spectral-val">{clamped.toFixed(1)}%</span>
      </div>
      <div className="spectral-track">
        <div className={`spectral-fill ${colorClass}`} style={{ width: `${width}%` }} />
      </div>
    </div>
  );
}

function Top3Item({ pred, rank }) {
  const [barWidth, setBarWidth] = useState(0);
  useEffect(() => {
    const t = setTimeout(() => setBarWidth(pred.confidence), 300);
    return () => clearTimeout(t);
  }, [pred.confidence]);
  return (
    <div className="top3-item">
      <div className={`top3-rank ${RANK_CLASS[rank]}`}>{rank + 1}</div>
      <div className="top3-info">
        <div className="top3-name">{pred.name}</div>
        <div className="top3-track">
          <div className="top3-bar" style={{ width: `${barWidth}%` }} />
        </div>
      </div>
      <div className="top3-conf">{pred.confidence.toFixed(1)}%</div>
    </div>
  );
}

export default function Results({ data, onReset }) {
  const [ringOffset, setRingOffset] = useState(314);
  const [pctDisplay, setPctDisplay] = useState(0);
  const circumference = 2 * Math.PI * 50;

  useEffect(() => {
    if (!data) return;
    const pct = Math.min(100, Math.max(0, data.predictions[0].confidence));
    const offset = circumference - (pct / 100) * circumference;
    const t = setTimeout(() => {
      setRingOffset(offset);
      animateNumber(setPctDisplay, 0, pct, 1200);
    }, 100);
    return () => clearTimeout(t);
  }, [data]);

  if (!data) return null;
  const top = data.predictions[0];
  const s   = data.spectral;

  return (
    <section className="results-section" id="results-section">
      <div className="container">
        {data.demo_mode && (
          <div className="demo-alert">
            ⚡ <strong>Demo Mode:</strong> Trained model not loaded — showing simulated predictions.
            Train and place your model at <code>model/plant_model.h5</code> to enable real inference.
          </div>
        )}

        <div className="results-grid">
          {/* Analysed Image */}
          <div className="result-block glass-card">
            <h3 className="block-title">📸 Analysed Image</h3>
            <img src={`${import.meta.env.VITE_API_URL || ''}${data.image_url}`} alt="Analysed leaf" className="result-img" />
          </div>

          {/* Primary Prediction */}
          <div className="result-block glass-card primary-result">
            <div className="primary-label">Primary Prediction</div>
            <h2 className="primary-name">{top.name}</h2>
            <div className={`primary-type-badge ${TYPE_MAP[top.type] || ''}`}>{top.type}</div>

            <div className="confidence-ring-wrapper">
              <svg className="confidence-ring" viewBox="0 0 120 120">
                <defs>
                  <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%"   stopColor="#16a34a" />
                    <stop offset="100%" stopColor="#2dd4bf" />
                  </linearGradient>
                </defs>
                <circle cx="60" cy="60" r="50" className="ring-bg" />
                <circle
                  cx="60" cy="60" r="50"
                  className="ring-fill"
                  strokeDasharray="314"
                  strokeDashoffset={ringOffset}
                />
              </svg>
              <div className="ring-label">
                <span className="ring-pct">{pctDisplay}%</span>
                <span className="ring-text">confidence</span>
              </div>
            </div>

            <div className="remedy-box">
              <div className="remedy-title">💊 Recommended Action</div>
              <p className="remedy-text">{top.remedy}</p>
            </div>
          </div>

          {/* Spectral Analysis */}
          <div className="result-block glass-card spectral-block">
            <h3 className="block-title">📡 Spectral Analysis</h3>
            <p className="spectral-desc">Multispectral vegetation indices extracted from the image</p>
            <SpectralBar label="ExG – Excess Green"     value={s.ExG}       colorClass="green" />
            <SpectralBar label="ExR – Excess Red"       value={s.ExR}       colorClass="red"   />
            <SpectralBar label="VARI – Vegetation Index" value={s.VARI}     colorClass="teal"  />
            <SpectralBar label="Greenness Ratio"         value={s.greenness} colorClass="lime"  />
          </div>

          {/* Top-3 Predictions */}
          <div className="result-block glass-card top3-block">
            <h3 className="block-title">🏆 Top 3 Predictions</h3>
            <div className="top3-list">
              {data.predictions.map((pred, i) => (
                <Top3Item key={i} pred={pred} rank={i} />
              ))}
            </div>
          </div>
        </div>

        <div className="reset-wrap">
          <button className="reset-btn" onClick={onReset}>🔄 Analyse Another Image</button>
        </div>
      </div>
    </section>
  );
}
