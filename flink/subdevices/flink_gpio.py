import flink
import ctypes as ct

__author__ = "Patrick Good, Urs Graf"
__license__ = "http://www.apache.org/licenses/LICENSE-2.0"
__version__ = "1.0"

class FlinkGPIO(flink.FlinkSubDevice):
    """
    The flink GPIO subdevice realizes digital input and output within a flink device.
    It offers several channels. Each channel drives a single pin.
    """

    def __init__(self):
        dev = flink.FlinkDevice()
        subDev = dev.getSubdeviceByType(flink.Definitions.GPIO_INTERFACE_ID)
        super().__init__(dev, subDev)
        dev.lib.flink_dio_set_direction.argtypes = [ct.c_void_p, ct.c_uint32, ct.c_uint8]
        dev.lib.flink_dio_set_direction.restype = ct.c_int
        dev.lib.flink_dio_set_value.argtypes = [ct.c_void_p, ct.c_uint32, ct.c_uint8]
        dev.lib.flink_dio_set_value.restype = ct.c_int  
        dev.lib.flink_dio_get_value.argtypes = [ct.c_void_p, ct.c_uint32, ct.POINTER(ct.c_uint8)]
        dev.lib.flink_dio_get_value.restype = ct.c_int

    def setDir(self, channel: int, out: bool) -> None:
        """
        Sets the direction of a single channel within a GPIO subdevice. 
        Each channel can work as either digital input or output. 
        Channel number must be 0 < channel < nof available channels.
        
        Parameters
        ----------
        channel : channel number 
        value : false = input, true = output
        
        Returns
        -------
        None
        """
        error = self.dev.lib.flink_dio_set_direction(self.subDev, channel, out)
        if error < 0:
            raise flink.FlinkException("Failed to set direction of gpio channel", error, self.subDev)

    def getValue(self, channel: int) -> bool:
        """
        Reads the value of a single channel within a GPIO subdevice. 
        Each channel can work as either digital input or output. 
        Channel number must be 0 < channel < nof available channels.
        
        Parameters
        ----------
        channel : channel number 
        
        Returns
        -------
        false = input, true = output
        """
        val = ct.c_uint8()
        error = self.dev.lib.flink_dio_get_value(self.subDev, channel, ct.byref(val))
        if error < 0:
            raise flink.FlinkException("Failed to read from gpio channel", error, self.subDev)
        return bool(val.value)

    def setValue(self, channel: int, val: bool) -> None:
        """
        Sets the logical level of a single channel within a GPIO subdevice. 
        Channel number must be 0 < channel < nof available channels.
        
        Parameters
        ----------
        channel : channel number 
        value : false = low, true = high
        
        Returns
        -------
        None
        """
        error = self.dev.lib.flink_dio_set_value(self.subDev, channel, val)
        if error < 0:
            raise flink.FlinkException("Failed to set value of gpio channel", error, self.subDev)
        