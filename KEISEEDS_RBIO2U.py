from Serial_Base import Controller
import serial

class KEISEEDS_RBIO2U(Controller):
    def __init__(self, serial_option = dict()):
        self.serial_option = {
                'port': 'COM9', 'baudrate': 9600, 'parity': serial.PARITY_NONE, 'stopbits': serial.STOPBITS_ONE, 
                'bytesize': serial.EIGHTBITS, 'rtscts': True
            }
        self.serial_option.update(serial_option)

    def change_relay(self, relay_number):
        """
        docstring
        """
        command_list = [f'R{i}{int(i == relay_number)}' for i in range(9)]
        self.send_command('PC'+''.join(command_list))

if __name__ == '__main__':
    command_list = [f'R{i}{int(i == 3)}' for i in range(9)]
    print('PC'+''.join(command_list))