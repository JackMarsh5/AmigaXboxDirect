import TopicMonitor from "./TopicMonitor";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Farm-ng Monitor</h1>
        <TopicMonitor />
      </header>
      <button
        style={{
          position: "absolute",
          bottom: 5,
          left: 10,
          zIndex: 1000,
        }}
        onClick={
            (() =>  window.location.href = `${window.location.protocol}//${window.location.hostname}/apps/launcher`)
        }
      >
        EXIT
      </button>
    </div>
  );
}

export default App;
