import osUtils from "os-utils";
import os from "os";
import fs from "fs";
import {BrowserWindow} from "electron";
import {ipcWebContentsSend} from "./util.js";

const POLL_INT = 50; //Se actualiza cada 100ms

export function pollResources(mainWindow: BrowserWindow) {
    setInterval(async ()=>{
        const cpuUsage = await getcpuUsage();
        const ramUsage = getRamUsage();
        const storageData = getStorageData();
        ipcWebContentsSend("statistics", mainWindow.webContents,{
            // @ts-expect-error cpuUsage
            cpuUsage,
            ramUsage,
            storageUsage: storageData.usage});
    }, POLL_INT);
}

export function getStaticData() {
    const totalStorage = getStorageData().total;
    const cpuModel = os.cpus()[0].model;
    const totalMemoryGB = Math.ceil(osUtils.totalmem() / 1024);

    return {
        totalStorage,
        cpuModel,
        totalMemoryGB
    }
}

function getcpuUsage(): Promise<number> {
    return new Promise(resolve => {
        osUtils.cpuUsage(resolve);
    });
}

function getRamUsage() {
    return 1 - osUtils.freememPercentage();
}

function getStorageData() {
    const stats = fs.statfsSync(process.platform === "win32" ? "C://" : "/");
    const total = stats.bsize * stats.blocks; //Total = tamaño de cada bloque de memoria x cant. de bloques totales
    const free = stats.bsize * stats.bfree; //Libre = tamaño de cada bloque de memoria x cant. de bloques libres

    return {
        total: Math.floor(total / 1_000_000_000),
        usage: 1 - free/total
    }
}