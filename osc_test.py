from RigolDS1054Z.RigolDS1054Z import RigolDS1054Z

osc = RigolDS1054Z('TCPIP::192.168.123.2::INSTR', read_termination='\n')

print(osc.get_info())