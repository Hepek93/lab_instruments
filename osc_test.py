from RigolDS1054Z.Oscilloscope import Oscilloscope
from time import sleep

osc = Oscilloscope()

osc.rigol.run()
sleep(10)
#osc.get_info(1)

#voltage, time = osc.convert_data_to_v_t(osc.get_screen_data('CHAN1'))

voltage1, time = osc.convert_data_to_v_t(osc.get_memory_data('CHAN1'))
voltage2, time = osc.convert_data_to_v_t(osc.get_memory_data('CHAN2'))
osc.write_to_csv('Rigol_snimci/memorija_polozaj3_2ms.csv', time, [voltage1, voltage2])