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
*                        Python class for stepper motor subdevice                         *
*                                                                                         *
*******************************************************************************************

File: flink_steppermotor.py

Changelog
When        Who         Version     What
05.11.23    P.Good      1.0         Initial version
"""

import flink
import ctypes as ct
from enum import Enum

__author__  = "Patrick Good, Urs Graf"
__license__ = "http://www.apache.org/licenses/LICENSE-2.0"
__version__ = "1.0"

class FlinkStepperMotor(flink.FlinkSubDevice):
    """
    The flinksteppermotor subdevice realizes an reflectiv sensor within a flink device.
    Each Channel generates an IRQ when the motor has stopped
    """

    class LocalConfReg(Enum):
        """
        Bit definitions for the local configuration register.
        """
        DIRECTION   = 0         # Motor direction (0: Clockwise, 1: Counter-Clockwise)
        FULL_STEP   = 1         # Full step mode (0: Disabled, 1: Enabled)
        TWO_PHASE   = 2         # Two-phase mode (0: Disabled, 1: Enabled)
        RUN_MODE_0  = 3         # Operating mode bit 0
        RUN_MODE_1  = 4         # Operating mode bit 1
        START       = 5         # Motor start (0: Start, 1: Stop)
        RESET_STEPS = 6         # Reset step count (0: Disabled, 1: Enabled)

    class RunMode(Enum):
        """
        Motor operation modes.
        """
        DISABLED  = 0           # Motor is disabled (no holding torque)
        STEPPING  = 1           # Stepping mode (Motor takes a fixed number of steps)
        FIX_SPEED = 2           # Fixed speed mode (Motor moves at a constant speed)

    class Direction(Enum):
        """
        Motor direction definitions.
        """
        CLOCKWISE         = 1   # Clockwise direction
        COUNTER_CLOCKWISE = 0   # Counter-clockwise direction

    class StepMode(Enum):
        """
        Motor stepping mode definitions.
        """
        FULL_STEPS = 1         # Full-step mode
        HALF_STEPS = 0         # Half-step mode

    class PhaseMode(Enum):
        """
        Motor phase mode definitions.
        Has an effect only in full step mode
        """
        TWO_PHASE = 1          # Two-phase mode
        ONE_PHASE = 0          # One-phase mode

    class Start(Enum):
        """
        Motor start/stop definitions.
        """
        START = 1              # Start the motor
        STOP  = 0              # Stop the motor

    def __init__(self):
        """
        Creates a stepper motor object.
        
        Parameters
        ----------
        
        Returns
        -------
        the object
        """
        dev = flink.FlinkDevice()
        subDev = dev.getSubdeviceByType(flink.Definitions.STEPPER_MOTOR_INTERFACE_ID)
        super().__init__(dev, subDev)
        dev.lib.flink_stepperMotor_get_baseclock.argtypes = [ct.c_void_p, ct.POINTER(ct.c_uint32)]
        dev.lib.flink_stepperMotor_get_baseclock.restype = ct.c_int

        dev.lib.flink_stepperMotor_set_local_config_reg.argtypes = [ct.c_void_p, ct.c_uint32, ct.c_uint32]
        dev.lib.flink_stepperMotor_set_local_config_reg.restype = ct.c_int  
        dev.lib.flink_stepperMotor_get_local_config_reg.argtypes = [ct.c_void_p, ct.c_uint32, ct.POINTER(ct.c_uint32)]
        dev.lib.flink_stepperMotor_get_local_config_reg.restype = ct.c_int
        dev.lib.flink_stepperMotor_set_local_config_reg_bits_atomic.argtypes = [ct.c_void_p, ct.c_uint32, ct.c_uint32]
        dev.lib.flink_stepperMotor_set_local_config_reg_bits_atomic.restype = ct.c_int
        dev.lib.flink_stepperMotor_reset_local_config_reg_bits_atomic.argtypes = [ct.c_void_p, ct.c_uint32, ct.c_uint32]
        dev.lib.flink_stepperMotor_reset_local_config_reg_bits_atomic.restype = ct.c_int

        dev.lib.flink_stepperMotor_set_prescaler_start.argtypes = [ct.c_void_p, ct.c_uint32, ct.c_uint32]
        dev.lib.flink_stepperMotor_set_prescaler_start.restype = ct.c_int
        dev.lib.flink_stepperMotor_get_prescaler_start.argtypes = [ct.c_void_p, ct.c_uint32, ct.POINTER(ct.c_uint32)]
        dev.lib.flink_stepperMotor_get_prescaler_start.restype = ct.c_int
        dev.lib.flink_stepperMotor_set_prescaler_top.argtypes = [ct.c_void_p, ct.c_uint32, ct.c_uint32]
        dev.lib.flink_stepperMotor_set_prescaler_top.restype = ct.c_int
        dev.lib.flink_stepperMotor_get_prescaler_top.argtypes = [ct.c_void_p, ct.c_uint32, ct.POINTER(ct.c_uint32)]
        dev.lib.flink_stepperMotor_get_prescaler_top.restype = ct.c_int
        
        dev.lib.flink_stepperMotor_set_acceleration.argtypes = [ct.c_void_p, ct.c_uint32, ct.c_uint32]
        dev.lib.flink_stepperMotor_set_acceleration.restype = ct.c_int
        dev.lib.flink_stepperMotor_get_acceleration.argtypes = [ct.c_void_p, ct.c_uint32, ct.POINTER(ct.c_uint32)]
        dev.lib.flink_stepperMotor_get_acceleration.restype = ct.c_int

        dev.lib.flink_stepperMotor_set_steps_to_do.argtypes = [ct.c_void_p, ct.c_uint32, ct.c_uint32]
        dev.lib.flink_stepperMotor_set_steps_to_do.restype = ct.c_int
        dev.lib.flink_stepperMotor_get_steps_to_do.argtypes = [ct.c_void_p, ct.c_uint32, ct.POINTER(ct.c_uint32)]
        dev.lib.flink_stepperMotor_get_steps_to_do.restype = ct.c_int
        dev.lib.flink_stepperMotor_get_steps_have_done.argtypes = [ct.c_void_p, ct.c_uint32, ct.POINTER(ct.c_uint32)]
        dev.lib.flink_stepperMotor_get_steps_have_done.restype = ct.c_int

        dev.lib.flink_steppermotor_global_step_reset.argtypes = [ct.c_void_p]
        dev.lib.flink_steppermotor_global_step_reset.restype = ct.c_int

    def getBaseClock(self) -> int:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function 

    def unsave_setLocalConfiguration(self, channel: int, config: int) -> None:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function 
    
    def getLocalConfiguration(self, channel: int) -> int:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function 

    def setBitsInLocalConfiguration(self, channel: int, bitsToSet: int) -> None:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function

    def ResetBitsInLocalConfiguration(self, channel: int, bitsToReset: int) -> None:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function
    
    def setStartSpeed(self, channel: int, config: int) -> None:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function 
    
    def getStartSpeed(self, channel: int) -> int:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function 

    def setSollSpeed(self, channel: int, config: int) -> None:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function 
    
    def getSollSpeed(self, channel: int) -> int:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function 

    def setAcceleration(self, channel: int, config: int) -> None:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function 
    
    def getAcceleration(self, channel: int) -> int:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function

    def setStepsToDo(self, channel: int, config: int) -> None:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function 
    
    def getStepsToDo(self, channel: int) -> int:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function 

    def getStepsHaveDone(self, channel: int) -> int:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function
    
    def resetStepsGlobal(self) -> None:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function

    def resetStepsLocal(self, channel: int) -> None:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function

    def setDirection(self, channel: int, direction: Direction) -> None:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function

    def getDirection(self, channel: int) -> Direction:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function

    def setStepMode(self, channel: int, stepMode: StepMode) -> None:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function

    def getStepMode(self, channel: int) -> StepMode:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function

    def setPhaseMode(self, channel: int, phaseMode: PhaseMode) -> None:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function

    def getPhaseMode(self, channel: int) -> PhaseMode:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function

    def setRunMode(self, channel: int, runMdoe: RunMode) -> None:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function

    def getRunMode(self, channel: int) -> RunMode:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function

    def setStart(self, channel: int, start: Start) -> None:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function

    def getStart(self, channel: int) -> Start:
        """
        
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        """
        # TODO: implement function