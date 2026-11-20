export type Frame = [step: number, count: number, threshold: number, mask: Uint8Array<ArrayBuffer>];
export type Request =
  | { type: "reset"; id: number; parameters: number[] }
  | { type: "advance"; id: number; steps: number };
export type Reply =
  | { type: "ready" | "fatal" }
  | { type: "reset" | "advance"; id: number; frame: Frame }
  | { type: "failed"; id: number; message: string };

export interface SimulationProxy {
  advance(steps: number): void;
  frame(): {
    toJs(options: { create_pyproxies: false }): Frame;
    destroy(): void;
  };
  destroy(): void;
}
export interface WorkerScope {
  importScripts(url: string): void;
  location: Location;
  loadPyodide(options: { indexURL: string }): Promise<{
    loadPackage(name: string): Promise<void>;
    FS: { writeFile(path: string, contents: string): void };
    runPython(code: string): (parameters: string) => SimulationProxy;
  }>;
  onmessage: (event: MessageEvent<Request>) => void;
  postMessage(message: Reply, transfer?: ArrayBuffer[]): void;
}
