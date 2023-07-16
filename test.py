from Fluke8846A.Fluke8846A import Fluke8846A
import time

instr = Fluke8846A('TCPIP::169.254.1.2::3490::SOCKET', read_termination='\n', write_termination='\n', timeout = 100_000)
instr.clear_status()

instr.clear_status()
instr.set_dc_current('6E-1', 'MAX')
#instr.set_ac_current(range = 'DEF', resolution='MAX')
#instr.set_ac_current_bandwidth(200)

instr.set_trigger_source('EXT')
instr.set_trigger_delay()
instr.switch_to_remote()
instr.set_trigger_count(5000)
instr.set_samples_per_trigger()
instr.set_display_status('OFF')

instr.init_wait_for_triger()
data = instr.fetch_data()
print(data)
instr.set_display_status('ON')

with open('500mA.csv', "w", newline='') as f:
    try:
        rows=data.strip().split(',')
        
        for i in rows:
            f.write(i+'\n')
    except:
        print('Error')


