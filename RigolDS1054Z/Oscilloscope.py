from RigolDS1054Z.RigolDS1054Z import RigolDS1054Z
from time import sleep

class Channel:
    def __init__(self) -> None:
        self.x_increment = None
        self.x_origin = None 
        self.x_reference = None
        self.y_increment = None
        self.y_origin = None
        self.y_reference = None

class Oscilloscope:
    def __init__(self) -> None:
        self.format = None
        self.type = None
        self.points = None 
        self.count_avg = None
        self.channel1 = Channel()
        self.channel2 = Channel()
        self.channel3 = Channel()
        self.channel4 = Channel()
        self.active_channel = None
        self.rigol = RigolDS1054Z('TCPIP::192.168.123.2::INSTR', read_termination='\n', timeout=100_000)

    def get_info(self,channel):
        data = self.rigol.get_waveform_parameters().split(',')
        self.format = self.get_format(data[0])
        self.type = self.get_type(data[1])
        self.points = float(data[2])
        self.count_avg = float(data[3])
        if channel == 'CHAN1':
            self.channel1.x_increment = float(data[4])
            self.channel1.x_origin = float(data[5])
            self.channel1.x_reference = float(data[6])
            self.channel1.y_increment = float(data[7])
            self.channel1.y_origin = float(data[8])
            self.channel1.y_reference = float(data[9])
            self.active_channel = self.channel1
        elif channel == 'CHAN2':
            self.channel2.x_increment = float(data[4])
            self.channel2.x_origin = float(data[5])
            self.channel2.x_reference = float(data[6])
            self.channel2.y_increment = float(data[7])
            self.channel2.y_origin = float(data[8])
            self.channel2.y_reference = float(data[9])
            self.active_channel = self.channel2
        elif channel == 'CHAN3':
            self.channel3.x_increment = float(data[4])
            self.channel3.x_origin = float(data[5])
            self.channel3.x_reference = float(data[6])
            self.channel3.y_increment = float(data[7])
            self.channel3.y_origin = float(data[8])
            self.channel3.y_reference = float(data[9])
            self.active_channel = self.channel3
        elif channel == 'CHAN4':
            self.channel4.x_increment = float(data[4])
            self.channel4.x_origin = float(data[5])
            self.channel4.x_reference = float(data[6])
            self.channel4.y_increment = float(data[7])
            self.channel4.y_origin = float(data[8])
            self.channel4.y_reference = float(data[9])
            self.active_channel = self.channel4

    def get_format(self,data) -> str:
        if data == 0:
            return 'BYTE'
        elif data == 1:
            return 'WORD'
        elif data == 2:
            return 'ASC'
        else:
            return None
        
    def get_type(self,data) -> str:
        if data == 0:
            return 'NORM'
        elif data == 1:
            return 'MAX'
        elif data == 2:
            return 'RAW'
        else:
            return None
        
    def get_screen_data(self,channel):
        #self.rigol.stop()
        self.rigol.set_waveform_channel(channel)
        self.rigol.set_reading_mode('NORM')
        self.rigol.set_return_format_waveform('BYTE')
        self.get_info(channel)
        return self.rigol.get_waveform_data()
    
    
    def convert_data_to_v_t(self, data):
        voltage = []
        time = []
        voltage_coeff = 25*self.active_channel.y_increment
        t_inc = self.active_channel.x_increment
        t = 0
        for v in data:
            voltage.append((v-self.active_channel.y_origin-self.active_channel.y_reference)*self.active_channel.y_increment)
            time.append(t)
            t+=t_inc
        return voltage,time
    
    def get_memory_data(self, channel):
        #print(self.rigol.get_reading_mode())
        print(f'Preuzimam podatke sa {channel}')
        self.rigol.set_waveform_channel(channel)
        self.rigol.set_reading_mode('RAW')
        self.rigol.set_return_format_waveform('BYTE')
        self.rigol.set_start_point_waveform_data(1)
        print('Prvi deo')
        self.rigol.set_stop_point_waveform_data(125000)
        voltage = (self.rigol.get_waveform_data())
        print('Drugi deo')
        self.rigol.set_start_point_waveform_data(125001)
        self.rigol.set_stop_point_waveform_data(250000)
        voltage.extend(self.rigol.get_waveform_data())
        print('Treci deo')
        #self.rigol.set_start_point_waveform_data(250001)
        # self.rigol.set_stop_point_waveform_data(375000)
        # voltage.extend(self.rigol.get_waveform_data())
        # self.rigol.set_start_point_waveform_data(375001)
        # self.rigol.set_stop_point_waveform_data(500000)
        # voltage.extend(self.rigol.get_waveform_data())
        # self.rigol.set_start_point_waveform_data(500001)
        # self.rigol.set_stop_point_waveform_data(625000)
        # voltage.extend(self.rigol.get_waveform_data())
        # self.rigol.set_start_point_waveform_data(625001)
        # self.rigol.set_stop_point_waveform_data(750000)
        # voltage.extend(self.rigol.get_waveform_data())
        # self.rigol.set_start_point_waveform_data(750001)
        # self.rigol.set_stop_point_waveform_data(875000)
        # voltage.extend(self.rigol.get_waveform_data())        
        # self.rigol.set_start_point_waveform_data(875001)
        # self.rigol.set_stop_point_waveform_data(1000000)
        # voltage.extend(self.rigol.get_waveform_data())
        self.get_info(channel)
        return voltage

    def write_to_csv(self, filename, time, voltage):
        with open(filename,'w') as f:
            for i in range(len(voltage[0])):
                f.write(f'{time[i]}')
                for j in range(len(voltage)):
                    f.write(f',{voltage[j][i]}')
                f.write('\n')
        