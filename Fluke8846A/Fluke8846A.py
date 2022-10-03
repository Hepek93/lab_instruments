import pyvisa
import time

class Fluke8846A:
    """Class that controls Fluke 9142 Dry Temperature bath.

    Set dev_info:
        - TCP/IP connection  e.g ['TCPIP::169.254.1.2::3490'])
        Note: If instrument could not be recognized with standdar TCPIP settings, try with raw socket
        e.g. ['TCPIP::169.254.1.2::3490:SOCKET']
        - usb connection  (dev_info set to ['usb_dev_info'] e.g [''])
        - serial connection (dev_info set_to ['COM port',] e.g ['ASRL/dev/ttyUSB0::INSTR'])"""

    def __init__(self, dev_info, read_termination = '\r\n', write_termination = '\r\n', delay = 0.05, timeout = 10_000) -> None:
        
        self.__instrument_connected = False
        
        rm = pyvisa.ResourceManager()
        try:
            self.__inst = rm.open_resource(dev_info, write_termination=write_termination, read_termination=read_termination)
            self.__instrument_connected = True
            self.__inst.timeout = timeout
            self.__delay = delay
        except:
            print('Check connection with Fluke 9142')
    
    def __get_data(self,query) -> str:
        if self.__instrument_connected:
            try:
                recv = self.__inst.query(query)
                time.sleep(self.__delay)
                return recv
            except:
                print('Can not query data from the instrument')
            
        else:
            print('Fluke 8846A is not connected')
        return None

    def __write_data(self, data) -> bool:
        if self.__instrument_connected:
            try:
                self.__inst.write(data)
                time.sleep(self.__delay)
                return True
            except Exception as e: 
                print('Can not send data to the Fluke 8846A')
                print('Reason:', e)
            
        else:
            print('Fluke 8846A is not connected')
        return False

    def close_connection(self) -> str:
        """Close connection"""
        if self.__instrument_connected:
            self.__inst.close()
            self.__instrument_connected = False

    # Get instrument info
    def get_info(self) -> str:
        """Get instrument info """
        return self.__get_data('*IDN?')

    def get_operation_complete_bit(self) -> str:
        """Get "Operation Complete" bit in Standard event reg.
           Returns “1” in output buffer after command execution."""
        return self.__get_data('*OPC?')

    def clear_status(self) -> bool:
        """Clear status byte summary, and all event registers"""
        return self.__write_data('*CLS')

    def reset_instrument(self) -> bool:
        """Reset Meter to its power-on state"""
        return self.__write_data('*RST')

    def self_test(self) -> bool:
        """Perform self-test. Returns “0” if the test succeeds,
        “1” if the test fails"""
        return self.__write_data('*TST')

    def switch_to_local(self) -> bool:
        """Places the Meter in the local mode. Front-panel keys still function"""
        return self.__write_data('SYST:LOC')

    def switch_to_remote(self) -> bool:
        """Places the Meter in the remote mode for RS-232 or Ethernet remote
        control. All front-panel keys, except the local key, are disabled."""
        return self.__write_data('SYST:REM')

    def get_current_config(self):
        """Retrieves present Meter configuration"""
        return self.__get_data('CONF?')

    '''2 wire resistance'''

    def get_2w_resistance_range(self) -> str:
        """Get 2-wire resistance measurement range"""
        return self.__get_data('SENS:RES:RANG?')

    def set_2w_resistance(self, range = 'DEF', resolution = 'MIN') -> bool:
        """Select 2-wire resistance function"""
        return self.__write_data('CONF:RES {}, {}'.format(range, resolution))

    '''4 wire resistance'''

    def set_4w_resistance(self, range = 'DEF', resolution = 'MIN') -> bool:
        """Select 4-wire resistance function"""
        return self.__write_data('CONF:FRES {}, {}'.format(range, resolution))

    def get_2w_resistance_range(self) -> str:
        """Get 4-wire resistance measurement range"""
        return self.__get_data('SENS:FRES:RANG?')

    '''DC voltage'''

    def set_dc_voltage(self, range = 'DEF', resolution = 'MIN') -> bool:
        """Select dc volts function """
        return self.__write_data('CONF:VOLT:DC {}, {}'.format(range, resolution))

    def get_dc_voltage_range(self) -> str:
        """Get dc volts measurement range"""
        return self.__get_data('SENS:VOLT:DC:RANG?')


    '''AC voltage'''

    def set_ac_voltage(self, range = 'DEF', resolution = 'MIN') -> bool: 
        """Selects ac volts function"""
        return self.__write_data('CONF:VOLT:AC {}, {}'.format(range,resolution))
    
    def get_ac_voltage_range(self) -> str:
        """Get ac volts measurement range"""
        return self.__get_data('SENS:VOLT:AC:RANG?')

    '''DC voltage ratio'''

    def set_dc_voltage_ratio(self) -> bool:
        """Selects dc volts ratio function"""
        return self.__write_data('CONF:VOLT:DC:RATIO')

    '''DC current'''

    def set_dc_current(self, range = 'DEF', resolution = 'MIN') -> bool:
        """Select dc current function """
        return self.__write_data('CONF:CURR:DC {}, {}'.format(range, resolution))

    def get_dc_voltage_range(self) -> str:
        """Get dc current measurement range"""
        return self.__get_data('SENS:CURR:DC:RANG?')

    '''AC current'''

    def set_ac_current(self, range = 'DEF', resolution = 'MIN') -> bool:
        """Select ac current function """
        return self.__write_data('CONF:CURR:AC {}, {}'.format(range, resolution))

    def get_ac_voltage_range(self) -> str:
        """Get ac current measurement range"""
        return self.__get_data('SENS:CURR:AC:RANG?')

    '''Selects frequency function'''
    
    def set_frequency(self, range = 'DEF', resolution = 'MIN') -> bool:
        """Select frequency function"""
        return self.__write_data('CONF:FREQ {}, {}'.format(range, resolution))

    def get_frequency_range(self) -> str:
        """Get frequency range"""
        return self.__get_data('SENS:FREQ:RANG?')

    '''Selects period function'''
    
    def set_period(self, range = 'DEF', resolution = 'MIN') -> bool:
        """Select period function"""
        return self.__write_data('CONF:PER {}, {}'.format(range, resolution))

    def get_period_range(self) -> str:
        """Get period range"""
        return self.__get_data('SENS:PER:RANG?')

    '''Selects capacitance function'''
    
    def set_capacitance(self, range = 'DEF', resolution = 'MIN') -> bool:
        """Select capacitance function"""
        return self.__write_data('CONF:CAP {}, {}'.format(range, resolution))

    def get_capacitance_range(self) -> str:
        """Get capacitance range"""
        return self.__get_data('SENS:CAP:RANG?')    

    '''Selects temperature 2-wire function'''
    
    def set_2w_temperature(self, type = 'DEF') -> bool:
        """Select temperature 2-wire function"""
        rtd = ['PT100_385', 'PT100_392', 'CUST1']
        if type in rtd:
            return self.__write_data('CONF:TEMP:RTD {}'.format(type))
        else:
            print('Please check sensor type.')
            return False

    '''Selects temperature 4-wire function'''
    
    def set_4w_temperature(self, type = 'DEF') -> bool:
        """Select temperature 4-wire function"""
        rtd = ['PT100_385', 'PT100_392', 'CUST1']
        if type in rtd:
            return self.__write_data('CONF:TEMP:FRTD {}'.format(type))
        else:
            print('Please check sensor type.')
            return False

    '''Selects continuity function'''

    def set_continuity(self) -> bool:
        """Select continuity function"""
        return self.__write_data('CONF:CONT')

    '''Selects diode function'''

    def set_diode(self, low_current = 'ON', high_voltage = 'OFF')-> bool:
        """Select diode function"""
        return self.__write_data('CONF:DIOD {}, {}'.format(low_current, high_voltage))

    @staticmethod
    def list_instruments()->str:
        rm = pyvisa.ResourceManager()
        return rm.list_resources()

    