import { Spinner } from "./ui/spinner"

export function FileModeMessage() {
  return (
    <div className="mt-4 p-4 bg-card rounded-lg">
      <p className="text-sm">Visualizando datos desde archivo</p>
    </div>
  )
}

export function LiveModeMessage() {
  return (
    <div className="mt-4 p-4 bg-card rounded-lg">
      <p className="text-sm">Visualizando datos en vivo</p>
    </div>
  )
}

export function DisconnectedMessage() {
  return (
    <div className="mt-4 p-4 bg-card rounded-lg">
      <p className="text-sm">Sin conexión en tiempo real.</p>
      <p className="text-sm">Chequéa la conexión o cargá un archivo de telemetría.</p>
    </div>
  )
}

export function LoadingMessage() {
  return (
    <div className="mt-4 p-4 bg-card rounded-lg flex items-center gap-2">
      <Spinner className="size-6 ml-2" />
      <p className="text-sm">Cargando archivo de telemetría...</p>
    </div>
  )
}
