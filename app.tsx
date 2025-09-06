import React, { useState } from "react";
import FileUpload from "./components/FileUpload";
import Chat from "./components/Chat";

const App: React.FC = () => {
  const [fileUploaded, setFileUploaded] = useState(false);

  return (
    <div className="min-h-screen p-6 flex flex-col items-center">
      <h1 className="text-3xl font-bold mb-6">📘 RAG Q&A System</h1>
      {!fileUploaded ? (
        <FileUpload onUpload={() => setFileUploaded(true)} />
      ) : (
        <Chat />
      )}
    </div>
  );
};

export default App;