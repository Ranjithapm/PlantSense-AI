import { useState, useRef } from 'react';
import axios from 'axios';

export default function UploadSection({ onResults }) {
  const [file, setFile]       = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dragover, setDragover] = useState(false);
  const inputRef = useRef(null);

  function loadFile(f) {
    if (!f || !f.type.startsWith('image/')) return;
    setFile(f);
    const reader = new FileReader();
    reader.onload = e => setPreview(e.target.result);
    reader.readAsDataURL(f);
  }

  function resetUpload() {
    setFile(null);
    setPreview(null);
    if (inputRef.current) inputRef.current.value = '';
  }

  async function handleAnalyze() {
    if (!file) return;
    setLoading(true);
    try {
      const fd = new FormData();
      fd.append('file', file);
      const API_URL = import.meta.env.VITE_API_URL || '';
      const { data } = await axios.post(`${API_URL}/predict`, fd);
      if (!data.success) throw new Error(data.error || 'Prediction failed');
      onResults(data);
    } catch (err) {
      const errorMsg = err.response?.data?.error || err.message;
      alert('Error: ' + errorMsg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="upload-section" id="upload-section">
      <div className="container">
        <div className="upload-card glass-card">
          <h2 className="section-title">Upload Leaf Image</h2>
          <p className="section-sub">Supports JPG, PNG, JPEG — Max 16 MB</p>

          <div
            className={`drop-zone${dragover ? ' dragover' : ''}`}
            onDragOver={e => { e.preventDefault(); setDragover(true); }}
            onDragLeave={() => setDragover(false)}
            onDrop={e => { e.preventDefault(); setDragover(false); loadFile(e.dataTransfer.files[0]); }}
            onClick={() => { if (!file) inputRef.current?.click(); }}
          >
            {!preview ? (
              <>
                <div className="drop-icon">📸</div>
                <p className="drop-title">Drag &amp; Drop your leaf image here</p>
                <p className="drop-or">or</p>
                <button
                  className="browse-btn"
                  onClick={e => { e.stopPropagation(); inputRef.current?.click(); }}
                >
                  Browse File
                </button>
              </>
            ) : (
              <div className="preview-container" onClick={e => e.stopPropagation()}>
                <img src={preview} alt="Preview" className="preview-img" />
                <div className="preview-overlay">
                  <span className="preview-label">Selected Image</span>
                  <button className="clear-btn" onClick={e => { e.stopPropagation(); resetUpload(); }}>
                    ✕ Clear
                  </button>
                </div>
              </div>
            )}
            <input
              ref={inputRef}
              type="file"
              accept="image/*"
              hidden
              onChange={e => { if (e.target.files[0]) loadFile(e.target.files[0]); }}
            />
          </div>

          <button
            className="analyze-btn"
            disabled={!file || loading}
            onClick={handleAnalyze}
          >
            <span className="btn-icon">🔬</span>
            <span>{loading ? 'Analysing…' : 'Analyze Image'}</span>
            {loading && <div className="btn-loader" />}
          </button>
        </div>
      </div>
    </section>
  );
}
