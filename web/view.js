export const stepsPerFrame = 1;
const iteration = document.querySelector("#iteration");
const dark = document.querySelector("#dark");
const threshold = document.querySelector("#threshold");
const format = new Intl.NumberFormat("en");
const canvas = document.querySelector("canvas");
const context = canvas?.getContext("2d");
const image = canvas && context?.createImageData(canvas.width, canvas.height);

/** @param {import("./protocol").Frame} frame */
export function draw([step, count, limit, mask]) {
  if (iteration) iteration.textContent = format.format(step);
  if (dark) dark.textContent = format.format(count);
  if (threshold) threshold.textContent = limit.toExponential(3);
  if (!context || !image) return;
  for (let i = 0; i < mask.length; i++) {
    const shade = mask[i] ? 0 : 255;
    const offset = 4 * i;
    image.data[offset] = shade;
    image.data[offset + 1] = shade;
    image.data[offset + 2] = shade;
    image.data[offset + 3] = 255;
  }
  context.putImageData(image, 0, 0);
}
