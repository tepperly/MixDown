mdDefinePrefix = "_prefix"
mdDefineJobSlots = "_jobslots"

#GNU make strings
mdMakeJobSlotsPrefix = "-j"
mdMakeJobSlotsDefineName = "_makejobslots"
mdMakeJobSlotsDefineValue = mdMakeJobSlotsPrefix + "$(" + mdDefineJobSlots + ")"