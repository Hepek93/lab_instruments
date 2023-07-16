import pyvisa
import time

class RigolDS1054Z:
    """
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
            print('Check connection with Rigol DS1054Z')
    
    def __get_data(self,query) -> str:
        if self.__instrument_connected:
            try:
                recv = self.__inst.query(query)
                time.sleep(self.__delay)
                return recv
            except:
                print('Can not query data from the instrument')
            
        else:
            print('Rigol DS1054Z is not connected')
        return None

    def __write_data(self, data) -> bool:
        if self.__instrument_connected:
            try:
                self.__inst.write(data)
                time.sleep(self.__delay)
                return True
            except Exception as e: 
                print('Can not send data to the Rigol DS1054Z')
                print('Reason:', e)
            
        else:
            print('Rigol DS1054Z is not connected')
        return False

    def get_enable_register(self) -> str:
        """Query the enable register for the standard event status register set.
        The bit 1 and bit 6 of the standard event status register are not used and are always
        treated as 0; therefore, the range of <value> are the decimal numbers corresponding to
        the binary numbers X0XXXX0X (X is 1 or 0).
        
        Returns
        -------
        str status - The query returns an integer which equals the sum of the weights of all the bits that have
                     already been set in the register."""
        return self.__get_data('*ESE?')

    def set_enable_register(self, value) -> bool:
        """Set the enable register for the standard event status register set.
        The bit 1 and bit 6 of the standard event status register are not used and are always
        treated as 0; therefore, the range of <value> are the decimal numbers corresponding to
        the binary numbers X0XXXX0X (X is 1 or 0).
        Parameters
        ----------
        value : type - str or int
        Returns
        -------
        bool status"""
        return self.__get_data('*ESE {}'.format(value))
    
    def clear_event_register(self) -> str:
        """Query and clear the event register for the standard event status register.
        The bit 1 and bit 6 of the standard event status register are not used and are always
        treated as 0. The range of the return value are the decimal numbers corresponding to
        the binary numbers X0XXXX0X (X is 1 or 0).
        
        Returns
        -------
        str status - The query returns an integer which equals the sum of the weights of all the bits in the
                     register."""
        
        return self.__get_data('*ESR?')

    def get_info(self) -> str:
        """Query the ID string of the instrument.
        Returns
        -------
        str status - The query returns RIGOL TECHNOLOGIES,<model>,<serial number>,<software version>.
                     Whererin:
                     <model>: the model number of the instrument.
                     <serial number>: the serial number of the instrument.
                     <software version>: the software version of the instrument.        
        """
        return self.__get_data('*IDN?')
    
    def get_operation_complete_bit(self) -> str:
        """The *OPC command is used to set the Operation Complete bit (bit 0) in the standard
        event status register to 1 after the current operation is finished. The *OPC? command is
        used to query whether the current operation is finished.
            
        Returns
        -------
        str status - The query returns 1 if the current operation is finished; otherwise, returns 0.
        """
        return self.__get_data('*OPC?')

    def reset_instrument(self) -> bool:
        """Restore the instrument to the default state.
        
        Returns
        -------
        bool status"""
        return self.__write_data('*RST')

    def self_test(self) -> bool:
        """Perform self-test. Returns “0” if the test succeeds,
        “1” if the test fails"""
        return self.__write_data('*TST')

    @staticmethod
    def list_instruments()->str:
        rm = pyvisa.ResourceManager()
        return rm.list_resources()
