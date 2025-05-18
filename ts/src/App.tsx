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
