import { useEffect, useState, useMemo, useRef, useReducer } from "react";
import { useTimeseriesData } from "../../hooks/useTimeseriesData";
import { Dataset } from "../../types";
import { Margins, Range, WorkerMessage } from "./WorkerTypes";
import { timeseriesViewReducer, initialState } from "./timeseriesViewReducer";

interface TimeseriesViewProps {
  width: number;
  height: number;
  dataset: Dataset;
}

const TimeseriesView: React.FC<TimeseriesViewProps> = ({
  width,
  height,
  dataset,
}) => {
  const { data, error } = useTimeseriesData(dataset);

  const [canvasElement, setCanvasElement] = useState<HTMLCanvasElement | null>(
    null,
  );
  const [overlayCanvasElement, setOverlayCanvasElement] =
    useState<HTMLCanvasElement | null>(null);
  const [state, dispatch] = useReducer(timeseriesViewReducer, initialState);
  const { selectedIndex, isDragging, lastDragX, xRange } = state;

  const containerRef = useRef<HTMLDivElement>(null);
  const [worker, setWorker] = useState<Worker | null>(null);
  const [margins] = useState<Margins>({
    left: 50,
    right: 20,
    top: 20,
    bottom: 50,
  });

  // Update xRange when data changes
  useEffect(() => {
    if (data) {
      dispatch({
        type: "SET_X_RANGE",
        range: { min: 0, max: data.length - 1 },
      });
    }
  }, [data]);

  // Set up wheel event listener
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const handleWheel = (e: WheelEvent) => {
      if (!data) return;
      e.preventDefault();

      const rect = container.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const xRatio =
        (x - margins.left) / (width - margins.left - margins.right);

      // Calculate zoom center in data coordinates
      const zoomCenter = xRange.min + (xRange.max - xRange.min) * xRatio;

      // Calculate new range
      const zoomFactor = e.deltaY > 0 ? 1.1 : 0.9;

      // Ensure we don't zoom out beyond data bounds
      const newMin = Math.max(
        0,
        zoomCenter - (zoomCenter - xRange.min) * zoomFactor,
      );
      const newMax = Math.min(
        data.length - 1,
        zoomCenter + (xRange.max - zoomCenter) * zoomFactor,
      );

      dispatch({ type: "SET_X_RANGE", range: { min: newMin, max: newMax } });
    };

    container.addEventListener("wheel", handleWheel, { passive: false });
    return () => {
      container.removeEventListener("wheel", handleWheel);
    };
  }, [data, width, margins, xRange]);

  // Set up mouse event listeners for panning
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const handleMouseDown = (e: MouseEvent) => {
      dispatch({ type: "SET_IS_DRAGGING", isDragging: true });
      dispatch({ type: "SET_LAST_DRAG_X", x: e.clientX });
    };

    const handleMouseMove = (e: MouseEvent) => {
      if (!isDragging || lastDragX === 0 || !data) return;

      const deltaX = e.clientX - lastDragX;
      const xRatio = deltaX / (width - margins.left - margins.right);
      const dataDelta = (xRange.max - xRange.min) * xRatio;

      if (xRange.min - dataDelta < 0) return;
      if (xRange.max - dataDelta > data.length - 1) return;

      const newMin = xRange.min - dataDelta;
      const newMax = xRange.max - dataDelta;

      // Only update if we're still within bounds
      if (newMin >= 0 && newMax <= data.length - 1) {
        dispatch({ type: "SET_X_RANGE", range: { min: newMin, max: newMax } });
      }

      dispatch({ type: "SET_LAST_DRAG_X", x: e.clientX });
    };

    const handleMouseUp = () => {
      dispatch({ type: "SET_IS_DRAGGING", isDragging: false });
      dispatch({ type: "SET_LAST_DRAG_X", x: 0 });
    };

    container.addEventListener("mousedown", handleMouseDown);
    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);

    return () => {
      container.removeEventListener("mousedown", handleMouseDown);
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, [data, width, margins, xRange, isDragging, lastDragX]);

  // Set worker
  useEffect(() => {
    if (!canvasElement) return;
    const worker = new Worker(
      new URL("./TimeseriesViewWorker", import.meta.url),
      {
        type: "module",
      },
    );
    let offscreenCanvas: OffscreenCanvas;
    try {
      offscreenCanvas = canvasElement.transferControlToOffscreen();
    } catch (err) {
      console.warn(err);
      console.warn(
        "Unable to transfer control to offscreen canvas (expected during dev)",
      );
      return;
    }
    const msg: WorkerMessage = {
      type: "initialize",
      canvas: offscreenCanvas,
    };
    worker.postMessage(msg, [offscreenCanvas]);

    setWorker(worker);

    return () => {
      worker.terminate();
    };
  }, [canvasElement]);

  // Calculate yRange from data
  const yRange = useMemo<Range>(() => {
    if (!data) return { min: 0, max: 1 };
    return {
      min: Math.min(...data),
      max: Math.max(...data),
    };
  }, [data]);

  // Handle dimension changes
  useEffect(() => {
    if (!worker) return;
    if (!data) return;

    const msg: WorkerMessage = {
      type: "render",
      timeseries: data,
      width,
      height,
      margins,
      xRange,
      yRange,
    };
    worker.postMessage(msg);
  }, [width, height, data, worker, margins, xRange, yRange]);

  // Render cursor on overlay canvas
  useEffect(() => {
    if (!overlayCanvasElement || selectedIndex === null || !data) return;
    const ctx = overlayCanvasElement.getContext("2d");
    if (!ctx) return;

    // Clear overlay canvas
    ctx.clearRect(0, 0, width, height);

    // Draw cursor line
    const xRatio = (selectedIndex - xRange.min) / (xRange.max - xRange.min);
    const x = margins.left + xRatio * (width - margins.left - margins.right);
    ctx.beginPath();
    ctx.strokeStyle = "#ff0000";
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 4]);
    ctx.moveTo(x, margins.top);
    ctx.lineTo(x, height - margins.bottom);
    ctx.stroke();
  }, [
    selectedIndex,
    overlayCanvasElement,
    width,
    height,
    margins,
    data,
    xRange,
  ]);

  if (error) {
    return <div>Error loading data: {error}</div>;
  }

  const handleCanvasClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!overlayCanvasElement || !data || isDragging) return;
    const rect = overlayCanvasElement.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const xRatio = (x - margins.left) / (width - margins.left - margins.right);
    const index = Math.round(xRange.min + xRatio * (xRange.max - xRange.min));
    if (index >= 0 && index < data.length) {
      dispatch({ type: "SET_SELECTED_INDEX", index });
    }
  };

  return (
    <div style={{ position: "relative", width, height: height + 30 }}>
      <div
        ref={containerRef}
        style={{ position: "relative", width, height }}
        onClick={handleCanvasClick}
      >
        <canvas
          ref={setCanvasElement}
          width={width}
          height={height}
          style={{
            position: "absolute",
            width: "100%",
            height: "100%",
          }}
        />
        <canvas
          ref={setOverlayCanvasElement}
          width={width}
          height={height}
          style={{
            position: "absolute",
            width: "100%",
            height: "100%",
            pointerEvents: "none",
          }}
        />
      </div>
      {selectedIndex !== -1 && data && (
        <div style={{ height: 30, padding: "5px 0", color: "#666" }}>
          Index: {selectedIndex}, Value: {data[selectedIndex].toFixed(3)}
        </div>
      )}
    </div>
  );
};

export default TimeseriesView;
