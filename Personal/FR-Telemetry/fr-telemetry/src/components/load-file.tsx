"use client"

import { Upload } from "lucide-react"
import { Button } from "../components/ui/button"
import { useState } from "react"
import { FileSensorData } from "../lib/sensors/sensor-data"

interface LoadFileProps {
  onDataLoaded: (data: FileSensorData[]) => void
  onLoadingChange?: (loading: boolean) => void
}

export function LoadFile({ onDataLoaded, onLoadingChange }: LoadFileProps) {
  const [loading, setLoading] = useState(false)

  const handleOpen = async () => {
    try {
      setLoading(true)
      onLoadingChange?.(true)
      const result = await window.electron.openFile({
        properties: ["openFile"],
        filters: [{ name: "Telemetry DataFiles", extensions: ["csv", "txt"] }],
      })
      if (!result.canceled && result.filePaths?.length) {
        const filePath = result.filePaths[0]
        console.log("Selected file:", filePath);

        const processResult = await window.electron.processFile(filePath)

        if (processResult.success && processResult.data) {
          console.log("File processed successfully:", processResult.data)
          onDataLoaded(processResult.data as FileSensorData[])
        } else {
          console.error("Error processing file:", processResult.error)
          alert(`Error: ${processResult.error}`)
        }
      }
    } catch (error) {
      console.error("Error:", error)
      alert(`Error loading file: ${error}`)
    } finally {
      setLoading(false)
      onLoadingChange?.(false)
    }
  }

  return (
    <Button variant="outline" size="icon" onClick={handleOpen} aria-label="Load file" disabled={loading}>
      <Upload className={`h-[1.2rem] w-[1.2rem] transition-transform ${loading ? "opacity-50 animate-pulse" : ""}`} />
    </Button>
  )
}
