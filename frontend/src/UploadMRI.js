import React, { useState } from 'react';
import axios from 'axios';

function UploadMRI() {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append('file', file);

        const response = await axios.post('http://localhost:5000/upload-mri', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });

        setResult(response.data);
    };

    return (
        <div>
            <h1>Upload MRI</h1>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload</button>
            {result && (
                <div>
                    <h3>Result:</h3>
                    <p>Tumor Type: {result.label}</p>
                    <p>Confidence: {result.score}</p>
                </div>
            )}
        </div>
    );
}

export default UploadMRI;
