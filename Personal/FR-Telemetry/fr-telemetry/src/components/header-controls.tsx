import { Button } from "./ui/button"
import { Play, Pause, Wifi, FileText } from "lucide-react"
import { LoadFile } from "./load-file"
import { ThemeToggler } from "./theme-toggler"
import { FileSensorData } from "../lib/sensors/sensor-data";

interface HeaderControlsProps {
  dataSource: 'streaming' | 'file'
  isPaused: boolean
  onToggleStream: () => void
  onSwitchToStreaming: () => void
  onDataLoaded: (data: FileSensorData[]) => void
  onLoadingChange: (loading: boolean) => void
}

export function HeaderControls({
  dataSource,
  isPaused,
  onToggleStream,
  onSwitchToStreaming,
  onDataLoaded,
  onLoadingChange
}: HeaderControlsProps) {
  return (
    <div className="flex items-center gap-4">
      {/* Data source indicator */}
      <div className="flex items-center gap-2 text-xs text-muted-foreground">
        {dataSource === 'streaming' ? (
          <><Wifi className="h-3 w-3" /> Live</>
        ) : (
          <><FileText className="h-3 w-3" /> File</>
        )}
      </div>

      {/* Button to toggle play/pause */}
      <Button
        onClick={onToggleStream}
        variant="outline"
        size="icon"
        className="flex items-center gap-2"
      >
        {isPaused ? <Play className="h-[1.2rem] w-[1.2rem]" fill={"#2bba04"} /> : <Pause className="h-[1.2rem] w-[1.2rem]" />}
      </Button>

      {/* Button to switch to streaming */}
      <Button
        onClick={onSwitchToStreaming}
        variant="outline"
        size="icon"
        disabled={dataSource === 'streaming'}
        className="flex items-center gap-2"
      >
        <Wifi className={`h-[1.2rem] w-[1.2rem] transition-transform ${dataSource === 'streaming' ? "opacity-50 animate-pulse" : ""}`} />
      </Button>

      {/* Button to load file */}
      <LoadFile onDataLoaded={onDataLoaded} onLoadingChange={onLoadingChange} />

      {/* Dark Mode Toggler */}
      <ThemeToggler />
    </div>
  )
}
