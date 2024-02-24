def check(prioritizedList, jdamMapping, timeAvailable):
    kills = 0
    misses = 0
    while timeAvailable > 0:
        for targetCriteria in sorted(prioritizedList, key = lambda x: x[1]):
            if (timeAvailable - targetCriteria[1]) >= 0:
                if jdamMapping[targetCriteria[2]] >= targetCriteria[3]:
                    jdamMapping[targetCriteria[2]] -= targetCriteria[3]
                    kills += 1
                else:
                    misses += 1
                timeAvailable -= targetCriteria[1]
            else:
                timeAvailable = 0
                break
    return kills/(kills+misses) * 100
