import numpy as np

def log(l, s):
    if l:
        print(str(s))
        
def trial(l=False, probability_day_outbreak=.01, snap_lockdown_time=3,
         probability_lockdown_extension=.3, 
         reduce_in_lockdown=False,
         vaccines=False,
         vaccine_decay=0,
         add_time=7,
         extend_time=3
         ):
    lockdown_days = 0
    lockdown_count = 0
    lockdown = False
    days_remaining = 0

    for i in range(365):
        log(l, f"Day: {i}")
        days_remaining = max(0, days_remaining-1) # Days left in current lockdown if any
        current_chance = probability_day_outbreak # Chance of a new outbreak today
        if vaccines: # as the population get vaccinated, the outbreak chance will drop
            # Outbreak chance drops to zero in vaccine_decay months
            current_chance = probability_day_outbreak + i*(-probability_day_outbreak/(30*vaccine_decay))
        if reduce_in_lockdown and lockdown: 
            # If already in lockdown, reduce the outbreak chance by 75%
            current_chance *= 0.25
        rolled = np.random.random() # Is there an outbreak today?
        log(l, f"Chance of outbreak {current_chance:.3f} - rolled {rolled:.3f}")
        if rolled <= current_chance:
            log(l, "Outbreak!")
            if not lockdown:
                # Start a new lockdown
                lockdown = True
                lockdown_count += 1
                days_remaining = snap_lockdown_time
            else:
                # New outbreak in existing lockdown, extend the current time a bit
                days_remaining += add_time

        if lockdown and days_remaining <= 0:
            # End of a lockdown reached
            log(l,"Lockdown ending?")
            if np.random.random() < probability_lockdown_extension:
                # Lockdown extended by a short period
                log(l,"Nope, short extension")
                days_remaining += extend_time
            else:
                # End the lockdown for real
                lockdown = False

        # Cap lockdown time to 14 days in the future
        days_remaining = min(days_remaining, 14) 

        if lockdown:
            lockdown_days += 1
        log(l, f"{days_remaining} remaining\n")
    return lockdown_days, lockdown_count

def sims(N=1000, probability_day_outbreak=.01, snap_lockdown_time=3,
         probability_lockdown_extension=.3,
         reduce_in_lockdown=False,
         vaccines=False,
         vaccine_decay=0,
         add_time=7,
         extend_time=3
         ):
    results = np.zeros(N) # days
    counts = np.zeros(N) # lockdowns
    for i in range(N):
        res = trial(probability_day_outbreak=probability_day_outbreak, snap_lockdown_time=snap_lockdown_time,
         probability_lockdown_extension=probability_lockdown_extension,
         reduce_in_lockdown=reduce_in_lockdown,
         vaccines=vaccines,
         vaccine_decay=vaccine_decay,
         add_time=add_time,
         extend_time=extend_time
         )
        results[i] = res[0]
        counts[i] = res[1]

    return results, counts
