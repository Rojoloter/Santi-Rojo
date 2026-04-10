export interface FileFilter {
  name: string;
  extensions: string[];
}

export interface OpenFileOptions {
  properties: string[];
  filters: FileFilter[];
}

export interface OpenFileResult {
  canceled: boolean;
  filePaths: string[];
}

export interface ProcessFileResult {
  success: boolean;
  data?: unknown;
  error?: string;
}

export interface ElectronAPI {
  openFile: (options: OpenFileOptions) => Promise<OpenFileResult>;
  processFile: (filePath: string) => Promise<ProcessFileResult>;
}

declare global {
  interface Window {
    electron: ElectronAPI;
  }
}
