import React, { useState } from 'react';

export default function UploadPage() {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleVerify = async () => {
    if (!file) {
      alert("Please select a file first!");
      return;
    }

    const reader = new FileReader();
    reader.onloadend = async () => {
      const base64 = reader.result.split(',')[1];

      try {
        const res = await fetch('http://localhost:5000/api/verify', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ file: base64 })
        });
        const data = await res.json();
        console.log("Verification result:", data);
        alert(JSON.stringify(data, null, 2));
      } catch (error) {
        console.error("Error verifying:", error);
        alert("Verification failed!");
      }
    };
    reader.readAsDataURL(file);
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-2">Upload Document to Verify</h2>
      <input type="file" onChange={handleFileChange} className="mb-2" />
      <button onClick={handleVerify} className="bg-blue-500 text-white px-4 py-2 rounded">
        Verify Document
      </button>
    </div>
  );
}
