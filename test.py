from Fluke8846A.Fluke8846A import Fluke8846A
import time

instr = Fluke8846A('TCPIP::169.254.1.2::3490::SOCKET', read_termination='\n', write_termination='\n')#, timeout = 100_000)


instr.clear_status()

print(instr.get_2w_resistance_range())

