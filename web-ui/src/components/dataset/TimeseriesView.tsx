import { useEffect, useMemo, useReducer, useState } from "react";
import { SupportedTypedArray } from "../../hooks/TimeseriesDataClient";
import { useTimeseriesDataClient } from "../../hooks/useTimeseriesDataClient";
import { Dataset } from "../../types";
import { Margins, Range, WorkerMessage } from "./WorkerTypes";
import { initialState, timeseriesViewReducer } from "./timeseriesViewReducer";

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
  const { client, error: clientError } = useTimeseriesDataClient(dataset);
  const [dataT, setDataT] = useState<number[] | null>(null);
  const [dataY, setDataY] = useState<SupportedTypedArray | null>(null);
  const [error, setError] = useState<string | null>(clientError);
  const [isLoading, setIsLoading] = useState(false);

  const [canvasElement, setCanvasElement] = useState<HTMLCanvasElement | null>(
    null,
  );
  const [overlayCanvasElement, setOverlayCanvasElement] =
    useState<HTMLCanvasElement | null>(null);
  const [state, dispatch] = useReducer(timeseriesViewReducer, initialState);
  const { selectedIndex, isDragging, lastDragX, xRange } = state;

  const [container, setContainer] = useState<HTMLDivElement | null>(null);
  const [worker, setWorker] = useState<Worker | null>(null);
  const [margins] = useState<Margins>({
    left: 50,
    right: 20,
    top: 20,
    bottom: 50,
  });

  // Load data for current range
  useEffect(() => {
    if (!client || !xRange) return;

    const loadRangeData = async () => {
      try {
        setIsLoading(true);
        const start = Math.floor(xRange.min);
        const end = Math.ceil(xRange.max) + 1;
        const rangeData = await client.fetchRange(start, end);
        setDataY(rangeData);
        const dT = Array.from(
          { length: rangeData.length },
          (_, i) => i + start,
        );
        setDataT(dT);
        setError(null);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to load data range",
        );
      } finally {
        setIsLoading(false);
      }
    };

    loadRangeData();
  }, [client, xRange]);

  // Update xRange when client is initialized
  useEffect(() => {
    if (client) {
      const shape = client.getShape();
      dispatch({
        type: "SET_X_RANGE",
        range: { min: 0, max: Math.min(999, shape - 1) },
      });
    }
  }, [client]);

  // Set up wheel event listener
  useEffect(() => {
    if (!container || !client) return;

    const handleWheel = (e: WheelEvent) => {
      e.preventDefault();

      const rect = container.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const xRatio =
        (x - margins.left) / (width - margins.left - margins.right);

      // Calculate zoom center in data coordinates
      const zoomCenter = xRange.min + (xRange.max - xRange.min) * xRatio;

      // Calculate new range
      const zoomFactor = e.deltaY > 0 ? 1.02 : 1 / 1.02;
      const shape = client.getShape();

      // Ensure we don't zoom out beyond data bounds
      const newMin = Math.max(
        0,
        zoomCenter - (zoomCenter - xRange.min) * zoomFactor,
      );
      const newMax = Math.min(
        shape - 1,
        zoomCenter + (xRange.max - zoomCenter) * zoomFactor,
      );

      dispatch({ type: "SET_X_RANGE", range: { min: newMin, max: newMax } });
    };

    container.addEventListener("wheel", handleWheel, { passive: false });
    return () => {
      container.removeEventListener("wheel", handleWheel);
    };
  }, [container, client, width, margins, xRange]);

  // Set up mouse event listeners for panning
  useEffect(() => {
    if (!container || !client) return;

    const handleMouseDown = (e: MouseEvent) => {
      dispatch({ type: "SET_IS_DRAGGING", isDragging: true });
      dispatch({ type: "SET_LAST_DRAG_X", x: e.clientX });
    };

    const handleMouseMove = (e: MouseEvent) => {
      if (!isDragging || lastDragX === 0) return;

      const deltaX = e.clientX - lastDragX;
      const xRatio = deltaX / (width - margins.left - margins.right);
      const dataDelta = (xRange.max - xRange.min) * xRatio;
      const shape = client.getShape();

      if (xRange.min - dataDelta < 0) return;
      if (xRange.max - dataDelta > shape - 1) return;

      const newMin = xRange.min - dataDelta;
      const newMax = xRange.max - dataDelta;

      // Only update if we're still within bounds
      if (newMin >= 0 && newMax <= shape - 1) {
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
  }, [container, client, width, margins, xRange, isDragging, lastDragX]);

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
    if (!dataY) return { min: 0, max: 1 };
    const values = Array.from(dataY);
    return {
      min: Math.min(...values),
      max: Math.max(...values),
    };
  }, [dataY]);

  // Handle dimension changes
  useEffect(() => {
    if (!worker) return;
    if (!dataY) return;
    if (!dataT) return;

    const msg: WorkerMessage = {
      type: "render",
      timeseriesT: dataT,
      timeseriesY: Array.from(dataY),
      width,
      height,
      margins,
      xRange,
      yRange,
    };
    console.log("--- posting message to worker", msg);
    worker.postMessage(msg);
  }, [width, height, dataT, dataY, worker, margins, xRange, yRange]);

  // Render cursor on overlay canvas
  useEffect(() => {
    if (!overlayCanvasElement || selectedIndex === null || !dataY) return;
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
    dataT,
    dataY,
    xRange,
  ]);

  const selectedValue = useMemo(() => {
    if (selectedIndex === -1 || !dataT || !dataY) return null;
    for (let i = 0; i < dataT.length; i++) {
      if (dataT[i] === selectedIndex) {
        return dataY[i];
      }
    }
    return null;
  }, [selectedIndex, dataT, dataY]);

  if (error || clientError) {
    return <div>Error loading data: {error || clientError}</div>;
  }

  if (isLoading && !dataY) {
    return <div>Loading...</div>;
  }

  const handleCanvasClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!overlayCanvasElement || !dataY || isDragging) return;
    const rect = overlayCanvasElement.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const xRatio = (x - margins.left) / (width - margins.left - margins.right);
    const index = Math.round(xRange.min + xRatio * (xRange.max - xRange.min));
    if (index >= 0) {
      dispatch({ type: "SET_SELECTED_INDEX", index });
    }
  };

  return (
    <div style={{ position: "relative", width, height: height + 30 }}>
      <div
        ref={setContainer}
        style={{ position: "relative", width, height }}
        onClick={handleCanvasClick}
      >
        <canvas
          ref={setCanvasElement}
          key={`canvas-${width}-${height}`}
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
      {selectedIndex !== -1 && dataY && (
        <div style={{ height: 30, padding: "5px 0", color: "#666" }}>
          Index: {selectedIndex}, Value: {selectedValue?.toFixed(3)}
        </div>
      )}
    </div>
  );
};

export default TimeseriesView;
