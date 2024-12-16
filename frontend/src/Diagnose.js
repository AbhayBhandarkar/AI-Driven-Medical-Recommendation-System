import React, { useState } from 'react';
import axios from 'axios';

function Diagnose() {
    const [symptoms, setSymptoms] = useState('');
    const [result, setResult] = useState(null);

    const handleDiagnose = async () => {
        const response = await axios.post('http://localhost:5000/diagnose', { symptoms });
        setResult(response.data);
    };

    return (
        <div>
            <h1>Symptom Diagnosis</h1>
            <textarea placeholder="Enter symptoms..." onChange={(e) => setSymptoms(e.target.value)}></textarea>
            <button onClick={handleDiagnose}>Diagnose</button>
            {result && (
                <div>
                    <h3>Result:</h3>
                    <p>Disease: {result.label}</p>
                    <p>Confidence: {result.score}</p>
                </div>
            )}
        </div>
    );
}

export default Diagnose;
