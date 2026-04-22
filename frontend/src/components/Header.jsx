export default function Header({ modelLoaded }) {
  return (
    <header className="header">
      <div className="header-inner">
        <div className="logo">
          <div className="logo-icon">🌿</div>
          <div>
            <span className="logo-title">PlantSense AI</span>
            <span className="logo-sub">Multispectral Stress Detection</span>
          </div>
        </div>
        <nav className="nav-pills">
          <a href="#upload-section" className="nav-pill active">Detect</a>
          <a href="#how-it-works"   className="nav-pill">How It Works</a>
          <a href="#about-section"  className="nav-pill">About</a>
        </nav>
        {modelLoaded
          ? <div className="live-badge">🟢 Model Live</div>
          : <div className="demo-badge">⚡ Demo Mode</div>}
      </div>
    </header>
  );
}
