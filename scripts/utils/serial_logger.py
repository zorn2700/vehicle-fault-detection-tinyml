import serial
import csv
import sys

def log_serial(port, baudrate, output_csv):
    ser = serial.Serial(port, baudrate, timeout=1)
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'sensor', 'value'])
        while True:
            line = ser.readline().decode().strip()
            if line:
                writer.writerow([pd.Timestamp.now(), line])
                print(line)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: serial_logger.py <port> <baudrate> <output.csv>")
    else:
        log_serial(sys.argv[1], int(sys.argv[2]), sys.argv[3])
