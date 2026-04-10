import { SensorData } from "../lib/sensors/sensor-data";
import { SensorChart } from "./ui/sensor-chart";
import { useState } from "react";
import { Circle, Square } from "lucide-react";
import { Slider } from "./ui/slider";
import { Button } from "./ui/button";
import { SteeringWheelRotation } from "./ui/steering-wheel";
import { LoadingMessage } from "./status-messages";

interface SensorPageProps {
  title: string;
  filteredSensors: SensorData[];
  isConnected: boolean;
  lastUpdate: number;
  isLoadingFile: boolean;
}

export function SensorPage({ title, filteredSensors, isConnected, lastUpdate, isLoadingFile }: SensorPageProps) {
  const [globalIsLive, setGlobalIsLive] = useState(true);
  const [globalViewportStart, setGlobalViewportStart] = useState(0);

  const [individualSensorStates, setIndividualSensorStates] = useState<Record<string, {
    isLive: boolean;
    viewportStart: number;
  }>>({});

  if (isLoadingFile) {
    return (
      <div className="p-6">
        <h1 className="text-3xl font-bold mb-6">{title}</h1>
        <LoadingMessage />
      </div>
    )
  }

  if (!isConnected) {
    return <div className="p-6">Sin conexión en tiempo real.</div>
  }

  const maxPoints = 300;
  const dataLength = filteredSensors.length > 0 ? filteredSensors[0].value.length : 0;
  const maxSliderValue = Math.max(0, dataLength - maxPoints);

  const handleGlobalSliderChange = (value: number) => {
    setGlobalViewportStart(value);
  }

  const handleGlobalModeToggle = () => {
    setGlobalIsLive(!globalIsLive);
  }

  const displayStart = globalIsLive ? maxSliderValue : globalViewportStart;

  const handleIndividualLiveChange = (sensorId: string, isLive: boolean) => {
    setIndividualSensorStates(prev => ({
      ...prev,
      [sensorId]: {
        ...prev[sensorId],
        isLive
      }
    }));
  };

  const handleIndividualViewportChange = (sensorId: string, start: number) => {
    setIndividualSensorStates(prev => ({
      ...prev,
      [sensorId]: {
        ...prev[sensorId],
        viewportStart: start
      }
    }));
  };

  const getSensorState = (sensorId: string) => {
    if (!individualSensorStates[sensorId]) {
      setIndividualSensorStates(prev => ({
        ...prev,
        [sensorId]: { isLive: true, viewportStart: 0 }
      }));
      return { isLive: true, viewportStart: 0 };
    }
    return individualSensorStates[sensorId];
  };

  if (title === "Posición del Volante") {
    const steeringSensor = filteredSensors[0];
    const rotation = steeringSensor && steeringSensor.value.length > 0 ? steeringSensor.value[steeringSensor.value.length - 1] : 90;

    return (
      <div className="p-6">
        <h1 className="text-3xl font-bold mb-6">{title}</h1>
        {steeringSensor ? (
          <SteeringWheelRotation rotation={rotation} />
        ) : (
          <div className="text-center text-gray-500 mt-10">
            <p>No hay sensor de posición del volante disponible.</p>
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">{title}</h1>
      <div className="mb-6 p-4 bg-gray-50 dark:bg-gray-900 rounded-lg border">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-medium">Control General</h3>
          <Button
            onClick={handleGlobalModeToggle}
            variant="outline"
            size="sm"
            className="flex items-center gap-2"
          >
            {globalIsLive ? <Square className="h-4 w-4" fill="red" /> : <Circle className="h-4 w-4" fill="grey" />}
            {globalIsLive ? "En vivo" : "Estático"}
          </Button>
        </div>

        {!globalIsLive && dataLength > maxPoints && (
          <div className="px-2">
            <Slider
              value={globalViewportStart}
              onValueChange={handleGlobalSliderChange}
              max={maxSliderValue}
              min={0}
              step={1}
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>Point {displayStart}</span>
              <span>Point {Math.min(displayStart + maxPoints, dataLength) - 1}</span>
            </div>
          </div>
        )}
      </div>

      <p className="mb-4 text-sm text-gray-600">
        Sensores disponibles: {filteredSensors.map(s => s.name).join(", ")}
      </p>

      {filteredSensors.length === 0 ? (
        <div className="text-center text-gray-500 mt-10">
          <p>No hay sensores de {title.toLowerCase()} disponibles</p>
        </div>
      ) : (
        <div className="chart-container">
          {filteredSensors.map(sensor => {
            const sensorState = getSensorState(sensor.id);
            return (
              <SensorChart
                data={sensor.value}
                triggerUpdate={lastUpdate}
                maxDataPoins={maxPoints}
                max={sensor.max}
                min={sensor.min}
                unit={sensor.unit}
                name={sensor.name}
                category={sensor.category}
                globalViewportStart={globalViewportStart}
                globalIsLive={globalIsLive}
                onGlobalSliderChange={handleGlobalSliderChange}
                onGlobalModeToggle={handleGlobalModeToggle}
                sensorId={sensor.id}
                isIndividualLive={sensorState.isLive}
                individualViewportStart={sensorState.viewportStart}
                onIndividualLiveChange={handleIndividualLiveChange}
                onIndividualViewportChange={handleIndividualViewportChange}
              />)
          })}
        </div>
      )}
    </div>
  );
}