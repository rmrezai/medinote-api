
import { useState } from 'react';

export default function MediNoteHoopDemo() {
  const [input, setInput] = useState('HOOP [ labs: {K:6.2, Cr:1.9}, meds: ["lisinopril"], use_opencds: true ]');
  const [response, setResponse] = useState(null);

  const parseHoopInput = (text) => {
    try {
      const jsonBlock = text.match(/\[([^\]]+)\]/)?.[1];
      if (!jsonBlock) return null;
      const fixed = `{${jsonBlock}}`.replace(/([a-zA-Z0-9_]+):/g, '"$1":');
      return JSON.parse(fixed);
    } catch (e) {
      return null;
    }
  };

  const handleSubmit = async () => {
    const payload = parseHoopInput(input);
    if (!payload) return alert("Invalid HOOP input");
    const res = await fetch('https://medinote-api.onrender.com/medinote/ap', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    setResponse(data);
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '700px', margin: 'auto' }}>
      <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>🧠 MediNote HOOP Web Demo</h1>
      <textarea value={input} onChange={e => setInput(e.target.value)} rows={6} style={{ width: '100%', marginTop: '1rem' }} />
      <button onClick={handleSubmit} style={{ marginTop: '1rem' }}>Submit</button>
      {response && (
        <pre style={{ marginTop: '1rem', background: '#f4f4f4', padding: '1rem' }}>
          {response.ap_entries?.join('\n\n') || 'No suggestions returned.'}
        </pre>
      )}
    </div>
  );
}
