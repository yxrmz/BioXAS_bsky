import sys
import logging

from ophyd.status import SubscriptionStatus
from ophyd import Component as Cpt, EpicsSignalRO, EpicsSignal, Device


logger = logging.getLogger('cls-motor')

logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Movable(Device):
    setpoint = Cpt(EpicsSignal, 'deg', kind='hinted')
    readback = Cpt(EpicsSignalRO, 'deg:fbk', kind='hinted')
    moving = Cpt(EpicsSignalRO, 'status', kind='omitted')

    def __init__(self, *args, tolerance=2e-3, **kwargs):
        super().__init__(*args, **kwargs)
        self._tolerance = tolerance

    def set(self, set_value):
        def callback(value, old_value, **kwargs):
            set_val = self.setpoint.get()
            read_val = self.readback.get()

            logger.debug(f'{old_value} -> {value}')
            logger.debug(f'setpoint: {set_val}\nreadback: {read_val}')

            if abs(set_val - read_val) < self._tolerance and (int(old_value) == 1 and int(value) != 1):  # 1 = motor is moving; 0 or 4 = motor is stoped (4 for the alarm state)
                return True
            else:
                return False

        status = SubscriptionStatus(self.moving, callback, run=False)
        self.setpoint.set(set_value)
        return status


dbhr_pitch = Movable('BL1607-I21:DBHR:Pitch:', name='dbhr_pitch', labels=['motor'])
