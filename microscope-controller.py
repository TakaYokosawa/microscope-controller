import time, serial
import numpy as np

class Controller(object):
    def __init__(self):
        self.log_on()

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, trace):
        self.log_off()

    def log_on(self):
        """serial port handle"""
        self.ser = serial.Serial(
            port = self.port,
            baudrate = self.baudrate,
            parity = self.parity,
            stopbits = self.stopbits,
            bytesize=serial.EIGHTBITS
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
        return message

class PRIOR(Controller):
    def __init__(self):
        self.position_list = [
            -1500, ## useless 
            -1370, -290, -120, -43, -51]
        self.port = 'COM9'
        self.baudrate = 9600
        self.parity = serial.PARITY_NONE
        self.stopbits = serial.STOPBITS_ONE
        super().__init__()

class BX3M_CBFM(Controller):
    def __init__(self):
        self.objective_list = ['x5', 'x10', 'x20', 'x50', 'x100', 'not using']
        self.port = 'COM7'
        self.baudrate = 19200
        self.parity = serial.PARITY_EVEN
        self.stopbits = serial.STOPBITS_TWO
        super().__init__()
    
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
            pass
        elif message == '1x\r\n':
            print ('maybe no control')
            pass
        elif message.split(' ')[1] == 'E013F0120\r\n' or message.split(' ')[1] == 'E013F0130\r\n':
            print('maybe error')
        else: 
            print (command, message)
            return message

    def change_objective(self, target):
        current_index = int(self.send_command('1OB?').split(' ')[1].split('\r\n')[0])
        target_index = self.objective_list.index(target) + 1
        for i in reversed(range(target_index, current_index, np.sign(current_index - target_index) )):
            self.send_command(f'1OB {i}')
        with PRIOR() as p:
            p.send_command('C 1')
            p.send_command(f'U {p.position_list[target_index]-p.position_list[current_index]}')

with BX3M_CBFM() as b:
    b.change_objective('x5') ## choose from 'x5', 'x10', 'x20', 'x50', 'x100'

# [command]? ask status X: no control
# 1MU? 1MU X
# 1VL? 1VL X
# 1[E, S]N1? X
# 1[D, E, M]IL? X

# 1U? 1U B3M,RV.6,B3M-HS,B3M-HSRE 
# 1OB? 1OB 1-6: objective position
# 1ER? 1ER E013F0120 
