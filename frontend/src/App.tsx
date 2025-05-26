import { useState } from "react";
import Editor from "@monaco-editor/react";

function App() {
  const [code, setCode] = useState("// Codegen output will appear here");

  const startCodegen = async () => {
    const response = await fetch("http://localhost:8000/start-codegen");
    const data = await response.json();
    setCode(data.code);
  };

  const saveCode = async () => {
    await fetch("http://localhost:8000/save-code", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ code })
    });
    alert("Code saved!");
  };

  return (
    <div>
      <button onClick={startCodegen}>Start Codegen</button>
      <button onClick={generatePageObjects}>Generate Page Objects</button>
      <button onClick={saveCode}>Save</button>
      <button onClick={generatePageObjects}>Generate Page Objects</button>
      <Editor
        height="80vh"
        defaultLanguage="csharp"
        value={code}
        onChange={(val) => setCode(val || "")}
      />
    </div>
  );
}

export default App;


  async function generatePageObjects() {
    await fetch("http://localhost:8000/generate-page-objects", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ code })
    });
    alert("Page objects and test classes generated!");
  }
