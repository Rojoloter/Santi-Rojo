import React from 'react';
import "./charts.css"

interface SliderProps {
  value: number;
  onValueChange: (value: number) => void;
  max: number;
  min: number;
  step: number;
}

export function Slider({ value, onValueChange, max, min, step }: SliderProps) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = parseInt(e.target.value);
    onValueChange(newValue);
  };

  return (
    <input
      className={"chart-slider"}
      type="range"
      min={min}
      max={max}
      step={step}
      value={value}
      onChange={handleChange}
    />
  );
}