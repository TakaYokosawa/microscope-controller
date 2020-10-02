import time, serial

class Controller(object):
    def __init__(self):
        self.serial_option = {
                'port': self.port, 'baudrate': self.baudrate, 'parity': self.parity, 'stopbits': self.stopbits, 
                'bytesize': serial.EIGHTBITS
            }
        self.delimiter = '\r\n'

    def __enter__(self):
        self.log_on()
        return self

    def __exit__(self, ex_type, ex_value, trace):
        self.log_off()

    def log_on(self):
        """serial port handle"""
        self.ser = serial.Serial(
            **self.serial_option
        )

    def log_off(self):
        """close the port"""
        self.ser.close()

    def send_command(self, command):
        """ Send a text command"""
        self.ser.write((command+'\r\n').encode())
        time.sleep(0.2)
        message = self.ser.read(self.ser.inWaiting()).decode()
        while not message:
            time.sleep(0.2)
            message = self.ser.read(self.ser.inWaiting()).decode()
            print('waiting for reply...')
        print (command, message)
        return message
