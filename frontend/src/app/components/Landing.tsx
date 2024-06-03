'use client';

import React, { useEffect, useState } from "react";
import CodeEditorWindow from "./CodeEditorWindow";
import axios from "axios";
import { classnames } from "../etc/general";
import { ActionMeta, SingleValue } from "react-select";
// import { languageOptions } from "../constants/languageOptions";

import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import { defineTheme } from "../etc/themes";
import useKeyPress from "../hooks/useKeyPress";
import { OutputWindow, OutputWindowDetails } from "./OutputWindow";
import CustomInput from "./CustomInput";
import { OutputDetails, OutputDetailsInterface } from "./OutputDetails";
import { ThemeDropdown, ThemeOption } from "./ThemeDropdown";

const API_URL = 'http://localhost:8000';

const pythonDefault = `# Returns index of x in arr if present, else -1
def binary_search(arr, low, high, x):

	# Check base case
	if high >= low:

		mid = (high + low) // 2

		# If element is present at the middle itself
		if arr[mid] == x:
			return mid

		# If element is smaller than mid, then it can only
		# be present in left subarray
		elif arr[mid] > x:
			return binary_search(arr, low, mid - 1, x)

		# Else the element can only be present in right subarray
		else:
			return binary_search(arr, mid + 1, high, x)

	else:
		# Element is not present in the array
		return -1

# Test array
arr = [ 2, 3, 4, 10, 40 ]
x = 10

# Function call
result = binary_search(arr, 0, len(arr)-1, x)

if result != -1:
	print("Element is present at index", str(result))
else:
	print("Element is not present in array")
`;

const Landing = () => {
  const [code, setCode] = useState(pythonDefault);
  const [outputWindowDetails, setOutputWindowDetails] = useState<OutputWindowDetails>({});
  const [outputDetails, setOutputDetails] = useState<OutputDetailsInterface | null>(null);
  const [processing, setProcessing] = useState(false);
  const [theme, setTheme] = useState<ThemeOption>({ value: "oceanic-next", label: "Oceanic Next" });

  const onChange = (action: string, data: string | undefined) => {
    switch (action) {
      case "code": {
        setCode(data || pythonDefault);
        break;
      }
      default: {
        console.warn("case not handled!", action, data);
      }
    }
  };

  const handleExecute = async () => {
    try {
      setProcessing(true);
      const response = await axios.post(`${API_URL}/execute`, { code });
      
      if (response.data.exit_code === 0) {
        showSuccessToast();
        const result: OutputWindowDetails = {
          status: { id: 0 },
          stdout: response.data.output,
        }
        setOutputWindowDetails(result);
        
        const outputDetailsInfo: OutputDetailsInterface = {
          status: { description: "Success" },
          memory: response.data.memory,
          time: response.data.time,
        }
        setOutputDetails(outputDetailsInfo);
      } else {
        showErrorToast();

        const result: OutputWindowDetails = {
          status: { id: 1 },
          stderr: response.data.output,
        }
        setOutputWindowDetails(result);
        
        const errorOutputDetails: OutputDetailsInterface = {
          status: { description: "Error" },
          memory: response.data.memory,
          time: response.data.time,
        }
        setOutputDetails(errorOutputDetails);

        console.error('Failed to execute code:', response);
      }
    } catch (error) {
      showErrorToast();
      console.error('Error executing code:', error);
    }

    setProcessing(false);
  };

  const handleSubmit = async () => {
    try {
      setProcessing(true);
      const response = await axios.post(`${API_URL}/submit`, { code });
      if (response.data.exit_code === 0) {
        showSuccessToast('Code submitted successfully!');
        const result: OutputWindowDetails = {
          status: { id: 0 },
          stdout: response.data.output,
        }
        setOutputWindowDetails(result);

        const outputDetailsInfo: OutputDetailsInterface = {
          status: { description: "Success" },
          memory: response.data.memory,
          time: response.data.time,
        }
        setOutputDetails(outputDetailsInfo);
      } else {
        showErrorToast('Failed to submit code!');

        const result: OutputWindowDetails = {
          status: { id: 1 },
          stderr: response.data.output,
        }
        setOutputWindowDetails(result);
        
        const errorOutputDetails: OutputDetailsInterface = {
          status: { description: "Error" },
          memory: response.data.memory,
          time: response.data.time,
        }
        setOutputDetails(errorOutputDetails);

        console.error('Failed to submit code:', response);
      }
    } catch (error) {
      showErrorToast('Failed to submit code!');
      console.error('Error submitting code:', error);
    }

    setProcessing(false);
  };

  function handleThemeChange(selectedOption: SingleValue<ThemeOption>, actionMeta: ActionMeta<ThemeOption>) {
    const theme = selectedOption as ThemeOption;
    console.log("theme...", theme);
  
    if (["light", "vs-dark"].includes(theme.value)) {
      setTheme(theme);
    } else {
      defineTheme(theme.value).then((_) => setTheme(theme));
    }
  }
  
  
  useEffect(() => {
    defineTheme("oceanic-next").then((_) =>
      setTheme({ value: "oceanic-next", label: "Oceanic Next" })
    );
  }, []);

  const showSuccessToast = (msg: string=`Compiled Successfully!`) => {
    toast.success(msg, {
      position: "top-right",
      autoClose: 1000,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
    });
  };

  const showErrorToast = (msg: string = `Something went wrong! Please try again.`, timer: number | undefined = 1000) => {
    toast.error(msg, {
      position: "top-right",
      autoClose: timer,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
    });
  };

  return (
    <div>
      <ToastContainer
        position="top-right"
        autoClose={2000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
      
      <div className="h-4 w-full bg-gradient-to-r from-blue-500 via-green-300 to-yellow-300"></div>

      <div className="px-4 py-2">
        <ThemeDropdown handleThemeChange={handleThemeChange} theme={theme} />
      </div>

      <div className="flex flex-row space-x-4 items-start px-4 py-4">
        <div className="flex flex-col w-full h-full justify-start items-end">
          <CodeEditorWindow
            code={code}
            onChange={onChange}
            theme={theme.value}
          />
        </div>

        <div className="right-container flex flex-shrink-0 w-[30%] flex-col">
          <OutputWindow outputDetails={outputWindowDetails} />
          <div className="flex items-end">
            <button
              onClick={() => handleExecute()}
              disabled={!code}
              className={classnames(
                "mt-4 mr-6 border-2 border-black z-10 rounded-md shadow-[5px_5px_0px_0px_rgba(0,0,0)] px-4 py-2 hover:shadow transition duration-200 bg-white flex-shrink-0",
                !code ? "opacity-50" : ""
              )}
            >
              {processing ? "Processing..." : "Execute"}
            </button>

            <button
              onClick={handleSubmit}
              disabled={!code}
              className={classnames(
                "mt-4 border-2 border-black z-10 rounded-md shadow-[5px_5px_0px_0px_rgba(0,0,0)] px-4 py-2 hover:shadow transition duration-200 bg-white flex-shrink-0",
                !code ? "opacity-50" : ""
              )}
            >
              {processing ? "Processing..." : "Submit"}
            </button>
          </div>
          {outputDetails && <OutputDetails outputDetails={outputDetails} />}
        </div>
      </div>
    </div>
  );
};

export default Landing;
