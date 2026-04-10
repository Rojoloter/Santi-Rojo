interface SteeringWheelProps {
  rotation: number
}

export function SteeringWheelRotation({ rotation }: SteeringWheelProps) {
  return (
    <div className="flex flex-col items-center justify-center p-6">
      <div className="relative w-64 h-64 md:w-80 md:h-80">
        <img
          src="/car-steering-wheel-free-png.png"
          alt="Steering Wheel"
          className="w-full h-full transition-transform duration-75 ease-linear"
          style={{
            transform: `rotate(${rotation - 90}deg)`,
          }}
        />
      </div>
      <p className="mt-4 text-2xl font-bold">{rotation - 90}°</p>
    </div>
  );
}