import pyvisa

class Isotech954:
    def __init__(self,dev_info) -> None:
        self.__instrument_connected = False
                
        rm = pyvisa.ResourceManager()
        try:
            self.__inst = rm.open_resource(dev_info)
            self.__instrument_connected = True
        except:
            print('Check connection with Isotech 954')

    def switch_to_channel(self, data) -> int:
        if self.__instrument_connected:
            if data > 0 and data < 9:
                self.__inst.write('C0{}'.format(data))
                return data
            else:
                print('Channel should be in range [1,8]')
        else:
            print('Isotech 954 is not connected')
        return 0

    def close_connection(self) -> None:
        """Close connection"""
        if self.__instrument_connected:
            self.__inst.close()
            self.__instrument_connected = False


    @staticmethod
    def list_instruments()->str:
        rm = pyvisa.ResourceManager()
        return rm.list_resources()