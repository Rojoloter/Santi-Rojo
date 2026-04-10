import { useEffect, useRef, useState } from "react";
import uPlot from "uplot";
import "uplot/dist/uPlot.min.css";

type BaseChartProps = {
  data: number[];
  startIndex: number;
  count: number;
  max: number;
  min: number;
  name: string;
  unit: string;
  line?: string;
  categroy: string;
  triggerUpdate: number;
};

export function BaseChart(props: BaseChartProps) {
  const chartRef = useRef<HTMLDivElement>(null);
  const plotRef = useRef<uPlot | null>(null);
  const tooltipRef = useRef<HTMLDivElement | null>(null);
  const [shouldRender, setShouldRender] = useState(false);
  const xBuffer = useRef<Float64Array>(new Float64Array(0));
  const yBuffer = useRef<Float64Array>(new Float64Array(0));


  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        setShouldRender(entry.isIntersecting);
      },
      { rootMargin: "10px 0px" }
    );

    if (chartRef.current) {
      observer.observe(chartRef.current);
    }

    return () => observer.disconnect();
  }, []);

  useEffect(() => { // Nos evitamos renderizar graficos que no esten en la pantalla
    if (!shouldRender || !chartRef.current) {
      if (plotRef.current) {
        plotRef.current.destroy();
        plotRef.current = null;
      }
      return;
    }

    const tooltip = document.createElement("div");
    tooltip.className = "chart-tooltip";
    tooltip.style.cssText = `
      position: absolute;
      color: white;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 12px;
      white-space: nowrap;
      pointer-events: none;
      z-index: 100;
      display: none;
      will-change: transform;
    `;
    tooltip.setAttribute("data-category", props.categroy);

    chartRef.current.appendChild(tooltip);
    tooltipRef.current = tooltip;

    const handleMouseLeave = () => {
      const allTooltips = document.querySelectorAll(`.chart-tooltip[data-category="${props.categroy}"]`);
      allTooltips.forEach((tip) => {
        (tip as HTMLElement).style.display = "none";
      });
    };

    chartRef.current.addEventListener("mouseleave", handleMouseLeave);

    const slicedData = props.data.slice(props.startIndex, props.startIndex + props.count);
    const timestamps = Array.from({ length: slicedData.length }, (_, i) => (props.startIndex + i) * 0.02);

    const opts: uPlot.Options = {
      width: chartRef.current.clientWidth,
      height: 256,
      cursor: {
        sync: {
          key: props.categroy,
          setSeries: false,
          scales: ["x", null]
        },
        drag: { x: false, y: false },
      },
      scales: {
        x: { time: false },
        y: { range: [props.min, props.max] },
      },
      series: [
        { label: "Tiempo" },
        {
          label: props.name,
          stroke: props.line || "#3b82f6",
          width: 2,
          points: { show: false },
        },
      ],
      axes: [
        {
          size: 50,
          stroke: "#888",
          values: (_, vals) => vals.map(v => `${v.toFixed(2)}s`),
        },
        {
          size: 50,
          stroke: "#888",
        },
      ],
      legend: { show: false },
      hooks: {
        setCursor: [
          (u) => {
            const tooltip = tooltipRef.current;
            if (!tooltip) return;

            const idx = u.cursor.idx;
            const left = u.cursor.left;
            const top = u.cursor.top;

            if (idx === null || idx === undefined || left === null || left === undefined) {
              tooltip.style.display = "none";
              return;
            }

            const currentValues = u.data[1];
            if (idx >= currentValues.length) {
              tooltip.style.display = "none";
              return;
            }

            const value = currentValues[idx];
            const time = u.data[0][idx];

            if (value === null || value === undefined) {
              tooltip.style.display = "none";
              return;
            }

            requestAnimationFrame(() => {
              const plotHeight = u.bbox.height / devicePixelRatio;
              const normalizedY = top !== null && top !== undefined ? top / plotHeight : 0;
              const tooltipTop = normalizedY * plotHeight;

              tooltip.style.transform = `translate(${left + 15}px, ${tooltipTop - 80}px)`;
              tooltip.style.display = "block";

              const newContent = `<div style="margin-bottom: 4px; font-weight: 600;">${props.name}</div><div style="margin-bottom: 2px;">${value.toFixed(2)} ${props.unit}</div><div style="opacity: 0.9; font-size: 11px;">${time.toFixed(2)}s</div>`;
              if (tooltip.innerHTML !== newContent) {
                tooltip.innerHTML = newContent;
              }
            });
          },
        ],
      },
    };

    const data: uPlot.AlignedData = [timestamps, slicedData];
    plotRef.current = new uPlot(opts, data, chartRef.current);

    const handleResize = () => {
      if (plotRef.current && chartRef.current) {
        plotRef.current.setSize({
          width: chartRef.current.clientWidth,
          height: 256,
        });
      }
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      chartRef.current?.removeEventListener("mouseleave", handleMouseLeave);
      if (plotRef.current) {
        plotRef.current.destroy();
        plotRef.current = null;
      }
      tooltip.remove();
      tooltipRef.current = null;
    };
  }, [props.name, props.categroy, shouldRender]);

  useEffect(() => {
    if (!plotRef.current || !shouldRender) return;

    const rawLength = props.data.length;
    const start = props.startIndex;
    const len = Math.min(props.count, rawLength - start);

    if (len <= 0) return;
    if (xBuffer.current.length !== len) {
      xBuffer.current = new Float64Array(len);
      yBuffer.current = new Float64Array(len);
    }

    const x = xBuffer.current;
    const y = yBuffer.current;
    for (let i = 0; i < len; i++) {
      x[i] = (start + i) * 0.02;
      y[i] = props.data[start + i];
    }

    plotRef.current.setData([x, y]);
    plotRef.current.setScale("y", { min: props.min, max: props.max });

  }, [props.data, props.startIndex, props.count, props.min, props.max, props.triggerUpdate, shouldRender]);

  return <div ref={chartRef} className="uplot-chart" style={{ position: "relative" }} />;
}