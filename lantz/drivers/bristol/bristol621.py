from ctypes import c_double, c_float, c_int, c_long, c_uint

from lantz.core import Action, Feat
from lantz.core.foreign import LibraryDriver
asdifjaosdif
from lantz.drivers.bristol import Bristol6XX


class Bristol621(LibraryDriver, Bristol6XX):
    LIBRARY_NAME = 'CLDevIFace.dll'
    LIBRARY_PREFIX = 'CL'

    def __init__(self, address):
        super().__init__()
        self.lib.OpenUSBSerialDevice.argtypes = [c_long]
        self.lib.OpenUSBSerialDevice.restype = c_int
        self.lib.CloseDevice.argtypes = [c_long]
        self.lib.CloseDevice.restype = c_int
        self.lib.SetLambdaUnits.argtypes = [c_int, c_uint]
        self.lib.SetLambdaUnits.restype = c_int
        self.lib.SetPowerUnits.argtypes = [c_int, c_uint]
        self.lib.SetPowerUnits.restype = c_int
        self.lib.GetLambdaReading.argtypes = [c_int]
        self.lib.GetLambdaReading.restype = c_double
        self.lib.GetPowerReading.argtypes = [c_int]
        self.lib.GetPowerReading.restype = c_float

        self.address = address
        self.handle = None
        return

    def initialize(self):
        self.handle = self.lib.OpenUSBSerialDevice(self.address)
        return

    def finalize(self):
        self.lib.CloseDevice()
        return

    @Action()
    def acquisition_frequency(self, f):
        self.lib.SetAcqFreq(self.handle, f)
        return

    @Feat(units='nm')
    def wavelength(self):
        self.lib.SetLambdaUnits(self.handle, 0)
        value = self.lib.GetLambdaReading(self.handle)
        return value

    @Feat(units='GHz')
    def frequency(self):
        self.lib.SetLambdaUnits(self.handle, 1)
        value = self.lib.GetLambdaReading(self.handle)
        return value

    @Feat(units='mW')
    def power(self):
        self.lib.SetPowerUnits(self.handle, 0)
        value = self.lib.GetPowerReading(self.handle)
        return value


if __name__ == '__main__':
    b = Bristol621(5)
    b.initialize()
    b.acquisition_frequency(5)
    while 1:
        print(b.frequency)
