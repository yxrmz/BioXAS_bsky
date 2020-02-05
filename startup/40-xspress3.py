from ophyd.areadetector.plugins import PluginBase
from hxntools.detectors.xspress3 import (XspressTrigger, Xspress3Detector, Xspress3Channel, Xspress3FileStore)


class CLSXspress3Detector(XspressTrigger, Xspress3Detector):
    roi_data = Cpt(PluginBase, 'ROIDATA:')
    channel1 = Cpt(Xspress3Channel, 'C1_', channel_num=1, read_attrs=['rois'])
    channel2 = Cpt(Xspress3Channel, 'C2_', channel_num=2, read_attrs=['rois'])
    channel3 = Cpt(Xspress3Channel, 'C3_', channel_num=3, read_attrs=['rois'])
    channel4 = Cpt(Xspress3Channel, 'C4_', channel_num=4, read_attrs=['rois'])
    channel5 = Cpt(Xspress3Channel, 'C5_', channel_num=4, read_attrs=['rois'])
    channel6 = Cpt(Xspress3Channel, 'C6_', channel_num=4, read_attrs=['rois'])
    channel7 = Cpt(Xspress3Channel, 'C7_', channel_num=1, read_attrs=['rois'])
    channel8 = Cpt(Xspress3Channel, 'C8_', channel_num=2, read_attrs=['rois'])
    channel9 = Cpt(Xspress3Channel, 'C9_', channel_num=3, read_attrs=['rois'])
    channel10 = Cpt(Xspress3Channel, 'C10_', channel_num=4, read_attrs=['rois'])
    channel11 = Cpt(Xspress3Channel, 'C11_', channel_num=4, read_attrs=['rois'])
    channel12 = Cpt(Xspress3Channel, 'C12_', channel_num=4, read_attrs=['rois'])
    hdf5 = Cpt(Xspress3FileStore, 'HDF5:',
               read_path_template='/tmp',
               root='/',
               write_path_template='/tmp')

    def __init__(self, prefix, *, configuration_attrs=None, read_attrs=None,
                 **kwargs):
        if configuration_attrs is None:
            configuration_attrs = ['external_trig', 'total_points',
                                   'spectra_per_point', 'settings',
                                   'rewindable']
        if read_attrs is None:
            read_attrs = [f'channel{x}' for x in range(1, 13)] + ['hdf5']
        super().__init__(prefix, configuration_attrs=configuration_attrs,
                         read_attrs=read_attrs, **kwargs)
        self.set_channels_for_hdf5()

    def set_channels_for_hdf5(self, channels=list(range(1, 13))):
        """
        Configure which channels' data should be saved in the resulted hdf5 file.
        Parameters
        ----------
        channels: tuple, optional
            the channels to save the data for
        """
        # The number of channel
        for n in channels:
            getattr(self, f'channel{n}').rois.read_attrs = ['roi{:02}'.format(j) for j in [1, 2, 3, 4]]
        self.hdf5.num_extra_dims.put(0)
        self.settings.num_channels.put(len(channels))


xs_inboard = CLSXspress3Detector('PDTR1607-701:', name='xs_inboard')
xs_outboard = CLSXspress3Detector('PDTR1607-703:', name='xs_outboard')
