import serial
import csv
import argparse
import time
from datetime import datetime

def record_data(port, baudrate, output_file, duration_sec=None):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Recording from {port} at {baudrate} baud...")
    except Exception as e:
        print(f"Error opening port: {e}")
        return
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'vibration_x', 'vibration_y', 'vibration_z',
                         'audio', 'magnetic', 'current', 'temperature'])
        start_time = time.time()
        while True:
            if duration_sec and (time.time() - start_time) > duration_sec:
                break
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                timestamp = datetime.now().isoformat()
                writer.writerow([timestamp] + line.split(','))
                print(f"Recorded: {line}")
    
    ser.close()
    print(f"Data saved to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', required=True, help='Serial port (e.g., COM3 or /dev/ttyUSB0)')
    parser.add_argument('--baud', type=int, default=115200, help='Baud rate')
    parser.add_argument('--output', required=True, help='Output CSV file')
    parser.add_argument('--duration', type=int, help='Recording duration in seconds')
    args = parser.parse_args()
    record_data(args.port, args.baud, args.output, args.duration)
