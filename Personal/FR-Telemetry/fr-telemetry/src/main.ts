import { app, BrowserWindow, dialog, ipcMain, nativeImage } from "electron"
import { spawn } from 'child_process';
import path from 'node:path';
import started from 'electron-squirrel-startup';

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (started) {
  app.quit();
}

app.setName('FR Telemetry');


const createWindow = () => {
  // Create the browser window.

  // Load icons
  let iconPath;
  if (app.isPackaged) {
    // In production, icons are in process.resourcesPath
    iconPath = path.join(process.resourcesPath, 'public', 'fiuba-racing-icon.icns');
  } else {
    // In development, use the PNG file
    iconPath = path.join(__dirname, '../../public', 'fiuba-racing-icon.png');
  }

  // Handle Windows .ico extension
  if (process.platform === 'win32') {
    iconPath = iconPath.replace('.icns', '.ico');
    iconPath = iconPath.replace('.png', '.ico');
  }

  const icon = nativeImage.createFromPath(iconPath);

  // Set icon for macOS
  if (process.platform === 'darwin') {
    app.dock.setIcon(icon);
  }

  const mainWindow = new BrowserWindow({
    width: 1000,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
      backgroundThrottling: false
    },
    icon: icon,
  });

  // and load the index.html of the app.
  if (MAIN_WINDOW_VITE_DEV_SERVER_URL) {
    mainWindow.loadURL(MAIN_WINDOW_VITE_DEV_SERVER_URL);
  } else {
    mainWindow.loadFile(
      path.join(__dirname, `../renderer/${MAIN_WINDOW_VITE_NAME}/index.html`),
    );
  }

  // Open the DevTools.
  // mainWindow.webContents.openDevTools();
};
app.whenReady().then(() => {
  createWindow();
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and import them here.

// IPC handler for opening native file dialog
ipcMain.handle("dialog:open-file", async (_, options?: Electron.OpenDialogOptions) => {
  const win = BrowserWindow.getFocusedWindow() || BrowserWindow.getAllWindows()[0]
  return await dialog.showOpenDialog(win, {
    properties: ["openFile"],
    filters: [
      { name: "All files", extensions: ["*"] },
      { name: "CSV", extensions: ["csv"] },
      { name: "JSON", extensions: ["json"] },
    ],
    ...options,
  })
})

// IPC handler to process file
ipcMain.handle("file:process-file", async (_, filePath: string) => {
  return new Promise((resolve, reject) => {

    // Script route
    const pythonScript = path.join(__dirname, '../../../backend/file_processor.py')

    // Execute Python script with platform-specific command
    const pythonCmd = process.platform === 'win32' ? 'python' : 'python3'
    const pythonProcess = spawn(pythonCmd, [pythonScript, filePath])

    let dataString = ''
    let errorString = ''

    pythonProcess.stdout.on('data', (data) => {
      dataString += data.toString()
    })
    pythonProcess.stderr.on('data', (data) => {
      errorString += data.toString()
    })
    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Python process exited with code ${code}. Error: ${errorString}. Output: ${dataString}`))
        return
      }

      try {
        const result = JSON.parse(dataString)
        resolve(result)
      } catch (error) {
        reject(new Error(`Failed to parse Python output: ${error}`))
      }
    })

    pythonProcess.on('error', (error) => {
      reject(new Error(`Failed to start Python process: ${error.message}`))
    })
  })
})
