import {useMemo, useState} from 'react'
import './App.css'
import {useStatistics} from "./useStatistics.ts";
import {Chart} from "./Charts.tsx";

function App() {
  const [count, setCount] = useState(0);
  const statistics = useStatistics(10);
  const cpuUsages = useMemo(() => statistics.map(stat => stat.cpuUsage), [statistics]);
  const ramUsages = useMemo(() => statistics.map(stat => stat.ramUsage), [statistics]);
    const memUsages = useMemo(() => statistics.map(stat => stat.storageUsage), [statistics]);

  return (
      <div className="App">
          <div className="main">
              <div className="mainGrid">
                  <Chart label="CPU Usage" data={cpuUsages} maxDataPoins={10} fill="#3b82f6" line="#479DB8"/>
                  <Chart label="RAM Usage" data={ramUsages} maxDataPoins={10} fill="#8A6D46" line="#DE6F2F"/>
                  <Chart label="Storage Used" data={memUsages} maxDataPoins={10} fill="#8E3B96" line="#C72FDE"/>
              </div>
          </div>
      </div>
  )
}

export default App
