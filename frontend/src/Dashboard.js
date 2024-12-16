import React from 'react';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
    const navigate = useNavigate();

    return (
        <div>
            <h1>Dashboard</h1>
            <button onClick={() => navigate('/upload-mri')}>Upload MRI</button>
            <button onClick={() => navigate('/diagnose')}>Symptom Diagnosis</button>
        </div>
    );
}

export default Dashboard;
