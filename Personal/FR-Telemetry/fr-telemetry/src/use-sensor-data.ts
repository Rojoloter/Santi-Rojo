import { useState, useEffect, useRef } from "react";
import { SensorData, FileSensorData } from "./lib/sensors/sensor-data";

type DataSource = 'streaming' | 'file';

interface SensorDataProps {
  datapoint?: number;
  isPaused: boolean;
  fileData?: FileSensorData[] | null;
}

export function useSensorData({ isPaused, fileData }: SensorDataProps) {
  const [activeCategory, setActiveCategory] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [sensorsByCategory, setSensorsByCategory] = useState<Record<string, SensorData[]>>({});
  const initializedRef = useRef(false);
  const sensorRef = useRef<Record<string, SensorData[]>>({});
  const [lastUpdate, setLastUpdate] = useState(0);
  const [dataSource, setDataSource] = useState<DataSource>('streaming');

  const indexRef = useRef(0);
  const totalPointsRef = useRef(0);
  const dataSourceRef = useRef<DataSource>('streaming');

  useEffect(() => {
    dataSourceRef.current = dataSource;
  }, [dataSource]);

  // Reset when fileData changes
  useEffect(() => {
    if (fileData) {
      dataSourceRef.current = 'file';
      initializeFromFile(fileData);
      setDataSource('file');
      setIsConnected(true);
      initializedRef.current = true;
    }
  }, [fileData]);

  useEffect(() => {
    if (!isPaused && !initializedRef.current) {
      setSensorsByCategory({});
      sensorRef.current = {};
    }
  }, [isPaused]);

  // Initialize sensors from file data
  const initializeFromFile = (data: FileSensorData[]) => {
    sensorRef.current = {};

    let maxLen = 0;

    const sensors = data.map((sensorData) => {
      const sensor = new SensorData(
        sensorData.id,
        sensorData.name,
        sensorData.values ? [...sensorData.values] : [], // Start at the end
        sensorData.unit,
        sensorData.category
      );

      // Save all values for replay
      sensor.allValues = sensorData.values;
      sensor.timestamps = sensorData.timestamps;
      sensor.max = sensorData.max;
      sensor.min = sensorData.min;

      if (sensor.allValues && sensor.allValues.length > maxLen) {
        maxLen = sensor.allValues.length;
      }

      return sensor;
    });

    totalPointsRef.current = maxLen;

    const categorizedSensors: Record<string, SensorData[]> = {};
    sensors.forEach((sensor: SensorData) => {
      if (!categorizedSensors[sensor.category]) {
        categorizedSensors[sensor.category] = [];
      }
      categorizedSensors[sensor.category].push(sensor);
    });

    setSensorsByCategory(categorizedSensors);
    indexRef.current = Math.max(-1, maxLen - 1);
  };

  // Replay simulation for file data
  useEffect(() => {
    if (dataSource === 'file' && !isPaused && initializedRef.current) {
      const interval = setInterval(() => {
        const currentIdx = indexRef.current;

        if (currentIdx >= totalPointsRef.current - 1) {
          clearInterval(interval);
          return;
        }

        const newIndex = currentIdx + 1;
        indexRef.current = newIndex;

        setSensorsByCategory(prevCategories => {
          const updatedCategories = { ...prevCategories };
          Object.values(updatedCategories).flat().forEach(sensor => {
            if (sensor.allValues && newIndex < sensor.allValues.length) {
              sensor.setValue(sensor.allValues[newIndex]);
            }
          });
          return updatedCategories;
        });
        setLastUpdate(Date.now());
      }, 20); // Podemos controlar los fps de los graficos. En este momento, 1000/20 = 50fps. En este caso seteado para la frecuencia de 20ms de la adquisición de datos de la ECU.

      return () => clearInterval(interval);
    }
  }, [dataSource, isPaused, initializedRef]);

  // Real-time streaming
  useEffect(() => {
    if (dataSource === 'streaming' && !isPaused) {
      const fetchData = async () => {
        try {
          if (dataSourceRef.current !== 'streaming') return;

          const response = await fetch(`http://127.0.0.1:5001/api/data`);
          if (response.ok) {
            const data = await response.json();

            if (dataSourceRef.current !== 'streaming') return;

            if (!initializedRef.current) {
              const sensors = data.map((sensorData: { id: string; name: string; value: number; unit: string; category: string }) => new SensorData(
                sensorData.id,
                sensorData.name,
                [sensorData.value],
                sensorData.unit,
                sensorData.category
              ))

              const categorizedSensors: Record<string, SensorData[]> = {};
              sensors.forEach((sensor: SensorData) => {
                if (!categorizedSensors[sensor.category]) {
                  categorizedSensors[sensor.category] = [];
                }
                categorizedSensors[sensor.category].push(sensor);
              })
              sensorRef.current = categorizedSensors;
              initializedRef.current = true;
              setSensorsByCategory(categorizedSensors);
              setIsConnected(true);

            } else {
              data.forEach((sensorData: { id: string; name: string; value: number; unit: string; category: string }) => {
                const categoryArray = sensorRef.current[sensorData.category];
                if (categoryArray) {
                  const sensor = categoryArray.find(s => s.id === sensorData.id);
                  if (sensor) sensor.setValue(sensorData.value)
                }
              })
            }
          }
        } catch (e) {
          console.error("Error fetching data", e);
        }
      };

      const interval = setInterval(fetchData, 20);
      fetchData();
      return () => clearInterval(interval);
    }
  }, [isPaused, dataSource])


  const switchToStreaming = () => {
    setDataSource('streaming');
    initializedRef.current = false;
    setSensorsByCategory({});
  };

  useEffect(() => {
    if (!isPaused && dataSource === 'streaming') {
      const renderLoop = setInterval(() => {
        if (dataSourceRef.current === 'streaming' && initializedRef.current) {
          setSensorsByCategory({ ...sensorRef.current });
          setLastUpdate(Date.now());
        }
      }, 50); // Podemos controlar los fps de los graficos. En este momento, 1000/50 = 20fps. Cuanto mayor el valor, menor fps
      return () => clearInterval(renderLoop);
    }
  }, [isPaused, dataSource]);

  const filteredSensors = activeCategory ? (sensorsByCategory[activeCategory] || []) : [];

  return {
    setActiveCategory,
    filteredSensors,
    isConnected,
    lastUpdate,
    dataSource,
    switchToStreaming
  };
}