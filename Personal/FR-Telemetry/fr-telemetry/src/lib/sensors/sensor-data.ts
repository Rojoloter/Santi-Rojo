export class SensorData {
  id: string
  name: string
  value: number[]
  unit: string
  category: string
  max: number
  min: number
  allValues?: number[] // For file data
  timestamps?: number[] // For file data

  constructor(id: string, name: string, value: number[], unit: string, category: string) {
    this.id = id;
    this.name = name;
    this.value = value;
    this.unit = unit;
    this.category = category;
    this.max = -Infinity
    this.min = Infinity
  }

  setValue(newValue: number) {
    if (newValue > this.max) {
      this.max = newValue
    }
    if (newValue < this.min) {
      this.min = newValue
    }
    this.value.push(newValue);
  }

}

export interface FileSensorData {
  id: string;
  name: string;
  values: number[];
  unit: string;
  category: string;
  max: number;
  min: number;
  timestamps: number[];
}