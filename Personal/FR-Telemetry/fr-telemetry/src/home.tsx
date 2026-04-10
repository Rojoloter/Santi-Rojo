import { AppSidebar } from "./components/app-sidebar"
import { BreadcrumbNav } from "./components/breadcrumb-nav"
import { Separator } from "./components/ui/separator"
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "./components/ui/sidebar"
import { HeaderControls } from "./components/header-controls"
import { useSensorData } from "./use-sensor-data"
import { SensorPage } from "./components/sensor-page"
import { useState, useEffect } from "react"
import { LoadingMessage, FileModeMessage, LiveModeMessage, DisconnectedMessage } from "./components/status-messages"
import { AboutPage } from "./components/about-page"
import { ThemeProvider } from "./components/theme-provider";
import { FileSensorData } from "./lib/sensors/sensor-data";

export default function Home() {
  const [isPaused, setIsPaused] = useState(false);
  const [currentPage, setCurrentPage] = useState<string | null>(null);
  const [loadedData, setLoadedData] = useState<FileSensorData[] | null>(null);
  const [isLoadingFile, setIsLoadingFile] = useState(false);

  const {
    setActiveCategory,
    filteredSensors,
    isConnected,
    lastUpdate,
    dataSource,
    switchToStreaming
  } = useSensorData({
    isPaused,
    fileData: loadedData
  })

  const handleDataLoaded = (data: FileSensorData[]) => {
    console.log("Data loaded from file:", data)
    setLoadedData(data)
    setIsPaused(true) // Start paused at the end
  }

  const handleCategoryClick = (category: string) => {
    setActiveCategory(category);
    setCurrentPage(category);
    if (category === "Home") {
      setCurrentPage(null);
    } else if (category === "About") {
      setCurrentPage("About"); // No sensors for About page
    } else {
      setActiveCategory(category);
      setCurrentPage(category);
    }
  }

  const handleToggleStream = () => {
    setIsPaused(!isPaused);
  }

  const handleSwitchToStreaming = () => {
    setLoadedData(null);
    switchToStreaming();
    setIsPaused(false);
  }

  useEffect(() => {
    const handleSpacePressed = (event: KeyboardEvent) => {
      if (event.code === "Space") {
        event.preventDefault();
        handleToggleStream();
      }
    }
    document.addEventListener("keydown", handleSpacePressed);
    return () => {
      document.removeEventListener("keydown", handleSpacePressed);
    }
  }, [isPaused])

  return (
    <ThemeProvider attribute="class" enableSystem={true} defaultTheme="system">
      <SidebarProvider>
        <AppSidebar onCategoryClick={handleCategoryClick} />
        <SidebarInset>
          <header className="flex h-20 shrink-0 items-center gap-2 border-b bg-sidebar px-4 transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-16">
            <div className="flex items-center gap-4 flex-1">
              <SidebarTrigger className="-ml-1" />
              <Separator
                orientation="vertical"
                className="mr-2 h-6"
              />

              {/* Site section Breadcrumb */}
              <div className="flex items-center gap-3">
                <BreadcrumbNav currentPage={currentPage} onNavigateHome={() => handleCategoryClick("Home")} />
              </div>

              {/* Stream Control Button, Load File button and Dark Mode Button */}
              <div className="ml-auto">
                <HeaderControls
                  dataSource={dataSource}
                  isPaused={isPaused}
                  onToggleStream={handleToggleStream}
                  onSwitchToStreaming={handleSwitchToStreaming}
                  onDataLoaded={handleDataLoaded}
                  onLoadingChange={setIsLoadingFile}
                />
              </div>
            </div>
          </header>

          {currentPage ? (
            currentPage === "About" ? (
              <AboutPage />
            ) : (
              <SensorPage title={currentPage} filteredSensors={filteredSensors} isConnected={isConnected} isLoadingFile={isLoadingFile} lastUpdate={lastUpdate} />
            )
          ) : (
            <div className="p-6">
              <h1 className="text-3xl font-bold mb-4">FIUBA Racing Telemetry</h1>
              <p className="text-muted-foreground">
                Datos de telemetría en tiempo real o desde archivo.
              </p>
              {dataSource === 'file' && !isLoadingFile && <FileModeMessage />}
              {dataSource === 'streaming' && isConnected && !isLoadingFile && <LiveModeMessage />}
              {dataSource === 'streaming' && !isConnected && !isLoadingFile && <DisconnectedMessage />}
              {isLoadingFile && <LoadingMessage />}
            </div>
          )}
        </SidebarInset>
      </SidebarProvider>
    </ThemeProvider>
  )
}
