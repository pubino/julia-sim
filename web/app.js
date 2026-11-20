import { draw, stepsPerFrame } from "./view.js";

/**
 * @template {Element} T
 * @param {string} id
 * @param {{new(): T}} constructor
 */
function find(id, constructor) {
  const element = document.getElementById(id);
  if (!(element instanceof constructor)) throw new Error(`Missing element ${id}`);
  return element;
}

const settings = find("settings", HTMLFormElement);
const inputs = find("inputs", HTMLFieldSetElement);
const play = find("play", HTMLButtonElement);
const step = find("step", HTMLButtonElement);
const reset = find("reset", HTMLButtonElement);
const status = find("status", HTMLElement);
const loading = find("loading", HTMLElement);
const error = find("error", HTMLElement);
const retry = find("retry", HTMLButtonElement);

const worker = new Worker(new URL("./worker.js", import.meta.url));
let running = false;
let pending = false;
let failed = false;
let hasFrame = false;
let currentStep = 0;
let animation = 0;
let generation = 0;

function scheduleFrame() {
  if (!running || pending || animation) return;
  animation = window.setTimeout(() => {
    animation = 0;
    advance(stepsPerFrame);
  }, 100);
}

/** @param {boolean} value @param {string} message */
function setRunning(value, message) {
  running = value;
  inputs.disabled = value;
  play.textContent = value ? "Pause" : (currentStep ? "Resume" : "Start");
  step.disabled = value || pending || failed;
  status.textContent = message;
  if (value) {
    scheduleFrame();
  } else {
    window.clearTimeout(animation);
    animation = 0;
  }
}

/** @param {number} steps */
function advance(steps) {
  if (pending || failed || !hasFrame) return;
  pending = true;
  step.disabled = true;
  send({ type: "advance", id: generation, steps });
}

/** @param {import("./protocol").Request} message */
function send(message) {
  worker.postMessage(message);
}

function resetSimulation() {
  setRunning(false, "Preparing the simulation…");
  error.hidden = true;
  if (!settings.reportValidity()) {
    pending = false;
    failed = true;
    generation++;
    play.disabled = true;
    step.disabled = true;
    reset.disabled = false;
    status.textContent = "Correct the highlighted field.";
    return;
  }
  currentStep = 0;
  pending = true;
  failed = false;
  generation++;
  play.disabled = true;
  step.disabled = true;
  reset.disabled = true;
  send({
    type: "reset", id: generation,
    parameters: Array.from(inputs.querySelectorAll("input"), (input) => input.valueAsNumber),
  });
}

function showFatal() {
  worker.terminate();
  setRunning(false, "");
  inputs.disabled = true;
  play.disabled = true;
  step.disabled = true;
  reset.disabled = true;
  error.textContent = "Python could not load. Reload the simulator to try again.";
  error.hidden = false;
  loading.textContent = "Simulation unavailable";
  retry.hidden = false;
}

worker.onerror = showFatal;
worker.onmessage = (/** @type {MessageEvent<import("./protocol").Reply>} */ { data }) => {
  if (data.type === "ready") {
    resetSimulation();
    return;
  }
  if (data.type === "fatal") {
    showFatal();
    return;
  }
  if (!("id" in data) || generation !== data.id) return;
  pending = false;
  if (data.type === "failed") {
    failed = true;
    setRunning(false, "Ready to reset.");
    play.disabled = true;
    reset.disabled = false;
    error.textContent = data.message;
    error.hidden = false;
    loading.hidden = true;
    return;
  }

  currentStep = data.frame[0];
  hasFrame = true;
  draw(data.frame);
  if (data.type === "reset") {
    loading.hidden = true;
    play.disabled = false;
    reset.disabled = false;
    setRunning(false, "Ready to start.");
  } else if (running) {
    scheduleFrame();
  } else {
    play.textContent = "Resume";
    step.disabled = false;
  }
};

settings.addEventListener("submit", (event) => {
  event.preventDefault();
  if (!play.disabled) setRunning(!running, running ? "Paused." : "Running…");
});
inputs.addEventListener("change", resetSimulation);
step.addEventListener("click", () => {
  status.textContent = "Paused.";
  advance(1);
});
reset.addEventListener("click", resetSimulation);
retry.addEventListener("click", () => window.location.reload());
