import { app, BrowserWindow } from "electron";

function createWindow() {
  const win = new BrowserWindow({
    width: 600,
    height: 400,
  });

  // Load Vite dev server
  win.loadURL("http://localhost:5173");
}

app.whenReady().then(createWindow);