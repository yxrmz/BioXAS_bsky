from ophyd.sim import NullStatus
from ophyd import Component as Cpt, Signal, Device


class DetectorBundle(Device):
    num_points = Cpt(Signal, value=-1)
    # xs_inboard = Cpt(CLSXspress3Detector, 'PDTR1607-701:')
    # xs_outboard = Cpt(CLSXspress3Detector, 'PDTR1607-703:')

    def __init__(self, xs_dets, scaler, trigger_signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xs_dets = xs_dets
        self.scaler = scaler
        self.trigger_signal = trigger_signal

    def read(self, *args, **kwargs):
        read_dict = {}
        for xs_det in self.xs_dets:
            read_dict.update(xs_det.read())
        return read_dict

    def describe(self, *args, **kwargs):
        desc_dict = {}
        for xs_det in self.xs_dets:
            desc_dict.update(xs_det.describe())
        return desc_dict
    
    def describe_configuration(self, *args, **kwargs):
        desc_conf_dict = {}
        for xs_det in self.xs_dets:
            desc_conf_dict.update(xs_det.describe_configuration())
        return desc_conf_dict

    def stage(self, *args, **kwargs):
        super().stage(*args, **kwargs)
        for xs_det in self.xs_dets:
            xs_det.hdf5.file_write_mode.put('Stream')
            # Prepare the soft signals for hxntools.detectors.xspress3.Xspress3FileStore#stage
            xs_det.external_trig.put(True)
            xs_det.total_points.put(self.num_points.get())
            xs_det.spectra_per_point.put(1)
            xs_det.stage()
            xs_det.trigger()
        self.scaler.stage()

    def set_num_points(self, num_points):
        self.num_points.put(num_points)

    def trigger(self, *args, **kwargs):
        try:
            del status0
            del status1
        except Exception:
            ...
        super().trigger(*args, **kwargs)
        def callback(value, old_value, **kwargs):
            print(f'old value: {old_value} -> new value: {value}')
            if int(old_value) < int(value):
                return True
            else:
                return False
        status0 = SubscriptionStatus(self.xs_dets[0].settings.array_counter, callback, run=True)
        status1 = SubscriptionStatus(self.xs_dets[1].settings.array_counter, callback, run=True)

        self.trigger_signal.put(1)
        return status0 & status1

    def unstage(self, *args, **kwargs):
        for xs_det in self.xs_dets:
            xs_det.unstage()
        self.scaler.unstage()
        super().unstage(*args, **kwargs)


bundle = DetectorBundle(xs_dets=[xs_inboard, xs_outboard], scaler=sis, trigger_signal=zebra.soft_input1, name='bundle')
