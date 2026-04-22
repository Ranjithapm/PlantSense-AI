import { useState, useEffect, useRef } from 'react';
import BgParticles   from './components/BgParticles';
import Header        from './components/Header';
import Hero          from './components/Hero';
import UploadSection from './components/UploadSection';
import Results       from './components/Results';
import HowItWorks    from './components/HowItWorks';
import About         from './components/About';
import Footer        from './components/Footer';

export default function App() {
  const [results, setResults]         = useState(null);
  const [modelLoaded, setModelLoaded] = useState(false);
  const resultsRef = useRef(null);

  // Check model status on mount
  useEffect(() => {
    fetch('/status')
      .then(r => r.json())
      .then(data => setModelLoaded(data.model_loaded))
      .catch(() => setModelLoaded(false));
  }, []);

  function handleResults(data) {
    setModelLoaded(!data.demo_mode);
    setResults(data);
    // Scroll to results after state update
    setTimeout(() => {
      resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
  }

  function handleReset() {
    setResults(null);
    document.getElementById('upload-section')?.scrollIntoView({ behavior: 'smooth' });
  }

  return (
    <>
      <BgParticles />
      <Header modelLoaded={modelLoaded} />
      <Hero />
      <UploadSection onResults={handleResults} />
      {results && (
        <div ref={resultsRef}>
          <Results data={results} onReset={handleReset} />
        </div>
      )}
      <HowItWorks />
      <About />
      <Footer />
    </>
  );
}
