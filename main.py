import serial
import pynmea2
import sys

cog = 0
sog = 0

# Konfigurasi serial port
def serial_ports():
    
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
print(str(serial_ports()))
port = input("write port : ")

ser = serial.Serial(port, 9600, timeout=1)  # Ganti 'COM10' dengan port serial yang sesuai dan sesuaikan baud rate

try:
    while True:
        # Baca data dari port serial
        raw_data = ser.readline().decode('utf-8').strip()

        # Parsing data menggunakan pynmea2
        print(raw_data)
        try:
            msg = pynmea2.parse(raw_data)
            
            if isinstance(msg, pynmea2.GGA):
                print(f'GGA: Latitude: {msg.latitude}, Longitude: {msg.longitude}, Altitude: {msg.altitude}')

            elif isinstance(msg, pynmea2.RMC):
                print(f'RMC: Latitude: {msg.latitude}, Longitude: {msg.longitude}, Speed: {msg.spd_over_grnd}, COG : {msg.true_course}')
                if (msg.spd_over_grnd) is None:
                    sog = 0
                else:
                    sog = float(msg.spd_over_grnd)
                
                
                with open('sog.txt', 'w') as file:
                    # Menulis data ke file
                    file.write(str(sog))
                if (msg.true_course) is None:
                    cog = 0
                else:
                    cog = float(msg.true_course)
                with open('cog.txt', 'w') as file:
                    # Menulis data ke file
                    file.write(str(cog))
                
                
                
            elif isinstance(msg, pynmea2.GLL):
                print(f'GLL: Latitude: {msg.latitude}, Longitude: {msg.longitude}')
                with open('longitude.txt', 'w') as file:
                    # Menulis data ke file
                    file.write(str(msg.longitude))
                
                with open('latitude.txt', 'w') as file:
                    # Menulis data ke file
                    file.write(str(msg.latitude))
         
            

        except pynmea2.ParseError:
            print(f'Error parsing NMEA sentence: {raw_data}')

except KeyboardInterrupt:
    print('Dibatalkan oleh pengguna.')

finally:
    # Tutup koneksi serial port
    ser.close()


