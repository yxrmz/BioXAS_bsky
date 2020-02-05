def scan_bundle(bundle, num_points): 
    yield from bps.open_run() 
    yield from bps.mv(bundle.num_points, num_points)
    yield from bps.stage(bundle) 
    for i in range(num_points): 
        yield from bps.trigger_and_read([bundle]) 
    yield from bps.unstage(bundle) 
    yield from bps.close_run() 

