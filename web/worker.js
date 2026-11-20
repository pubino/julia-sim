const scope = /** @type {import("./protocol").WorkerScope} */ (/** @type {unknown} */ (self));

async function initialize() {
  const vendor = new URL("./vendor/", scope.location.href).href;
  scope.importScripts(new URL("pyodide.js", vendor).href);
  const python = await scope.loadPyodide({ indexURL: vendor });
  await python.loadPackage("numpy");
  const response = await fetch(new URL("simulation.py", scope.location.href));
  if (!response.ok) throw new Error("Could not load the Python model.");
  python.FS.writeFile("/home/pyodide/simulation.py", await response.text());
  return python.runPython("from simulation import create\ncreate");
}

initialize().then((create) => {
  /** @type {import("./protocol").SimulationProxy | undefined} */
  let simulation;
  scope.onmessage = ({ data }) => {
    try {
      if (data.type === "reset") {
        const next = create(JSON.stringify(data.parameters));
        simulation?.destroy();
        simulation = next;
      } else {
        if (!simulation) throw new Error("The simulation must be initialized.");
        simulation.advance(data.steps);
      }

      const proxy = simulation.frame();
      try {
        const frame = proxy.toJs({ create_pyproxies: false });
        scope.postMessage({ type: data.type, id: data.id, frame }, [frame[3].buffer]);
      } finally {
        proxy.destroy();
      }
    } catch (error) {
      const message = String(error).match(/ValueError: ([^\r\n]+)/)?.[1];
      scope.postMessage({ type: "failed", id: data.id, message: message ?? "The simulation stopped unexpectedly." });
    }
  };
  scope.postMessage({ type: "ready" });
}, () => scope.postMessage({ type: "fatal" }));
