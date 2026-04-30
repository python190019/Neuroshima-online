import { app, BrowserWindow } from "electron";

// // app.disableHardwareAcceleration();

// // app.commandLine.appendSwitch("disable-gpu");
// // app.commandLine.appendSwitch("disable-software-rasterizer");
// // app.commandLine.appendSwitch("disable-accelerated-video-decode");
// // app.commandLine.appendSwitch("disable-features", "VaapiVideoDecoder,VaapiVideoDecodeLinuxGL");

// function createWindow() {
//   const win = new BrowserWindow({
//     width: 1800,
//     height: 1000,
//   });

//   // Load Vite dev server
//   win.loadURL("http://localhost:5173");
// }

// app.whenReady().then(createWindow);

// const { app, BrowserWindow } = require("electron");

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 700,
  });

  mainWindow.loadURL("http://localhost:5173");
  mainWindow.webContents.openDevTools();
}

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});