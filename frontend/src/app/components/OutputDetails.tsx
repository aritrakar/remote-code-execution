'use client';

import React from "react";

/**
 * Formats memory usage from bytes to megabytes.
 * @param memoryUsage - Memory usage in bytes as a string.
 * @returns Memory usage formatted as a string in megabytes (MB).
 */
const formatMemoryUsage = (memoryUsage: string): string => {
  const memoryInMB = parseFloat(memoryUsage) / (1024 * 1024); // Convert bytes to MB
  return `${memoryInMB.toFixed(2)} MB`; // Format to 2 decimal places
};


/**
 * Formats time taken from seconds to milliseconds.
 * @param timeTaken - Time taken in seconds as a string.
 * @returns Time taken formatted as a string in milliseconds (ms).
 */
const formatTimeTaken = (timeTaken: string): string => {
  const timeInMS = parseFloat(timeTaken) * 1000; // Convert seconds to milliseconds
  return `${timeInMS.toFixed(2)} ms`; // Format to 2 decimal places
};

interface Status {
  description?: string;
}

export interface OutputDetailsInterface {
  status?: Status;
  memory?: string;
  time?: string;
};

interface OutputDetailsProps {
  outputDetails: OutputDetailsInterface;
}

export const OutputDetails: React.FC<OutputDetailsProps> = ({ outputDetails }) => {
  return (
    <div className="metrics-container mt-10 flex flex-col space-y-3">
      <p className="text-sm">
        Status:{" "}
        <span className="font-semibold px-2 py-1 rounded-md bg-gray-100">
          {outputDetails?.status?.description}
        </span>
      </p>
      <p className="text-sm">
        Memory:{" "}
        <span className="font-semibold px-2 py-1 rounded-md bg-gray-100">
          {formatMemoryUsage(outputDetails?.memory || "0")}
        </span>
      </p>
      <p className="text-sm">
        Time:{" "}
        <span className="font-semibold px-2 py-1 rounded-md bg-gray-100">
          {formatTimeTaken(outputDetails?.time || "0")}
        </span>
      </p>
    </div>
  );
};
