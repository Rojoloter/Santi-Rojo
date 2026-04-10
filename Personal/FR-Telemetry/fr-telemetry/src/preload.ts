import { contextBridge, ipcRenderer } from "electron"

// Expose API to the renderer process through the context bridge

contextBridge.exposeInMainWorld("electron", {
  // Native file open dialog
  openFile: async (options?: Electron.OpenDialogOptions) => {
    return ipcRenderer.invoke("dialog:open-file", options)
  },

  // Process file using Python script
  processFile: async (filePath: string) => {
    return ipcRenderer.invoke("file:process-file", filePath)
  }
})
