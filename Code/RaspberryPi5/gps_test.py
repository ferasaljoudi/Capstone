import serial
import os

# Open the GPS serial port
gps_port = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)

# Variable to track the last state of the speed
speed_above_20 = None

# Audio file path
file1 = "speed_over_20km.mp3"
file2 = "speed_below_20km.mp3"

try:
    while True:
        # Read a line of data from the GPS module
        line = gps_port.readline().decode('ascii', errors='ignore')
        
        # Check for the line that contains the GPVTG sentence (it contains speed)
        if line.startswith('$GPVTG'):
            parts = line.split(',')
            
            # Extract the speed in km/h (field index 7 in GPVTG)
            if len(parts) > 7 and parts[7]:
                speed_kmh = float(parts[7])
                
                if speed_kmh > 20 and speed_above_20 != True:
                    os.system(f"mpg321 {file1}")
                    speed_above_20 = True
                elif speed_kmh <= 20 and speed_above_20 != False:
                    os.system(f"mpg321 {file2}")
                    speed_above_20 = False

except KeyboardInterrupt:
    print("Monitoring stopped.")
finally:
    gps_port.close()