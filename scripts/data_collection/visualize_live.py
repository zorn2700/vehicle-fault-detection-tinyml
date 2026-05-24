import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse
from collections import deque

# إعدادات الرسم البياني
WINDOW_SIZE = 100
data_buffer = deque(maxlen=WINDOW_SIZE)

def update_plot(frame, ser, ax):
    if ser.in_waiting:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            values = line.split(',')
            try:
                vib_x = float(values[0])
                data_buffer.append(vib_x)
                ax.clear()
                ax.plot(data_buffer, 'b-')
                ax.set_ylim(0, 2)
                ax.set_title('Live Vibration X-axis')
                ax.set_xlabel('Sample')
                ax.set_ylabel('Acceleration (g)')
            except:
                pass
    return ax,

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', required=True)
    parser.add_argument('--baud', type=int, default=115200)
    args = parser.parse_args()
    
    ser = serial.Serial(args.port, args.baud, timeout=1)
    fig, ax = plt.subplots()
    ani = animation.FuncAnimation(fig, update_plot, fargs=(ser, ax), interval=50)
    plt.show()
    ser.close()

if __name__ == '__main__':
    main()
