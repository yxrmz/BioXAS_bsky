from collections import OrderedDict

from ophyd import (Component as Cpt, Device,
                   DynamicDeviceComponent as DDCpt,
                   EpicsSignal, EpicsSignalRO, )


def _channel_fields(cls, attr_base, field_base, range_, **kwargs):
    defn = OrderedDict()
    for i in range_:
        attr = '{attr}{i}'.format(attr=attr_base, i=i)
        suffix = '{field}{i:02d}'.format(field=field_base, i=i)
        defn[attr] = (cls, suffix, kwargs)
    return defn


class MCSChannel(Device):
    enable = Cpt(EpicsSignal, ':enable', kind='config')
    readback = Cpt(EpicsSignalRO, ':fbk')


class CLSSIS3820(Device):
    start_scan = Cpt(EpicsSignal, ':startScan')
    scan_count = Cpt(EpicsSignal, ':scanCount')
    scan = Cpt(EpicsSignal, ':scan')
    nscan = Cpt(EpicsSignal, ':nscan')
    mode = Cpt(EpicsSignal, ':mode')
    input_mode = Cpt(EpicsSignal, ':inputMode')
    source = Cpt(EpicsSignal, ':source')
    trigger_source = Cpt(EpicsSignal, ':triggerSource')
    delay = Cpt(EpicsSignal, ':delay')
    channels = DDCpt(_channel_fields(MCSChannel, 'ch', '', range(32)))

    def update_kind(self, disabled_type='config'):
        for cpt in sis.channels.component_names:
            ch = getattr(sis.channels, cpt) 
            if not ch.enable.get(): 
                ch.readback.kind = disabled_type 
            else: 
                ch.readback.kind = 'hinted' 

    def stage(self, *args, disabled_type='config', **kwargs):
        super().stage(*args, **kwargs)
        self.update_kind(disabled_type)


sis = CLSSIS3820('MCS1607-701:mcs', name='sis') 
