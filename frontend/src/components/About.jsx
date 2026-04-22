const STATS = [
  { num: '54,305', label: 'Training Images' },
  { num: '38',     label: 'Plant Classes'   },
  { num: '93%+',   label: 'Test Accuracy'   },
  { num: '<2s',    label: 'Per Prediction'  },
];

const CHIPS = ['Python 3.10','TensorFlow / Keras','MobileNetV2','OpenCV','Flask','PlantVillage Dataset'];

export default function About() {
  return (
    <section className="about-section" id="about-section">
      <div className="container about-grid">
        <div className="about-text">
          <h2 className="section-heading">About This Project</h2>
          <p>
            <strong>PlantSense AI</strong> is a mini project developed as part of the B.E. / B.Tech
            curriculum. It leverages multispectral image analysis and convolutional neural networks to
            identify plant stress conditions <em>before</em> visible symptoms appear — enabling timely
            intervention and reducing crop yield losses.
          </p>
          <div className="tech-chips">
            {CHIPS.map(c => <span key={c} className="chip">{c}</span>)}
          </div>
        </div>
        <div className="about-stats">
          {STATS.map(s => (
            <div key={s.label} className="astat glass-card">
              <div className="astat-num">{s.num}</div>
              <div className="astat-label">{s.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
