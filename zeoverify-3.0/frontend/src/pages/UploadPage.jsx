import React, { useState } from "react";
import FileCard from "../components/FileCard";

export default function UploadPage() {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file!");
      return;
    }
    alert(`Ready to upload: ${file.name}`);
    // TODO: connect backend
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 p-4">
      <div className="bg-white bg-opacity-20 backdrop-blur-md rounded-xl shadow-2xl p-8 max-w-md w-full">
        <h2 className="text-3xl font-semibold text-white mb-6 text-center">
          Upload Document
        </h2>
        <input
          type="file"
          onChange={handleFileChange}
          className="block w-full text-white file:mr-4 file:py-2 file:px-4 
                     file:rounded-full file:border-0
                     file:text-sm file:font-semibold
                     file:bg-blue-50 file:text-blue-700
                     hover:file:bg-blue-100 mb-4"
        />
        <button
          onClick={handleUpload}
          className="w-full bg-green-500 hover:bg-green-600 text-white py-2 rounded-lg font-medium transition"
        >
          Upload & Verify
        </button>
        {file && <FileCard file={file} />}
      </div>
    </div>
  );
}
