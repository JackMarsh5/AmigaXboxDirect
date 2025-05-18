import React, { useState } from "react";

type Device = {
  mac: string;
  name: string;
};

export function App() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [pairing, setPairing] = useState<string | null>(null);
  const [status, setStatus] = useState<string>("");

  const scanDevices = async () => {
    setStatus("Scanning...");
    const res = await fetch("/bluetooth/scan");
    const data = await res.json();
    setDevices(data);
    setStatus(data.length ? "Select a device to pair" : "No Xbox controllers found");
  };

  const pairDevice = async (mac: string) => {
    setPairing(mac);
    setStatus(`Pairing with ${mac}...`);
    const res = await fetch("/bluetooth/pair?mac=" + mac, { method: "POST" });
    const result = await res.json();
    setPairing(null);
    setStatus(result.message || "Pairing complete");
  };

  return (
    <div className="p-4 text-xl font-mono">
      <h1 className="text-2xl font-bold mb-4">Xbox Controller Pairing</h1>
      <button
        className="bg-blue-600 text-white px-4 py-2 rounded mb-4"
        onClick={scanDevices}
      >
        Scan for Devices
      </button>
      <div className="mb-4">{status}</div>
      <ul>
        {devices.map((device) => (
          <li key={device.mac} className="mb-2">
            <button
              className="bg-green-600 text-white px-3 py-1 rounded"
              onClick={() => pairDevice(device.mac)}
              disabled={pairing === device.mac}
            >
              {pairing === device.mac ? "Pairing..." : `Pair ${device.name}`}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

import React, { useEffect, useState } from "react";

export function App() {
  const [input, setInput] = useState<{ linear: number; angular: number } | null>(null);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8042/subscribe/track_follower/cmd_vel");
    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.linear !== undefined && msg.angular !== undefined) {
        setInput({ linear: msg.linear, angular: msg.angular });
      }
    };
    return () => ws.close();
  }, []);

  return (
    <div className="p-4 text-xl font-mono">
      <h1 className="text-2xl font-bold mb-4">Joystick Input Monitor</h1>
      {input ? (
        <div>
          Linear: {input.linear.toFixed(2)}<br />
          Angular: {input.angular.toFixed(2)}
        </div>
      ) : (
        <p>Waiting for joystick commands...</p>
      )}
    </div>
  );
}
