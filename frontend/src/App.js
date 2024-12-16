import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './LoginPage';
import Dashboard from './Dashboard';
import UploadMRI from './UploadMRI';
import Diagnose from './Diagnose';

function App() {
    const [authenticated, setAuthenticated] = useState(false);

    if (!authenticated) {
        return <LoginPage setAuthenticated={setAuthenticated} />;
    }

    return (
        <Router>
            <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/upload-mri" element={<UploadMRI />} />
                <Route path="/diagnose" element={<Diagnose />} />
            </Routes>
        </Router>
    );
}

export default App;
