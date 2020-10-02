from Serial_Base import Controller
import serial

class PriorES10ZE(Controller):
    def __init__(self, serial_option = dict()):
        self.serial_option = {
                'port': 'COM9', 'baudrate': 9600, 'parity': serial.PARITY_NONE, 'stopbits': serial.STOPBITS_ONE, 
                'bytesize': serial.EIGHTBITS
            }
        self.serial_option.update(serial_option)
        self.position_list = [
                -1500, ## useless 
                -1370, -290, -120, -43, -51
            ]

if __name__ == '__main__':
    with PriorES10ZE() as p:
        # p.send_command('C 100')
        # p.send_command('U')
        # res = p.send_command('$')
        print(res)