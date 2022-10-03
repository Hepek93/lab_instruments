from Fluke8846A.Fluke8846A import Fluke8846A
import time

instr = Fluke8846A('TCPIP::169.254.1.2::3490::SOCKET', read_termination='\n', write_termination='\n', timeout = 100_000)
instr.clear_status()

instr.clear_status()
instr.set_dc_current('DEF', 'MAX')

instr.set_trigger_source('EXT')
instr.set_trigger_delay()
instr.switch_to_remote()
instr.set_trigger_count(500)
instr.set_samples_per_trigger()

instr.init_wait_for_triger()
print(instr.fetch_data())


