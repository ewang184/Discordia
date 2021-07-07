def generateStatBoost(currentstats, toconsume):
    unum = currentstats[0]
    LVL = currentstats[1]
    HP = currentstats[2] 
    ATK = currentstats[3]
    DEF = currentstats[4]
    RES = currentstats[5]
    SPD = currentstats[6]
    DEX = currentstats[7]
    WIS = currentstats[8]
    ITL = currentstats[9]
    CRITD = currentstats[10]
    CRITC = currentstats[11]

    food = toconsume[1]
    consumable = food.split() 
    value = int(consumable[2])

    if consumable[0] == "HP":
        HP += value
    if consumable[0] == "ATK":
        ATK += value
    if consumable[0] == "DEF":
        DEF += value
    if consumable[0] == "RES":
        RES += value
    if consumable[0] == "SPD":
        SPD += value
    if consumable[0] == "DEX":
        DEX += value
    if consumable[0] == "WIS":
        WIS += value
    if consumable[0] == "ITL":
        ITL += value
    if consumable[0] == "CRITD":
        CRITD += value
    if consumable[0] == "CRITC":
        CRITC += value
    
    statsTuple = (unum, LVL, HP, ATK, DEF, RES, SPD, DEX, WIS, ITL, CRITD, CRITC)

    return statsTuple
