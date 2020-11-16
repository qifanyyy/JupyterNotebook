import numpy as np

def getAlgorithms():
    return [
        "blda",
        "bldh",
        "bldw",
        "BLhillClimber",
        "blia",
        "blih",
        "bliw",
        "BLmls_1_1",
        "BLmls_1_2",
        "BLmls_1_5",
        "BLsa_0.606531_1_10000",
        "BLsa_0.606531_1_1000",
        "BLsa_0.899661_3_1000",
        "BLsa_0.995282_1_10000",
        "BLts_100_46",
        "BLts2_1_46",
        "BLts_215_215",
        "BLts2_22_22",
        "BLts_2_22",
        "BLts_22_46",
        "BLts2_5_100",
        "BLts2_5_46",
        "gg_heightAsc_bestFit",
        "gg_heightAsc_bestFit_rotated",
        "gg_heightAsc_nextFit",
        "gg_heightAsc_nextFit_rotated",
        "gg_heightAsc_worstFit",
        "gg_heightAsc_worstFit_rotated",
        "gg_heightDsc_bestFit",
        "gg_heightDsc_bestFit_rotated",
        "gg_heightDsc_nextFit",
        "gg_heightDsc_nextFit_rotated",
        "gg_heightDsc_worstFit",
        "gg_heightDsc_worstFit_rotated",
        "gg_widthAsc_bestFit",
        "gg_widthAsc_bestFit_rotated",
        "gg_widthAsc_nextFit",
        "gg_widthAsc_nextFit_rotated",
        "gg_widthAsc_worstFit",
        "gg_widthAsc_worstFit_rotated",
        "gg_widthDsc_bestFit",
        "gg_widthDsc_bestFit_rotated",
        "gg_widthDsc_nextFit",
        "gg_widthDsc_nextFit_rotated",
        "gg_widthDsc_worstFit",
        "gg_widthDsc_worstFit_rotated",
        "graspBlda_5",
        "graspBldh_10",
        "graspBldh_5",
        "graspBldw_1000",
        "graspBldw_2",
        "graspBldw_5",
        "SHhillClimber",
        "SHsa_0.606531_10_10000",
        "SHsa_0.899661_1_10000",
        "SHsa_0.977887_10_10000"
]

def getGreedyAlgorithms():
    return set([
        "blda",
        "bldh",
        "bldw",
        "blia",
        "blih",
        "bliw",
        "gg_heightAsc_bestFit",
        "gg_heightAsc_bestFit_rotated",
        "gg_heightAsc_nextFit",
        "gg_heightAsc_nextFit_rotated",
        "gg_heightAsc_worstFit",
        "gg_heightAsc_worstFit_rotated",
        "gg_heightDsc_bestFit",
        "gg_heightDsc_bestFit_rotated",
        "gg_heightDsc_nextFit",
        "gg_heightDsc_nextFit_rotated",
        "gg_heightDsc_worstFit",
        "gg_heightDsc_worstFit_rotated",
        "gg_widthAsc_bestFit",
        "gg_widthAsc_bestFit_rotated",
        "gg_widthAsc_nextFit",
        "gg_widthAsc_nextFit_rotated",
        "gg_widthAsc_worstFit",
        "gg_widthAsc_worstFit_rotated",
        "gg_widthDsc_bestFit",
        "gg_widthDsc_bestFit_rotated",
        "gg_widthDsc_nextFit",
        "gg_widthDsc_nextFit_rotated",
        "gg_widthDsc_worstFit",
        "gg_widthDsc_worstFit_rotated"
])

def getTimePoints():
    timePoints = []
    t = 20
    second = 1000
    hour = second*3600
    n = 500
    dt = (np.log(hour)-np.log(t))/n
    ct = np.log(t)
    for i in range(n):
        timePoints.append(np.exp(ct))
        ct+=dt
    return np.array(timePoints)

def getNames():
    return ["0-999", "300-699", "400-799", "500-999", "700-999", "1000-1999", "1000-2206"]

def getRange(s):
    a, b = [int(x) for x in s.split("-")]
    return [x for x in range(a, b+1)]