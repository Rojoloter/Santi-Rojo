import {ipcMain, WebContents, WebFrameMain} from "electron";
import {getUIPath} from "./pathResolver.js";
import * as url from "node:url";

export function isDev(): boolean {
    return process.env.NODE_ENV === "development";
}

export function ipcMainHandle<Key extends keyof EventPayloadMapping>(key: Key, handler: () => EventPayloadMapping[Key]) {
    ipcMain.handle(key, (event) => {
        // @ts-expect-error WebFrameMain
        validateEventFrame(event.senderFrame);
        return handler();
    });
}

export function ipcWebContentsSend<Key extends keyof EventPayloadMapping>(key: Key, webContents: WebContents, payload: EventPayloadMapping) {
    webContents.send(key, payload);
}

export function validateEventFrame(frame: WebFrameMain) {
    if (isDev() && new URL(frame.url).host === "localhost:5123") {
        return;
    }
    if (frame.url !== url.pathToFileURL(getUIPath()).toString()) {
        throw new Error("Evento malicioso")
    }
}