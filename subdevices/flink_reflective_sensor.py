"""
*******************************************************************************************
*    ____   _____ _______            _________  _____     _____  ____  _____  ___  ____   *
*   / __ \ / ____|__   __|          |_   ___  ||_   _|   |_   _||_   \|_   _||_  ||_  _|  *
*  | |  | | (___    | |    _______    | |_  \_|  | |       | |    |   \ | |    | |_/ /    *
*  | |  | |\___ \   | |   |_______|   |  _|      | |   _   | |    | |\ \| |    |  __'.    *
*  | |__| |____) |  | |              _| |_      _| |__/ | _| |_  _| |_\   |_  _| |  \ \_  *
*   \____/|_____/   |_|             |_____|    |________||_____||_____|\____||____||____| *
*                                                                                         *
*******************************************************************************************
*                                                                                         *
*                      Python class for reflective sensor subdevice                       *
*                                                                                         *
*******************************************************************************************

File: flink_reflective_sensor.py

Changelog
When        Who         Version     What
05.11.23    P.Good      1.0         Initial version
"""

import flink
import ctypes as ct
from typing import Tuple

__author__  = "Patrick Good, Urs Graf"
__license__ = "http://www.apache.org/licenses/LICENSE-2.0"
__version__ = "1.0"

class FlinkRefelectiveSensor(flink.FlinkSubDevice):
    """
    The flinkreflectivesensor subdevice realizes an reflective sensor within a flink device.
    It offers several channels. Each channel has it's own sensor value and a hysteresis for IRQ generating.
    
    For IRQ:
        - Each channel has two IRQ lines. one line when the sensor value exceeds the upper bound of the 
          hysteresis and one line when the sensor value goes below the lower bound of the hysteresis.
        - The configuration of the histeresis is done through this module, but to connect the IRQ to a 
          function use the FlinkInterrupt class.
    """

    def __init__(self):
        """
        Creates a reflective sensor object.
        
        Parameters
        ----------
        
        Returns
        -------
        the object
        """
        dev = flink.FlinkDevice()
        subDev = dev.getSubdeviceByType(flink.Definitions.SENSOR_INTERFACE_ID, flink.Definitions.REFELCTIV_SENSOR_SUBTYP)
        super().__init__(dev, subDev)
        dev.lib.flink_reflectivesensor_get_resolution.argtypes = [ct.c_void_p, ct.POINTER(ct.c_uint32)]
        dev.lib.flink_reflectivesensor_get_resolution.restype = ct.c_int
        dev.lib.flink_reflectivesensor_get_value.argtypes = [ct.c_void_p, ct.c_uint32, ct.POINTER(ct.c_uint32)]
        dev.lib.flink_reflectivesensor_get_value.restype = ct.c_int  
        dev.lib.flink_reflectivesensor_set_upper_hysterese.argtypes = [ct.c_void_p, ct.c_uint32, ct.c_uint32]
        dev.lib.flink_reflectivesensor_set_upper_hysterese.restype = ct.c_int
        dev.lib.flink_reflectivesensor_get_upper_hysterese.argtypes = [ct.c_void_p, ct.c_uint32, ct.POINTER(ct.c_uint32)]
        dev.lib.flink_reflectivesensor_get_upper_hysterese.restype = ct.c_int
        dev.lib.flink_reflectivesensor_set_lower_hysterese.argtypes = [ct.c_void_p, ct.c_uint32, ct.c_uint32]
        dev.lib.flink_reflectivesensor_set_lower_hysterese.restype = ct.c_int
        dev.lib.flink_reflectivesensor_get_lower_hysterese.argtypes = [ct.c_void_p, ct.c_uint32, ct.POINTER(ct.c_uint32)]
        dev.lib.flink_reflectivesensor_get_lower_hysterese.restype = ct.c_int

    def getResolution(self, channel: int) -> int:
        """
        Reads the resolution of a single channel within a reflective sensor subdevice. 
        Channel number must be 0 <= channel < nof available channels.
        
        Parameters
        ----------
        channel : channel number 
        
        Returns
        -------
        Resolution
        """
        val = ct.c_uint32()
        error = self.dev.lib.flink_reflectivesensor_get_resolution(self.subDev, channel, ct.byref(val))
        if error < 0:
            raise flink.FlinkException("Failed read the resolution of the reflective sensor", error, self.subDev)
        return int(val.value)

    def getValue(self, channel: int) -> int:
        """
        Reads the value of a single channel within a reflective sensor subdevice. 
        Channel number must be 0 <= channel < nof available channels.
        
        Parameters
        ----------
        channel : channel number 
        
        Returns
        -------
        Sensor value in digitised steps between 0 and Resolution
        """
        val = ct.c_uint32()
        error = self.dev.lib.flink_dio_get_value(self.subDev, channel, ct.byref(val))
        if error < 0:
            raise flink.FlinkException("Failed to read value from reflective sensor channel", error, self.subDev)
        return int(val.value)
    
    def getValueInVolt(self, channel: int, voltage: float = 3.3) -> float:
        """
        Reads the value of a single channel within a reflective sensor subdevice. 
        Channel number must be 0 <= channel < nof available channels.
        
        Parameters
        ----------
        channel : channel number 
        voltage : max Voltage [V] 
        
        Returns
        -------
        Sensor value in Volt [V]
        """
        resolution = self.getResolution(channel)
        value = self.getValue(channel)
        return (voltage/resolution)*value

    def setHysteresis(self, channel: int, upperBound: int, lowerBound: int) -> None:
        """
        Writes the hysteresis of a single channel within a reflective sensor subdevice. 
        Channel number must be 0 <= channel < nof available channels.
        Bounds must be 0 <= upperBound,lowerBound <= resolution
        
        Parameters
        ----------
        channel    : channel number
        upperBound : The upper limit of the hysteresis for the IRQ
        lowerBound : The lower limit of the hysteresis for the IRQ
        
        Returns
        -------
        None
        """
        error = self.dev.lib.flink_reflectivesensor_set_upper_hysterese(self.subDev, channel, upperBound)
        if error < 0:
            raise flink.FlinkException("Failed to write hysteresis upper bound to reflective sensor channel", error, self.subDev)
        error = self.dev.lib.flink_reflectivesensor_set_lower_hysterese(self.subDev, channel, lowerBound)
        if error < 0:
            raise flink.FlinkException("Failed to write hysteresis lower bound to reflective sensor channel", error, self.subDev)
        
    def getHysteresis(self, channel: int) -> Tuple[int]:
        """
        Writes the hysteresis of a single channel within a reflective sensor subdevice. 
        Channel number must be 0 <= channel < nof available channels.
        Bounds must be 0 <= upperBound,lowerBound <= resolution
        
        Parameters
        ----------
        channel    : channel number
        
        Returns
        -------
        (lowerBound, upperBound)
        lowerBound : The lower limit of the hysteresis for the IRQ
        upperBound : The upper limit of the hysteresis for the IRQ
        """

        upperBound = ct.c_uint32()
        lowerBound = ct.c_uint32()
        error = self.dev.lib.flink_reflectivesensor_set_upper_hysterese(self.subDev, channel, ct.byref(upperBound))
        if error < 0:
            raise flink.FlinkException("Failed to read hysteresis upper bound to reflective sensor channel", error, self.subDev)
        error = self.dev.lib.flink_reflectivesensor_set_lower_hysterese(self.subDev, channel, ct.byref(lowerBound))
        if error < 0:
            raise flink.FlinkException("Failed to read hysteresis lower bound to reflective sensor channel", error, self.subDev)
        return (int(lowerBound.value), int(upperBound.value))
        