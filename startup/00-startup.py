import numpy as np
import matplotlib.pyplot as plt
plt.ion()

import bluesky.plans as bp
import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp
from bluesky.run_engine import RunEngine
from bluesky import SupplementalData
from bluesky.callbacks.best_effort import BestEffortCallback
from bluesky.utils import ts_msg_hook
from ophyd.sim import det

from cls_bsky.bl_base import create_run_engine

RE = create_run_engine()
RE.msg_hook = ts_msg_hook

# Set up SupplementalData.
sd = SupplementalData()
RE.preprocessors.append(sd)

bec = BestEffortCallback()
RE.subscribe(bec)

db = RE.db
