// Web worker for rendering timeseries data to canvas

import { Margins, Range, WorkerMessage } from "./WorkerTypes";

// Helper function to find a nice integer tick interval
function getNiceTickInterval(range: number, maxTicks: number): number {
  const minInterval = Math.ceil(range / maxTicks);
  if (minInterval <= 1) return 1;

  const magnitude = Math.pow(10, Math.floor(Math.log10(minInterval)));
  const niceIntervals = [1, 2, 5, 10];

  for (const interval of niceIntervals) {
    const tickInterval = interval * magnitude;
    if (tickInterval >= minInterval) {
      return Math.ceil(tickInterval);
    }
  }
  return Math.ceil(niceIntervals[niceIntervals.length - 1] * magnitude * 10);
}

// Helper function to get tick positions
function getTickPositions(
  range: Range,
  width: number,
): { value: number; x: number }[] {
  const pixelsPerTick = 20; // Minimum pixels between ticks
  const maxTicks = Math.floor(width / pixelsPerTick);
  const tickInterval = getNiceTickInterval(range.max - range.min, maxTicks);

  const firstTick = Math.ceil(range.min);
  const lastTick = Math.floor(range.max);

  const ticks: { value: number; x: number }[] = [];
  for (let value = firstTick; value <= lastTick; value += tickInterval) {
    const x = (value - range.min) / (range.max - range.min);
    if (Number.isInteger(value)) {
      ticks.push({ value, x });
    }
  }

  return ticks;
}

let canvas: OffscreenCanvas | null = null;
let ctx: OffscreenCanvasRenderingContext2D | null = null;

function renderTimeseries(
  timeseries: number[],
  width: number,
  height: number,
  margins: Margins,
  xRange: Range,
  yRange: Range,
) {
  if (!ctx || !canvas) return;

  const context = ctx; // Create a stable reference to satisfy TypeScript

  // Clear canvas
  context.clearRect(0, 0, width, height);

  // Draw axes
  context.strokeStyle = "#666666";
  context.lineWidth = 1;
  context.beginPath();

  // Y axis
  context.moveTo(margins.left, margins.top);
  context.lineTo(margins.left, height - margins.bottom);

  // X axis
  context.moveTo(margins.left, height - margins.bottom);
  context.lineTo(width - margins.right, height - margins.bottom);

  context.stroke();

  // Calculate the drawing area dimensions
  const drawingWidth = width - margins.left - margins.right;
  const drawingHeight = height - margins.top - margins.bottom;

  // Set up clipping region for timeseries
  context.save();
  context.beginPath();
  context.rect(margins.left, margins.top, drawingWidth, drawingHeight);
  context.clip();

  // Set up drawing style for timeseries
  context.strokeStyle = "#2196f3";
  context.lineWidth = 2;
  context.beginPath();

  // Calculate scaling factors
  const xScale = drawingWidth / (xRange.max - xRange.min);
  const yScale = drawingHeight / (yRange.max - yRange.min);

  // Draw the path
  let isFirst = true;
  for (let i = Math.floor(xRange.min); i <= Math.ceil(xRange.max); i++) {
    if (i < 0 || i >= timeseries.length) continue;
    const value = timeseries[i];
    const x = margins.left + (i - xRange.min) * xScale;
    const y = margins.top + drawingHeight - (value - yRange.min) * yScale;
    if (isFirst) {
      context.moveTo(x, y);
      isFirst = false;
    } else {
      context.lineTo(x, y);
    }
  }

  context.stroke();

  // Remove clipping before drawing ticks
  context.restore();

  // Draw Y-axis ticks and labels
  const yTicks = getTickPositions(yRange, drawingHeight);

  context.textAlign = "right";
  context.textBaseline = "middle";
  context.fillStyle = "#666666";
  context.font = "12px Arial";

  yTicks.forEach((tick) => {
    const y = margins.top + drawingHeight - tick.x * drawingHeight;

    // Draw tick mark
    context.beginPath();
    context.moveTo(margins.left - 6, y);
    context.lineTo(margins.left, y);
    context.stroke();

    // Draw label
    context.fillText(tick.value.toString(), margins.left - 8, y);
  });

  // Draw X-axis ticks and labels
  const ticks = getTickPositions(xRange, drawingWidth);

  context.textAlign = "center";
  context.textBaseline = "top";
  context.fillStyle = "#666666";
  context.font = "12px Arial";

  ticks.forEach((tick) => {
    const x = margins.left + tick.x * drawingWidth;

    // Draw tick mark
    context.beginPath();
    context.moveTo(x, height - margins.bottom);
    context.lineTo(x, height - margins.bottom + 6);
    context.stroke();

    // Draw label
    context.fillText(tick.value.toString(), x, height - margins.bottom + 8);
  });
}

self.onmessage = (evt: MessageEvent) => {
  const message = evt.data as WorkerMessage;

  if (message.type === "initialize") {
    canvas = message.canvas;
    ctx = canvas.getContext("2d");
    if (!ctx) {
      self.postMessage({
        type: "error",
        error: "Failed to get canvas context",
      });
      return;
    }
    self.postMessage({ type: "initialized" });
    return;
  }

  if (message.type === "render") {
    const { timeseries, width, height, margins, xRange, yRange } = message;
    renderTimeseries(timeseries, width, height, margins, xRange, yRange);
    self.postMessage({ type: "render_complete" });
    return;
  }
};

export {}; // Needed for TypeScript modules
