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

    def get_current_config(self) -> str:
        """Retrieves present Meter configuration"""
        return self.__get_data('CONF?')

    def set_display_status(self, status = 'ON') -> bool:
        """Enables or disables the Meter's display"""
        return self.__write_data('DISP {}'.format(status))


    '''Filters'''

    def set_filter_analog(self, state) -> bool:
        """Activates or deactivates the 3-pole analog filter to improve noise immunity
            for dc functions
            
        Parameters
        ----------
        state : type - str or int
            - ON or 1 - Turns the analog dc filter on.
            - OFF or 0 - Turns the analog dc filter off.
        
        Returns
        -------
        bool status
        """
        if state == 'ON' or state == '1' or state == 1:
            return self.__write_data('FILT ON')
        elif state == 'OFF' or state == '0' or state == 0:
            return self.__write_data('FILT OFF')
        else:
            print('Please check parameter state.')
        

    def set_filter_digital(self, state) -> bool:
        """ Activates or deactivates the digital averaging filter to improve noise
            immunity for dc functions.
            
        Parameters
        ----------
        state : type - str or int
            - ON or 1 - Turns the digital averaging filter on.
            - OFF or 0 - Turns the digital averaging filter off.
        
        Returns
        -------
        bool status
        """
        if state == 'ON' or state == '1' or state == 1:
            return self.__write_data('FILT:DIG ON')
        elif state == 'OFF' or state == '0' or state == 0:
            return self.__write_data('FILT:DIG OFF')
        else:
            print('Please check parameter state.')

    def get_filter_digital(self) -> str:
        """Gets state of the digital averaging filter.

        Returns
        -------
        str status - Returns the digital averaging filter setting. (0 =
                     OFF and 1 = ON)
        """
        return self.__write_data('FILT:DIG?')

    def get_filter_analog(self) -> str:
        """Gets state of the 3-pole analog filter.

        Returns
        -------
        str status - Returns the analog dc filter setting. (0 = OFF and 1 = ON)
        """
        return self.__write_data('FILT?')

    '''2 wire resistance'''

    def get_2w_resistance_range(self) -> str:
        """Gets 2-wire resistance measurement range"""
        return self.__get_data('SENS:RES:RANG?')

    def set_2w_resistance(self, range = 'DEF', resolution = 'MIN') -> bool:
        """Selects 2-wire resistance function"""
        return self.__write_data('CONF:RES {}, {}'.format(range, resolution))

    '''4 wire resistance'''

    def set_4w_resistance(self, range = 'DEF', resolution = 'MIN') -> bool:
        """Selects 4-wire resistance function"""
        return self.__write_data('CONF:FRES {}, {}'.format(range, resolution))

    def get_2w_resistance_range(self) -> str:
        """Gets 4-wire resistance measurement range"""
        return self.__get_data('SENS:FRES:RANG?')

    '''DC voltage'''

    def set_dc_voltage(self, range = 'DEF', resolution = 'MIN') -> bool:
        """Selects dc volts function """
        return self.__write_data('CONF:VOLT:DC {}, {}'.format(range, resolution))

    def set_dc_voltage_range(self, range) -> bool:
        """Sets the range of the DC voltage measurement.

        Parameters
        ----------
        range : type - str/int
            - range - expected reading in volts,
            - MINimum - Lowest range
            - MAXimum - Highest range
        
        Returns
        -------
        bool status                
        """
        return self.__write_data('SENS:VOLT:DC:RANG {}'.format(range))

    def set_dc_voltage_auto_range(self, autorange) -> bool:
        """Switches the Meter between autoranging and manual ranging.
        
        Parameters
        ----------
        autorange : type - bool
            - true - Sets the meter's dc volts to autorange,
            - false - Sets the meter's dc volts to manual range.
            
        Returns
        -------
        bool status    
        """ 
        if autorange:
            return self.__write_data('SENS:VOLT:DC:RANG:AUTO ON')
        else:
            return self.__write_data('SENS:VOLT:DC:RANG:AUTO OFF')

    def set_dc_voltage_resolution(self, resolution) -> bool:
        """Sets the resolution of the DC voltage measurement.

        Parameters
        ----------
        resolution : type - str or int
            - resolution - desired resolution in volts,
            - MINimum - Highest resolution
            - MAXimum - Lowest resolution
        
        Returns
        -------
        bool status                
        """
        return self.__write_data('SENS:VOLT:DC:RES {}'.format(resolution))

    def set_dc_voltage_NPLC(self, nplc) -> bool:
        """Sets the Meter's integration time for the dc voltage measurement.

        Parameters
        ----------
        nplc : type - str or int
            - resolution - sets integration time to a preset value of a 
                           power line cycle (0.02, 0.2, 1, 10, and 100),
            - MINimum - 0.02 NPLC
            - MAXimum - 100 NPLC
        
        Returns
        -------
        bool status      
        """
        nplc_list = [0.02, 0.2, 1, 10, 100, '0.02', '0.2', '1', '10', '100', 'MIN', 'MAX']

        if nplc in nplc_list:
            return self.__write_data('SENS:VOLT:DC:NPLC {}'.format(nplc))
        else:
            print('Please check nplc parameter.')

    def get_dc_voltage_range(self) -> str:
        """Gets the range of the DC voltage measurement.
        
        Returns
        -------
        str - Returns the set resolution for dc volts.   
        """
        return self.__get_data('SENS:VOLT:DC:RANG?')

    def get_dc_voltage_resolution(self) -> str:
        """Gets the resolution of the DC voltage measurement.

        Returns
        -------
        str - Returns the set resolution for dc volts.               
        """
        return self.__get_data('SENS:VOLT:DC:RES?')

    def get_dc_voltage_nplc(self) -> str:
        """Gets the nplc of the DC voltage measurement.

        Returns
        -------
        str - Returns the set nplc for dc volts.               
        """
        return self.__get_data('SENS:VOLT:DC:NPLC?')


    '''AC voltage'''

    def set_ac_voltage(self, range = 'DEF', resolution = 'MIN') -> bool: 
        """Selects ac volts function"""
        return self.__write_data('CONF:VOLT:AC {}, {}'.format(range,resolution))
    
    def set_ac_voltage_range(self, range) -> bool:
        """Sets the range of the AC voltage measurement.

        Parameters
        ----------
        rang : type - str or int
            - range - expected reading in volts,
            - MINimum - Lowest range
            - MAXimum - Highest range
        
        Returns
        -------
        bool status                
        """
        return self.__write_data('SENS:VOLT:AC:RANG {}'.format(range))

    def get_ac_voltage_range(self) -> str:
        """Gets ac volts measurement range"""
        return self.__get_data('SENS:VOLT:AC:RANG?')

    '''DC voltage ratio'''

    def set_dc_voltage_ratio(self) -> bool:
        """Selects dc volts ratio function"""
        return self.__write_data('CONF:VOLT:DC:RATIO')

    '''DC current'''

    def set_dc_current(self, range = 'DEF', resolution = 'MIN') -> bool:
        """Selects dc current function """
        return self.__write_data('CONF:CURR:DC {}, {}'.format(range, resolution))

    def get_dc_voltage_range(self) -> str:
        """Gets dc current measurement range"""
        return self.__get_data('SENS:CURR:DC:RANG?')

    '''AC current'''

    def set_ac_current(self, range = 'DEF', resolution = 'MIN') -> bool:
        """Selects ac current function """
        return self.__write_data('CONF:CURR:AC {}, {}'.format(range, resolution))

    def set_ac_current_range(self, range) -> bool:
        """Sets the range of the AC current measurement.

        Parameters
        ----------
        range : type - str/int
            - range - expected reading in amperes,
            - MINimum - Lowest range
            - MAXimum - Highest range
        
        Returns
        -------
        bool status                
        """
        return self.__write_data('SENS:CURR:AC:RANG {}'.format(range))

    def set_ac_voltage_auto_range(self, autorange) -> bool:
        """Switches the Meter between autoranging and manual ranging.
        
        Parameters
        ----------
        autorange : type - bool
            - true - Sets the meter's AC current to autorange,
            - false - Sets the meter's AC current to manual range.
            
        Returns
        -------
        bool status    
        """ 
        if autorange:
            return self.__write_data('SENS:CURR:AC:RANG:AUTO ON')
        else:
            return self.__write_data('SENS:CURR:AC:RANG:AUTO OFF')

    def set_ac_current_resolution(self, resolution) -> bool:
        """Sets the resolution of the AC current measurement.

        Parameters
        ----------
        resolution : type - str or int
            - resolution - desired resolution in amperes,
            - MINimum - Highest resolution
            - MAXimum - Lowest resolution
        
        Returns
        -------
        bool status                
        """
        return self.__write_data('SENS:CURR:AC:RES {}'.format(resolution))

    def set_ac_current_bandwidth(self, bandwidth=20) -> bool:
        """Sets the appropriate filter for the frequency specified by bandwidth parameter.

        Parameters
        ----------
        bandwidth : type - str or int
            - 3 - Selects slow filter
            - 20 (default) - Selects medium filter
            - 200 - Selects fast filter
            - MIN - Selects slow filter
            - MAX - Selects fast filter
        
        Returns
        -------
        bool status      
        """
        bandwidth_list = [3, 20, 200, '3', '20', '200', 'MIN', 'MAX']

        if bandwidth in bandwidth_list:
            return self.__write_data('SENS:CURRENT:AC:BAND {}'.format(bandwidth))
        else:
            print('Please check bandwidth parameter.')

    def get_ac_current_range(self) -> str:
        """Gets the range of the AC current measurement.
        
        Returns
        -------
        str - Returns the set resolution for ac current.   
        """
        return self.__get_data('SENS:CURR:AC:RANG?')

    def get_ac_current_resolution(self) -> str:
        """Gets the resolution of the AC current measurement.

        Returns
        -------
        str - Returns the set resolution for ac current.               
        """
        return self.__get_data('SENS:CURR:AC:RES?')

    def get_ac_current_bandwidth(self) -> str:
        """Gets the bandwidth of the AC current measurement.

        Returns
        -------
        str - Returns the set bandwidth for ac current.               
        """
        return self.__get_data('SENS:CURR:AC:BAND?')

    '''Selects frequency function'''
    
    def set_frequency(self, range = 'DEF', resolution = 'MIN') -> bool:
        """Selects frequency function"""
        return self.__write_data('CONF:FREQ {}, {}'.format(range, resolution))

    def get_frequency_range(self) -> str:
        """Gets frequency range"""
        return self.__get_data('SENS:FREQ:RANG?')

    '''Selects period function'''
    
    def set_period(self, range = 'DEF', resolution = 'MIN') -> bool:
        """Selects period function"""
        return self.__write_data('CONF:PER {}, {}'.format(range, resolution))

    def get_period_range(self) -> str:
        """Gets period range"""
        return self.__get_data('SENS:PER:RANG?')

    '''Selects capacitance function'''
    
    def set_capacitance(self, range = 'DEF', resolution = 'MIN') -> bool:
        """Selects capacitance function"""
        return self.__write_data('CONF:CAP {}, {}'.format(range, resolution))

    def get_capacitance_range(self) -> str:
        """Gets capacitance range"""
        return self.__get_data('SENS:CAP:RANG?')    

    '''Selects temperature 2-wire function'''
    
    def set_2w_temperature(self, type = 'DEF') -> bool:
        """Selects temperature 2-wire function

        Parameters
        ----------
        type : str
            - PT100_385 - sensor type PT100 385
            - PT100_392 - sensor type PT100 392
            - CUST1     - meter using the values set into the R0 and Alpha parameters. 
                          (see methods set_4w_parameter_R0 and set_4w_parameter_Alpha)
        
        Returns
        -------
        bool status                
        """
        rtd = ['PT100_385', 'PT100_392', 'CUST1']
        if type in rtd:
            return self.__write_data('CONF:TEMP:RTD {}'.format(type))
        else:
            print('Please check sensor type.')
            return False

    '''Selects temperature 4-wire function'''
    
    def set_4w_temperature(self, type = 'PT100_385') -> bool:
        """Selects temperature 4-wire function.
        The range and resolution are fixed for temperature measurements.

        Parameters
        ----------
        type : str
            - PT100_385 - sensor type PT100 385
            - PT100_392 - sensor type PT100 392
            - CUST1     - meter using the values set into the R0 and Alpha parameters. 
                          (see methods set_4w_parameter_R0 and set_4w_parameter_Alpha)

        Returns
        -------
        bool status
        """
        rtd = ['PT100_385', 'PT100_392', 'CUST1']
        if type in rtd:
            return self.__write_data('CONF:TEMP:FRTD {}'.format(type))
        else:
            print('Please check sensor type.')
            return False

    def set_4_parameter_R0(self, r0) -> bool:
        """
        Sets the resistance at zero degrees C specified by r0 for the R0 parameter
        of the temperature function.
        
        Parameters
        ----------
        r0 : type - int
            - r0 - 0 to 1010 Resistance at 0 °C.

        Returns
        -------
        bool status
        """
        return self.__write_data('SENS:TEMP:TRAN:FRTD:R0 {}'.format(r0))

    '''Selects continuity function.'''

    def set_continuity(self) -> bool:
        """Selects continuity function.
        The range and resolution are fixed for continuity tests: 1 kΩ range and
        5½ digits.

        Returns
        -------
        bool status
        """
        return self.__write_data('CONF:CONT')

    '''Selects diode function'''

    def set_diode(self, low_current = 'ON', high_voltage = 'OFF')-> bool:
        """Selects diode function. The range and resolution are fixed for diode test: 10 Vdc range and 5½ digits.
        
        Parameters
        ----------
        low_current : type - str
            - ON  - sets the diode test current to 0.1 mA.
            - OFF - sets the diode test current to 1 mA.
        high_voltage : type - str
            - ON  - sets the diode test voltage to 10 V.
            - OFF - setst the diode test voltage to 5 V.

        Returns
        -------
        bool status
        """
        return self.__write_data('CONF:DIOD {}, {}'.format(low_current, high_voltage))

    '''Triggering'''

    def set_trigger_source(self, triggering_source = 'IMM')-> bool:
        """Sets the source from which the Meter will expect a measurement trigger.

        Parameters
        ----------
        triggering_source : type - str
            - BUS : Sets the Meter to expect a trigger through the IEEE-488 bus or upon execution of a *TRG command.
            - IMMediate : Selects Meter's internal triggering system.
            - EXTernal : Sets the Meter to sense triggers through the trigger jack on the rear panel of the Meter.     

        Returns
        -------
        bool status
        """
        sources = ['BUS', 'IMM', 'EXT', 'IMMEDIATE', 'EXTERNAL']
        if triggering_source.upper() in sources: 
            return self.__write_data('TRIG:SOUR {}'.format(triggering_source.upper()))
        else:
            print('Please check triggering source parameter.')
            return False

    def set_trigger_delay(self, trigger_delay = 'MIN')-> bool:
        """Sets the delay between receiving a trigger and the beginning of measurement cycle.
        
        Parameters
        ----------
        trigger_delay : type - int or str
            - 0 to 3600 : Delay specified in seconds.
            - MINimum : Delay set to 0 seconds.
            - MAXimum : Delay set to 3600 seconds.     

        Returns
        -------
        bool status
        """
        return self.__write_data('TRIG:DEL {}'.format(trigger_delay))

    def set_trigger_count(self, trigger_count = 1)-> bool:
        """Sets the number of triggers the Meter will take before switching to an idle state. 
        
        Parameters
        ----------
        samples_count : type - int or str
            - 0 to 50000 : Number of triggers before Meter becomes idle.
            - MINimum : Number of triggers is set to 1.
            - MAXimum : Number of triggers is set to 50000.
            - INFinite: Continuously accepts triggers. A device clear is required to 
                        set the Meter to idle state after INFinite has been set.     

        Returns
        -------
        bool status 
        """
        return self.__write_data('TRIG:COUN {}'.format(trigger_count))
    
    def set_samples_per_trigger(self, samples_count = 1)-> bool:
        """Sets the number of measurements the Meter takes per trigger.
        
        Parameters
        ----------
        samples_count : type - int or str
            - 0 to 50000 : Number of measurements per trigger.
            - MINimum : Number of measurements per trigger set to 1.
            - MAXimum : Number of measurements per trigger set to 50000.     

        Returns
        -------
        bool status        
        """
        return self.__write_data('SAMP:COUN {}'.format(samples_count))

    def init_wait_for_triger(self) -> bool:
        """Sets the Meter to the wait-for-trigger state in which the next trigger from
        the selected source triggers a measurement cycle. Up to 5,000
        measurements are placed into the Meter's internal memory, where they can
        be retrieved with the FETCh? command.
        
        Returns
        -------
        bool status
        """
        return self.__write_data('INIT')

    def read_sample_per_trigger(self) -> str:
        """Sets the Meter in to the wait-for-trigger state where the next trigger from
        the selected source triggers a measurement cycle. Measurements are sent
        directly to the output buffer.
        
        Returns
        -------
        str : sample
        """
        return self.__get_data('READ?')

    def fetch_data(self, data_source = 1) -> str:
        """ Moves measurements stored in the Meter's internal memory to the output
            buffer. FETCh1? or FETCh? returns measurements from the primary
            display. FETCh2? Returns readings from the secondary display.
        
        Parameters
        ----------
        data_source : type - int
            - 1 : returns measurements from the primary display,
            - 2 : returns readings from the secondary display.

        Returns
        -------
        str : samples defined by trigger and sample count.
        """

        if data_source in [1,2]:
            return self.__get_data('FETC{}?'.format(data_source))
        else:
            print('Please check data_source parameter.')

    @staticmethod
    def list_instruments()->str:
        rm = pyvisa.ResourceManager()
        return rm.list_resources()

    