from RigolDS1054Z.Oscilloscope import Oscilloscope
from time import sleep

osc = Oscilloscope()

osc.rigol.run()
sleep(10)
#osc.get_info(1)
osc.rigol.set_memory_depth(300_000)
osc.rigol.single()
sleep(20)
#voltage, time = osc.convert_data_to_v_t(osc.get_screen_data('CHAN1'))

voltage1, time = osc.convert_data_to_v_t(osc.get_memory_data('CHAN1'))
voltage2, time = osc.convert_data_to_v_t(osc.get_memory_data('CHAN2'))
voltage3, time = osc.convert_data_to_v_t(osc.get_memory_data('CHAN3'))
osc.write_to_csv('Rigol_snimci/230729/memorija_trougao_3_polozaj_100ms_4v_v1.csv', time, [voltage1, voltage2, voltage3])