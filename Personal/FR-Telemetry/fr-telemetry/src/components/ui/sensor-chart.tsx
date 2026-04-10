import { BaseChart } from "./base-chart";
import { useMemo } from "react";
import { Slider } from "./slider";
import { Button } from "./button";
import { Circle, Square } from "lucide-react";

export type ChartProps = {
  data: number[];
  triggerUpdate: number;
  maxDataPoins: number;
  max: number;
  min: number;
  unit: string;
  name: string;
  line?: string;
  category: string;
  globalViewportStart: number;
  globalIsLive: boolean;
  onGlobalSliderChange?: (value: number) => void;
  onGlobalModeToggle?: () => void;
  isIndividualLive: boolean;
  individualViewportStart: number;
  onIndividualLiveChange: (sensorId: string, isLive: boolean) => void;
  onIndividualViewportChange: (sensorId: string, start: number) => void;
  sensorId: string;
};

export function SensorChart(props: ChartProps) {
  const startIndex = useMemo(() => {
    if (!props.globalIsLive) {
      return props.globalViewportStart;
    } else if (props.isIndividualLive) {
      return Math.max(0, props.data.length - props.maxDataPoins);
    } else {
      return props.individualViewportStart;
    }
  }, [props.data, props.triggerUpdate, props.maxDataPoins, props.individualViewportStart, props.isIndividualLive, props.globalIsLive, props.globalViewportStart]);

  const maxSliderValue = Math.max(0, props.data.length - props.maxDataPoins);

  const handleSliderChange = (value: number) => {
    if (!props.globalIsLive) {
      props.onGlobalSliderChange?.(value);
    } else {
      props.onIndividualViewportChange(props.sensorId, value);
    }
  };

  const toggleLiveMode = () => {
    if (props.globalIsLive) {
      const currentLatestStart = Math.max(0, props.data.length - props.maxDataPoins);
      props.onIndividualViewportChange(props.sensorId, currentLatestStart);

      props.onIndividualLiveChange(props.sensorId, !props.isIndividualLive);
    }
  };

  const showSlider = (!props.globalIsLive || !props.isIndividualLive) && props.data.length > props.maxDataPoins;
  const sliderValue = !props.globalIsLive ? props.globalViewportStart : props.individualViewportStart;
  const isIndividualToggleDisabled = !props.globalIsLive;

  return (
    <div className="chart-container bg-white dark:bg-gray-800 rounded-lg p-4 border min-h-[300px] mt-4">
      <div className="flex justify-between items-center mb-4">
        <h4 className="chart-label font-medium text-lg">{props.name}</h4>
        <Button
          onClick={toggleLiveMode}
          variant="outline"
          size="sm"
          className="flex items-center gap-2"
          disabled={isIndividualToggleDisabled}
        >
          {(props.isIndividualLive && props.globalIsLive) ? <Square className="h-4 w-4" fill="red" /> : <Circle className="h-4 w-4" fill="grey" />}
          {(props.isIndividualLive && props.globalIsLive) ? "En vivo" : "Estático"}
        </Button>
      </div>

      <div className="h-64">
        <BaseChart
          data={props.data}
          startIndex={startIndex}
          count={props.maxDataPoins}
          line={props.line}
          max={props.max}
          min={props.min}
          name={props.name}
          unit={props.unit}
          categroy={props.category}
          triggerUpdate={props.triggerUpdate}
        />
      </div>

      {showSlider && (
        <div className="mt-4 px-2">
          <Slider
            value={sliderValue}
            onValueChange={handleSliderChange}
            max={maxSliderValue}
            min={0}
            step={1}
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>Point {startIndex}</span>
            <span>Point {Math.min(startIndex + props.maxDataPoins, props.data.length) - 1}</span>
          </div>
        </div>
      )}

      <div className="mt-2 text-sm text-gray-600">
        Actual: {props.data[props.data.length - 1] || 0} {props.unit}
      </div>
    </div>
  );
}