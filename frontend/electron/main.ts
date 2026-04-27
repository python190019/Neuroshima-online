import { app, BrowserWindow } from "electron";

// app.disableHardwareAcceleration();

// app.commandLine.appendSwitch("disable-gpu");
// app.commandLine.appendSwitch("disable-software-rasterizer");
// app.commandLine.appendSwitch("disable-accelerated-video-decode");
// app.commandLine.appendSwitch("disable-features", "VaapiVideoDecoder,VaapiVideoDecodeLinuxGL");

function createWindow() {
  const win = new BrowserWindow({
    width: 1800,
    height: 1000,
  });

  // Load Vite dev server
  win.loadURL("http://localhost:5173");
}

app.whenReady().then(createWindow);