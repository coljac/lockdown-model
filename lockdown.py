import numpy as np

def log(l, s):
    if l:
        print(str(s))
        
def trial(l=False, probability_day_outbreak=.01, snap_lockdown_time=3,
         probability_lockdown_extension=.3, probability_decay=1):
    lockdown_days = 0
    lockdown = False
    days_remaining = 0
    for i in range(365):
        log(l, f"Day: {i}")
        days_remaining = max(0, days_remaining-1)
        if np.random.random() <= probability_day_outbreak:
            log(l, "Outbreak!")
            if not lockdown:
                lockdown = True
                days_remaining = snap_lockdown_time
            else:
                days_remaining += 7
        if lockdown and days_remaining <= 0:
            log(l,"Lockdown ending")
            if np.random.random() < probability_lockdown_extension:
                log(l,"Nope, short extension")
                days_remaining += 3
            else:
                lockdown = False
        days_remaining = min(days_remaining, 14)
        if lockdown:
            lockdown_days += 1
        log(l, f"{days_remaining} remaining\n")
    return lockdown_days

def sims(N=1000, probability_day_outbreak=.01, snap_lockdown_time=3,
         probability_lockdown_extension=.3):
    results = np.zeros(N)
    for i in range(N):
        results[i] = trial(probability_day_outbreak=probability_day_outbreak, snap_lockdown_time=snap_lockdown_time,
         probability_lockdown_extension=probability_lockdown_extension)
    return results
