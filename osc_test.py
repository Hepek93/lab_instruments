from RigolDS1054Z.Oscilloscope import Oscilloscope
from time import sleep

osc = Oscilloscope()


osc.get_info(1)

voltage, time = osc.convert_data_to_v_t(osc.get_screen_data('CHAN1'))


osc.write_to_csv('test.csv', time, voltage)