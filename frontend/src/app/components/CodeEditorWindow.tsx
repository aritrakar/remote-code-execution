'use client';

import React, { useState } from "react";
import Editor, { OnChange } from "@monaco-editor/react";

interface CodeEditorWindowProps {
  onChange: (field: string, value: string | undefined) => void;
  code: string;
  theme: string;
}

const CodeEditorWindow: React.FC<CodeEditorWindowProps> = ({ onChange, code, theme }) => {
  const [value, setValue] = useState<string>(code || "");

  const handleEditorChange: OnChange = (value, event) => {
    setValue(value || "");
    onChange("code", value);
  };

  return (
    <div className="overlay rounded-md overflow-hidden w-full h-full shadow-4xl">
      <Editor
        height="89vh"
        width="100%"
        language={"python"}
        value={value}
        theme={theme}
        defaultValue="// some comment"
        onChange={handleEditorChange}
      />
    </div>
  );
};

export default CodeEditorWindow;
