import sys
import json

def parse_telemetry_file(file_path):
    """
    Parse telemetry data file and convert to standardized format
    """
    import csv
    from datetime import datetime

    lines = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        # Fallback to latin-1 for Windows files with special chars
        with open(file_path, "r", encoding="latin-1") as f:
            lines = f.readlines()

    registros = []
    first_time = None

    # Use DictReader on the loaded lines array
    reader = csv.DictReader(lines, skipinitialspace=True)
    for row in reader:
        if 'TIEMPO' not in row or not row['TIEMPO']:
            continue
        
        time_str = row['TIEMPO'].strip()
        try:
            # Parse HH:MM:SS.mmm
            t = datetime.strptime(time_str, "%H:%M:%S.%f")
            absolute_seconds = t.hour * 3600 + t.minute * 60 + t.second + t.microsecond / 1000000.0
        except ValueError:
            try:
                t = datetime.strptime(time_str, "%H:%M:%S")
                absolute_seconds = t.hour * 3600 + t.minute * 60 + t.second
            except ValueError:
                continue
        
        if first_time is None:
            first_time = absolute_seconds
            
        relative_time = absolute_seconds - first_time
        
        datos = {}
        
        # Check for expected ECU metrics
        if 'RPM' in row and row['RPM'].strip():
            try:
                datos['RPM'] = {"id": "RPM", "name": "RPM", "value": float(row['RPM']), "unit": "RPM", "category": "Velocidad & RPM"}
            except ValueError: pass

        if 'AFR' in row and row['AFR'].strip():
            try:
                datos['AFR'] = {"id": "AFR", "name": "AFR", "value": float(row['AFR']), "unit": "AFR", "category": "Motor"}
            except ValueError: pass

        if 'TPS' in row and row['TPS'].strip():
            try:
                datos['TPS'] = {"id": "TPS", "name": "TPS", "value": float(row['TPS']), "unit": "%", "category": "TPS & Freno"}
            except ValueError: pass

        if 'BATERIA' in row and row['BATERIA'].strip():
            try:
                datos['BATERIA'] = {"id": "BATERIA", "name": "Batería", "value": float(row['BATERIA']), "unit": "V", "category": "Motor"}
            except ValueError: pass

        if 'TEMP_MOTOR' in row and row['TEMP_MOTOR'].strip():
            try:
                datos['TEMP_MOTOR'] = {"id": "TEMP_MOTOR", "name": "Temp. Motor", "value": float(row['TEMP_MOTOR']), "unit": "°C", "category": "Motor"}
            except ValueError: pass

        registros.append({
            "tiempo": round(relative_time, 3),
            "datos": datos
        })

    return registros

def convert_to_sensor_format(registros):
    """
    Convert parsed data to the same format as streaming data
    Returns array of sensors with their time series data
    """
    # Group data by sensor ID
    sensors_map = {}
    
    for registro in registros:
        tiempo = registro["tiempo"]
        
        for key, sensor_data in registro["datos"].items():
            if "error" in sensor_data:
                continue
                
            sensor_id = sensor_data.get("id")
            if not sensor_id:
                continue

            # Initialize sensor if it doesn't exist
            if sensor_id not in sensors_map:
                sensors_map[sensor_id] = {
                    "id": sensor_data["id"],
                    "name": sensor_data["name"],
                    "category": sensor_data["category"],
                    "unit": sensor_data["unit"],
                    "values": [],
                    "timestamps": []
                }

            # Add value with timestamp
            sensors_map[sensor_id]["values"].append(sensor_data["value"])
            sensors_map[sensor_id]["timestamps"].append(tiempo)

    # Convert to list and calculate min/max
    sensors_list = []
    for sensor_id, sensor_data in sensors_map.items():
        values = sensor_data["values"]
        sensor_data["min"] = min(values) if values else 0
        sensor_data["max"] = max(values) if values else 0
        sensors_list.append(sensor_data)
    
    return sensors_list

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "No se proporcionó ruta de archivo"}))
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        registros = parse_telemetry_file(file_path)
        sensors_data = convert_to_sensor_format(registros)
        
        print(json.dumps({
            "success": True,
            "data": sensors_data
        }))
        
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }))
        sys.exit(1)
