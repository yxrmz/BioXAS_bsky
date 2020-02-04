import bluesky.plans as bp
from bluesky.run_engine import RunEngine
from bluesky import SupplementalData
from bluesky.callbacks.best_effort import BestEffortCallback
from ophyd.sim import det

from cls_bsky.bl_base import create_run_engine

RE = create_run_engine()

# Set up SupplementalData.
sd = SupplementalData()
RE.preprocessors.append(sd)

bec = BestEffortCallback()
RE.subscribe(bec)
