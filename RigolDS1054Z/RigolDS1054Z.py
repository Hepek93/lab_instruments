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
            except Exception as e:
                print('Can not query data from the instrument')
            
        else:
            print('Rigol DS1054Z is not connected')
        return None

    def __get_bytes(self,query) -> bytes:
        if self.__instrument_connected:
            try:
                self.__write_data(query)
                recv = self.__inst.read_binary_values(datatype='B', expect_termination = False )
                time.sleep(self.__delay)
                return recv
            except Exception as e:
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
        return self.__get_data(f'*ESE {value}')
    
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
        “1” if the test fails

        Returns
        -------
        bool status
        """
        return self.__write_data('*TST')

    def auto_scale(self)->bool:
        """
        Enable the waveform auto setting function. The oscilloscope will automatically adjust the
        vertical scale, horizontal timebase, and trigger mode according to the input signal to
        realize optimum waveform display. This command is equivalent to pressing the AUTO key
        at the front panel.

        Returns
        -------
        bool status
        """
        return self.__write_data('AUT')
    
    def clear_display(self)->bool:
        """
        Clear all the waveforms on the screen. If the oscilloscope is in the RUN state, waveform
        will still be displayed. This command is equivalent to pressing the CLEAR key at the front
        panel.
                
        Returns
        -------
        bool status

        """
        return self.__write_data('CLE')

    def run(self)->bool:
        """
        The :RUN command starts the oscilloscope.
                
        Returns
        -------
        bool status

        """
        return self.__write_data(':RUN')

    def stop(self)->bool:
        """
        The :STOP command stops the oscilloscope.
        
                
        Returns
        -------
        bool status

        """
        return self.__write_data(':STOP')
    
    def single(self)->bool:
        """
        Set the oscilloscope to the single trigger mode. This command is equivalent to any of the
        following two operations: pressing the SINGLE key at the front panel and sending
        the :TRIGger:SWEep SINGle command.
        
                
        Returns
        -------
        bool status

        """
        return self.__write_data(':SING')

    def force_trigger(self)->bool:
        """
        Generate a trigger signal forcefully. This command is only applicable to the normal and
        single trigger modes and is equivalent to pressing the FORCE key in the trigger control 
        area at the front panel.
                
        Returns
        -------
        bool status

        """
        return self.__write_data(':TFOR')
    
    def set_average_acquisition_mode(self, count)->bool:
        """Set or query the number of averages under the average acquisition mode.
        Parameters
        ----------
        count : type - str or int - 2**n(n is an integer from 1 to 10)
        Returns
        -------
        bool status"""
        
        return self.__write_data(f':ACQ:AVER {count}')

    def get_average_acquisition_mode(self)->str:
        """
        The query returns an integer between 2 and 1024.
                
        Returns
        -------
        str - number of averages under the average acquisition mode.

        """
        return self.__get_data(':ACQ:AVER?')

    def set_memory_depth(self, mdep)->bool:
        """Set the memory depth of the oscilloscope (namely the number of waveform
        points that can be stored in a single trigger sample). The default unit is pts (points).

        Parameters
        ----------
        mdep : type - str or int
            For the analog channel:
                ― When a single channel is enabled, the range of <mdep> is {AUTO|12000|
                120000|1200000|12000000|24000000}. Wherein, 24000000 (pts) is an
                optional memory depth.
                ― When dual channels are enabled, the range of <mdep> is {AUTO|6000|60000|
                600000|6000000|12000000}. Wherein, 12000000 (pts) is an optional memory
                depth.
                ― When three/four channels are enabled, the range of <mdep> is {AUTO|3000|
                30000|300000|3000000|6000000}. Wherein, 6000000 (pts) is an optional
                memory depth.
            For the digital channel:
                ― When 8 channels are enabled, the range of <mdep> is {AUTO|12000|120000|
                1200000|12000000|24000000}. Wherein, 24000000 (pts) is an optional
                memory depth.
                ― When 16 channels are enabled, the range of <mdep> is {AUTO|6000|60000|
                600000|6000000|12000000}. Wherein, 12000000 (pts) is an optional memory
                depth.

            The following equation describes the relationship among memory depth, sample
            rate, and waveform length:
            Memory Depth = Sample Rate x Waveform Length
            Wherein, the Waveform Length is the product of the horizontal timebase (set by
            the :TIMebase[:MAIN]:SCALe command) times the number of grids in the horizontal
            direction on the screen (12 for MSO1000Z/DS1000Z).
            When AUTO is selected, the oscilloscope will select the memory depth automatically
            according to the current sample rate.
        Returns
        -------
        bool status"""
        
        return self.__write_data(f':ACQ:MDEP {mdep}')

    def get_memory_depth(self)->str:
        """
        The query returns the actual number of points (integer) or AUTO.
                
        Returns
        -------
        str - number of memory depth in pts.

        """
        return self.__get_data(':ACQ:MDEP?')
    
    def set_acquisition_mode(self, mode)->bool:
        """
        Set the acquisition mode of the oscilloscope.

        Parameters
        ----------
        mode : type - str

            - NORMal: in this mode, the oscilloscope samples the signal at equal time interval to
            rebuild the waveform. For most of the waveforms, the best display effect can be
            obtained using this mode.
            
            - AVERages: in this mode, the oscilloscope averages the waveforms from multiple
            samples to reduce the random noise of the input signal and improve the vertical
            resolution. The number of averages can be set by the:ACQuire:AVERages command.
            Greater number of averages can lower the noise and increase the vertical resolution,
            but will also slow the response of the displayed waveform to the waveform changes.
            
            - PEAK (Peak Detect): in this mode, the oscilloscope acquires the maximum and
            minimum values of the signal within the sample interval to get the envelope of the
            signal or the narrow pulse of the signal that might be lost. In this mode, signal
            confusion can be prevented but the noise displayed would be larger.
            
            - HRESolution (High Resolution): this mode uses a kind of ultra-sample technique to
            average the neighboring points of the sample waveform to reduce the random noise
            on the input signal and generate much smoother waveforms on the screen. This is
            generally used when the sample rate of the digital converter is higher than the
            storage rate of the acquisition memory.
        Returns
        -------
        bool status"""
        
        if mode in ['NORM','NORMal','AVERages','AVER','PEAK','HRES','HRESolution']:
            return self.__write_data(f':ACQ:TYPE {mode}')
        else:
            return False
        
    def get_acquisition_mode(self)->str:
        """
        The returns query the acquisition mode of the oscilloscope.
        
        Returns
        -------
        str - NORM, AVER, PEAK, or HRES.
        """
        return self.__get_data(':ACQ:TYPE?')

    def get_sampling_rate(self)->str:
        """
        Query the current sample rate. The default unit is Sa/s.
        
        Returns
        -------
        str -  the sample rate in scientific notation.
        """
        return self.__get_data(':ACQ:SRAT?')

    def set_waveform_channel(self, source)->bool:
        """
        Set the channel of which the waveform data will be read.

        Parameters
        ----------
        source : type - str

            -If the MATH channel is selected, only NORMal can be selected in :WAVeform:MODE.
            
            -If an digital channel (D0 to D15) is selected, the :WAVeform:DATA? command always
            returns the waveform data in BYTE format. If the waveform data on the screen is
            read, the signal status of the channel source currently selected is returned and a
            waveform point occupies one byte (8 bits). If the waveform data in the internal
            memory is read, the signal statuses of the channel group (D7 to D0 or D15 to D8; 8
            digital channels) which includes the channel source currently selected are returned;
            one byte represents the statuses of a group of digital signals and the data represents
            the statuses of D7 to D0 (or D15 to D8) respectively from the highest bit to the
            lowest bit.
        Returns
        -------
        bool status"""
        
        if source in ['D0','D1','D2','D3','D4','D5','D6','D7','D8','D9','D10','D11',
                      'D12','D13','D14','D15','CHAN1','CHANnel1','CHAN2','CHANnel2',
                      'CHAN3','CHANnel3','CHAN4','CHANnel4','MATH']:
            return self.__write_data(f':WAV:SOUR {source}')
        else:
            return False

    def get_waveform_channel(self)->str:
        """
        The returns query the channel of which the waveform data will be read.
        
        Returns
        -------
        str - The query returns D0, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13, D14,
              D15, CHAN1, CHAN2, CHAN3, CHAN4, or MATH.
        """
        return self.__get_data(':WAV:SOUR?')

    def set_reading_mode(self,mode)->bool:
        """
        Set the reading mode .

        Parameters
        ----------
        source : type - str
            - NORMal: read the waveform data displayed on the screen.
            - MAXimum: read the waveform data displayed on the screen when the instrument is
              in the run state and the waveform data in the internal memory in the stop state.
            - RAW: read the waveform data in the internal memory. Note that the waveform data
              in the internal memory can only be read when the oscilloscope is in the stop state
              and the oscilloscope cannot be operated during the reading process.
            - If the MATH channel is selected, only the NORMal mode is valid.
        Returns
        -------
        bool status
        """

        if mode in ['NORMal','NORM','MAXimum','MAX','RAW']:
            return self.__write_data(f':WAV:MODE {mode}')
        else:
            return False
        
    
    def get_reading_mode(self)->str:
        """
        The returns query the reading mode.
        
        Returns
        -------
        str - The query returns NORM, MAX, or RAW.
        """
        return self.__get_data(':WAV:MODE?')

    def set_return_format_waveform(self, format)->bool:
        """
        Set the return format of the waveform data.

        Parameters
        ----------
        source : type - str
            - WORD: a waveform point occupies two bytes (namely 16 bits) in which the lower 8
                    bits are valid and the higher 8 bits are 0.
            - BYTE: a waveform point occupies one byte (namely 8 bits).
            - ASCii: return the actual voltage value of each waveform point in scientific notation.
                    The voltage values are separated by commas.
        Returns
        -------
        bool status
        """

        if format in ['WORD','BYTE','ASCii','ASC']:
            return self.__write_data(f':WAV:FORM {format}')
        else:
            return False
        
    
    def get_return_format_waveform(self)->str:
        """
        Returns query the return format of the waveform data.
        
        Returns
        -------
        str - The query returns WORD, BYTE, or ASC.
        """
        return self.__get_data(':WAV:FORM?')
    
    def get_waveform_data(self)->bytes:
        """
        Read the waveform data.
        
        Returns
        -------
        bytes - waveform data.
        """
        return self.__get_bytes(':WAV:DATA?')


    def get_waveform_parameters(self)->str:
        """
        Query and return all the waveform parameters.
        
        Returns
        -------
        bytes - The query returns 10 waveform parameters separated by ",":
                <format>,<type>,<points>,<count>,<xincrement>,<xorigin>,<xreference>,<yincrem
                ent>,<yorigin>,<yreference>
            
            Wherein,
            <format>: 0 (BYTE), 1 (WORD) or 2 (ASC).
            <type>: 0 (NORMal), 1 (MAXimum) or 2 (RAW).
            <points>: an integer between 1 and 12000000. After the memory depth option is
            installed, <points> is an integer between 1 and 24000000.
            <count>: the number of averages in the average sample mode and 1 in other modes.
            <xincrement>: the time difference between two neighboring points in the X direction.
            <xorigin>: the start time of the waveform data in the X direction.
            <xreference>: the reference time of the data point in the X direction.
            <yincrement>: the waveform increment in the Y direction.
            <yorigin>: the vertical offset relative to the "Vertical Reference Position" in the Y
            direction.
            <yreference>: the vertical reference position in the Y direction.
        """
        return self.__get_data(':WAV:PRE?')

    @staticmethod
    def list_instruments()->str:
        rm = pyvisa.ResourceManager()
        return rm.list_resources()

    