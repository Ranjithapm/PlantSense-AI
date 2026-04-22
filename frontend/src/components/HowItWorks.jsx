const STEPS = [
  { num: '01', icon: '📤', title: 'Upload Image',
    desc: 'Drag and drop or browse a clear leaf photograph from your device.' },
  { num: '02', icon: '🎨', title: 'Multispectral Extraction',
    desc: 'RGB, HSV, and LAB channels are separated. Vegetation indices (ExG, ExR, VARI) are computed.' },
  { num: '03', icon: '🧠', title: 'AI Classification',
    desc: 'MobileNetV2 (Transfer Learning) classifies the image into one of 38 plant health categories.' },
  { num: '04', icon: '📋', title: 'Instant Results',
    desc: 'Receive the stress type, confidence score, spectral breakdown, and a remediation suggestion.' },
];

export default function HowItWorks() {
  return (
    <section className="how-section" id="how-it-works">
      <div className="container">
        <h2 className="section-heading">How It Works</h2>
        <div className="steps-grid">
          {STEPS.map(s => (
            <div key={s.num} className="step-card glass-card">
              <div className="step-num">{s.num}</div>
              <div className="step-icon">{s.icon}</div>
              <h4>{s.title}</h4>
              <p>{s.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
