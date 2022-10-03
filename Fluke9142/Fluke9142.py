import pyvisa



class Fluke9142:
    """Class that controls Fluke 9142 Dry Temperature bath.

    Set dev_info:
        - TCP/IP connection  e.g [''])
        - usb connection  (dev_info set to ['usb_dev_info'] e.g [''])
        - serial connection (dev_info set_to ['COM port',] e.g ['ASRL/dev/ttyUSB0::INSTR'])"""

    def __init__(self, dev_info) -> None:
        
        self.__instrument_connected = False
        
        rm = pyvisa.ResourceManager()
        try:
            self._inst = rm.open_resource(dev_info)
            self.__instrument_connected = True
        except:
            print('Check connection with Fluke 9142')
    
    def __get_data(self,query) -> str:
        if self.__instrument_connected:
            try:
                recv = self._inst.query(query)
                return recv
            except:
                print('Can not query data from the instrument')
            
        else:
            print('Fluke 9142 is not connected')
        return None

    def __write_data(self, data) -> bool:
        if self.__instrument_connected:
            try:
                self._inst.write(data)
                return True
            except:
                print('Can not send data to the Fluke 9142')
            
        else:
            print('Fluke 9142 is not connected')
        return False

    def close_connection(self) -> str:
        """Close connection"""
        if self.__instrument_connected:
            self._inst.close()
            self.__instrument_connected = False

    # Get instrument info
    def get_info(self) -> str:
        """Get instrument info """
        return self.__get_data('*IDN?')

    def get_reference_temperature(self) -> str:
        """Get temperature from reference probe"""
        return self.__get_data('READ?')

    def get_reference_resistance(self) -> str:
        """Get reference probe resistance"""
        return self.__get_data('SENS1:DATA?')
    
    def get_control_temperature(self) -> str:
        """Get control probe temperature"""
        return self.__get_data('SOUR:SENS:DATA? TEMP')

    def get_control_resistance(self) -> str:
        """Get control probe resistance"""
        return self.__get_data('SOUR:SENS:DATA? RES')

    def get_output_status(self) -> str:
        """Get output status"""
        return self.__get_data('OUT:STAT?')

    def get_stability_limit(self) -> str:
        """Get stability limit"""
        return self.__get_data('SOUR:STAB:LIM?')

    def get_stability_status(self) -> str:
        """Check set point temperature stability
            return
            0 - controller is not stable
            1 - controller is stable
        """
        return self.__get_data('SOUR:STAB:TEST?')

    def get_stability_of_controller(self) -> str:
        """Get current stability limit of controller"""
        return self.__get_data('SOUR:STAB:DAT?')

    def set_stability_limit(self, stab_lim) -> bool:
        """Set stability limit"""
        if stab_lim >= 0.01 and stab_lim <= 9.99:
            return self.__write_data('SOUR:STAB:LIM '+str(stab_lim))
        else:
            print('Stability limit should be in range [0.01, 9.99]')
            return False

    def set_temperature(self, temp) -> bool:
        """Set desired temperature"""
        if temp >= -25 and temp <= 150:
            return self.__write_data('SOUR:SPO '+ str(round(temp,2)))
        else:
            print('Temperature is not in range [-25,150]')
            return False
    def set_output_on(self) -> bool:
        """Enable heating/cooling"""
        return self.__write_data('OUTP:STAT 1')

    def set_output_off(self) -> bool:
        """Disable heating/cooling"""
        return self.__write_data('OUTP:STAT 0')

    def beep(self) -> bool:
        """Beep the system beeper"""
        return self.__write_data('SYST:BEEP:IMM')

    @staticmethod
    def list_instruments()->str:
        rm = pyvisa.ResourceManager()
        return rm.list_resources()

    