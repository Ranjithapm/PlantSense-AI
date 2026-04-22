export default function Hero() {
  return (
    <section className="hero">
      <div className="hero-content">
        <div className="hero-tag">🔬 Deep Learning + Multispectral Analysis</div>
        <h1 className="hero-title">
          Detect Plant Stress<br />
          <span className="gradient-text">Before It's Visible</span>
        </h1>
        <p className="hero-desc">
          Upload a leaf image and our AI model analyzes{' '}
          <strong>RGB, HSV, LAB color channels</strong> and{' '}
          <strong>vegetation indices</strong> to detect disease, nutrient
          deficiency, or water stress at the earliest stage — powered by
          MobileNetV2 Transfer Learning.
        </p>
        <div className="hero-stats">
          <div className="stat-pill">🎯 93%+ Accuracy</div>
          <div className="stat-pill">⚡ &lt;2s Inference</div>
          <div className="stat-pill">🌱 38 Plant Classes</div>
          <div className="stat-pill">📊 Vegetation Indices</div>
        </div>
      </div>
    </section>
  );
}
