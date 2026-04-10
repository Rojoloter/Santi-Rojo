import time
from flask import Flask, jsonify
from flask_cors import CORS
import threading
import logging
import serial
import re
import platform

app = Flask(__name__)
CORS(app)

BAUDRATE = 115200
#Se pueden modificar los puertos si se quieren crear en otro lado
VIRTUAL_PORT_ARDUINO_LINUX = '/tmp/ttyArduino'
VIRTUAL_PORT_READER_LINUX = '/tmp/ttyReader'
VIRTUAL_PORT_ARDUINO_WINDOWS = "COM10"
VIRTUAL_PORT_READER_WINDOWS = "COM11"


def parse_json_string(json_str):
    pattern = r"'([^']+)':\s*([^,}]+)"
    matches = re.findall(pattern, json_str)

    result = {}
    for key, value in matches:
        if value.startswith("'") and value.endswith("'"):
            result[key] = value[1:-1]
        else:
            try:
                if '.' in value:
                    result[key] = float(value)
                else:
                    result[key] = int(value)
            except ValueError:
                result[key] = value

    return result


class Reader:
    def __init__(self):
        port = VIRTUAL_PORT_READER_WINDOWS if platform.system() == 'Windows' else VIRTUAL_PORT_READER_LINUX
        self.ser = serial.Serial(
            port=port,
            baudrate=BAUDRATE,
            timeout=1,
        )
        time.sleep(0.1)

    def read_line(self):
        line = self.ser.readline().decode().strip()

        json_pattern = r'\{[^}]+\}'
        json_objects = re.findall(json_pattern, line)

        res = []
        for json_obj in json_objects:
            parsed_obj = parse_json_string(json_obj)
            res.append(parsed_obj)

        return res

latest_data = []

@app.route('/api/data')
def get_data():
    return jsonify(latest_data)

def run_flask():
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)

    app.run(debug=True, port=5001, host="127.0.0.1", use_reloader=False)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    try:
        try:
            reader = Reader()
            while True:
                try:
                    latest_data = reader.read_line()
                except Exception as e:
                    print(f"[API] Error reading from serial: {e}")
                    time.sleep(1)
        except Exception as e:
            print(f"\n[API] Could not connect to the live telemetry serial port ({e}).")
            print("[API] The application will continue running in file mode / without live connection.\n")
            
            # Block the main thread, waiting for the daemon Flask thread
            flask_thread.join()
    except KeyboardInterrupt:
        pass