from Serial_Base import Controller
import serial

class OptoSigmaSRC101(Controller):
    def __init__(self, serial_option = dict()):
        self.serial_option = {
                'port': 'COM9', 'baudrate': 38400, 'parity': serial.PARITY_NONE, 'stopbits': serial.STOPBITS_ONE, 
                'bytesize': serial.EIGHTBITS
            }
        self.serial_option.update(serial_option)

    def jog_start(self, direction):
        sdire = '+' if direction else '-'
        self.send_command(f'J:1{sdire}')
        self.send_command('G:')

    def pulse_move(self, direction, number):
        sdire = '+' if direction else '-'
        self.send_command(f'M:1{sdire}P{int(number)}')
        self.send_command('G:')

    def stop_move(self):
        self.send_command('L:1')

    def change_speed(self, speed):
        speed = 1 if speed < 1 else speed
        speed = 48 if speed > 48 else speed
        self.send_command(f'S:J{int(speed)}')

    def check_status_in_detail(self):
        self.send_command('Q:')

    def check_move_status(self):
        self.send_command('!:')

    def software_version(self):
        self.send_command('?:V')

    def check_speed(self):
        self.send_command('?:S')

if __name__ == '__main__':
    speed = 24.4
    speed = 1 if speed < 1 else speed
    speed = 48 if speed > 48 else speed
    print(f'S:J{int(speed)}')