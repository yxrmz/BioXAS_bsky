# TODO: have hxntools installed either from
# - the nsls2forge conda channel
# or
# - https://github.com/NSLS-II-HXN/hxntools
from hxntools.detectors.zebra import Zebra, HxnZebra


zebra = HxnZebra('TRG1607-701:', name='zebra')
