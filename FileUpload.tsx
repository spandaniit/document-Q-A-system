import React, { useState } from "react";
import axios from "axios";

interface Props {
  onUpload: () => void;
}

const FileUpload: React.FC<Props> = ({ onUpload }) => {
  const [file, setFile] = useState<File | null>(null);

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    await axios.post("/api/upload", formData);
    onUpload();
  };

  return (
    <div className="flex flex-col items-center gap-4">
      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <button
        onClick={handleUpload}
        className="bg-blue-500 text-white px-4 py-2 rounded-lg"
      >
        Upload
      </button>
    </div>
  );
};

export default FileUpload;