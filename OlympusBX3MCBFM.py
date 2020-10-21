from Serial_Base import Controller
import serial
import numpy as np

class OlympusBX3MCBFM(Controller):
    def __init__(self, serial_option = dict()):
        self.serial_option = {
                'port': 'COM7', 'baudrate': 19200, 'parity': serial.PARITY_EVEN, 'stopbits': serial.STOPBITS_TWO, 
                'bytesize': serial.EIGHTBITS
            }
        self.serial_option.update(serial_option)
        self.objective_list = ['x5', 'x10', 'x20', 'x50', 'x100', 'not using']
    
    def log_on(self):
        super().log_on()
        self.send_command('1L 2')

    def log_off(self):
        """ turn off remote control of microscope, close the port"""
        self.send_command('1L 0')
        super().log_off()

    def send_command(self, command):
        """ Send a text command to the microscope controller"""
        message = super().send_command(command)
        if message == 'x\r\n':
            print ('Maybe no command')
        elif message == '1x\r\n':
            print ('maybe no control')
        elif 'E013F01' in message.split(' ')[1]:
            print('maybe error')
        # elif message.split(' ')[1] == 'E013F0120\r\n' \
        #         or message.split(' ')[1] == 'E013F0130\r\n':
        #     print('maybe error')
        return message

    def change_objective(self, target):
        current_index = self.current_objective()
        target_index = self.objective_list.index(target) + 1
        if not current_index == target_index:
            for i in reversed(range(
                        target_index, current_index, 
                        np.sign(current_index - target_index) 
                    )):
                self.send_command(f'1OB {i}')
        return current_index, target_index

    def current_objective(self):
        return int(self.send_command('1OB?').split(' ')[1].split('\r\n')[0])

if __name__ == '__main__':
    with OlympusBX3MCBFM() as B:
        B.current_objective()

## error due to bad contact

## TODO?
# look for reset command



# [command]? ask status X: no control
# 1MU? 1MU X
# 1VL? 1VL X
# 1[E, S]N1? X
# 1[D, E, M]IL? X

# 1U? 1U B3M,RV.6,B3M-HS,B3M-HSRE 
# 1OB? 1OB 1-6: objective position
# 1ER? 1ER E013F0120 
