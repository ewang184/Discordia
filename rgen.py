import random    

def generateLevelUp(currentstats):
    
    LVL = currentstats[1] + 1
    HP = currentstats[2] * random.uniform(1.1,1.3)
    ATK = currentstats[3] * random.uniform(1.1,1.3)
    DEF = currentstats[4] * random.uniform(1.1,1.3)
    RES = currentstats[5] * random.uniform(1.1,1.3)
    SPD = currentstats[6] * random.uniform(1.1,1.3)
    DEX = currentstats[7] * random.uniform(1.1,1.3)
    WIS = currentstats[8] * random.uniform(1.1,1.3)
    ITL = currentstats[9] * random.uniform(1.1,1.3)
    CRITD = currentstats[10] * random.uniform(1.1,1.3)
    CRITC = currentstats[11]
    newstats = (LVL, HP, ATK, DEF, RES, SPD, DEX, WIS, ITL, CRITD, CRITC)
    return newstats
    
def generateStats(floornumber):
    LVL = random.randint(0,floornumber)
    skillpoints = round(1.1**LVL * 10)
    addthis = 0

    addthis = random.randint(0,skillpoints)
    skillpoints -= addthis
    HP = round(LVL**(random.uniform(1,1.3)) * 20) + addthis

    addthis = random.randint(0,skillpoints)
    skillpoints -= addthis
    ATK = round(LVL**(random.uniform(1,1.3)) * 2) + addthis

    addthis = random.randint(0,skillpoints)
    skillpoints -= addthis
    ITL = round(LVL**(random.uniform(1,1.3)) * 2) + addthis

    addthis = random.randint(0,skillpoints)
    skillpoints -= addthis
    DEF = round(LVL**(random.uniform(1,1.3)) * 2) + addthis

    addthis = random.randint(0,skillpoints)
    skillpoints -= addthis
    RES = round(LVL**(random.uniform(1,1.3)) * 2) + addthis

    addthis = random.randint(0,skillpoints)
    skillpoints -= addthis
    SPD = round(LVL**(random.uniform(1,1.3)) * 2) + addthis

    addthis = random.randint(0,skillpoints)
    skillpoints -= addthis
    DEX = round(LVL**(random.uniform(1,1.3)) * 2) + addthis

    addthis = random.randint(0,skillpoints)
    skillpoints -= addthis
    WIS = round(LVL**(random.uniform(1,1.3)) * 2) + addthis

    addthis = random.randint(0,skillpoints)
    skillpoints -= addthis
    CRITD = round(LVL**(random.uniform(1,1.3)) * 2) + addthis

    CRITC = 5

    unum = LVL + floornumber
    
    statsTuple = (unum, LVL, HP, ATK, DEF, RES, SPD, DEX, WIS, ITL, CRITD, CRITC)

    return statsTuple


def generateLoot(floornumber):
    possiblestats = []
    possiblestats.append("HP")
    possiblestats.append("ATK")
    possiblestats.append("DEF")
    possiblestats.append("RES")
    possiblestats.append("SPD")
    possiblestats.append("DEX")
    possiblestats.append("WIS")
    possiblestats.append("ITL")
    possiblestats.append("CRITD")
    possiblestats.append("CRITC")
    items = open("items.txt","r")
    items = items.read()
    items = items.split()
    number = round(random.randint(0,71))
    item = items[number]

    statchoice = random.randint(0,9)
    if statchoice == 9 or statchoice == 8:
        num = round(random.normalvariate(10, 5))
    else:
        num = round(random.normalvariate(floornumber, floornumber/4))
    effect1 = str(possiblestats[statchoice])+" + "+str(num)

    statchoice = random.randint(0,9)
    if statchoice == 9 or statchoice == 10:
        num = round(random.normalvariate(10, 5))
    else:
        num = round(random.normalvariate(floornumber, floornumber/4))
    effect2 = str(possiblestats[statchoice])+" + "+str(num)

    statchoice = random.randint(0,9)
    if statchoice == 9 or statchoice == 10:
        num = round(random.normalvariate(10, 5))
    else:
        num = round(random.normalvariate(floornumber, floornumber/4))
    effect3 = str(possiblestats[statchoice])+" + "+str(num)

    statchoice = random.randint(0,9)
    if statchoice == 9 or statchoice == 10:
        num = round(random.normalvariate(10, 5))
    else:
        num = round(random.normalvariate(floornumber, floornumber/4))
    effect4 = str(possiblestats[statchoice])+" + "+str(num)
    
    itemtuple = (item, effect1, effect2, effect3, effect4)

    return itemtuple

def generateEXP(LVL):
    dropexp = round(1/10*LVL**2 +1)
    return dropexp

def generateConsume(floornumber):
    possiblestats = []
    possiblestats.append("HP")
    possiblestats.append("ATK")
    possiblestats.append("DEF")
    possiblestats.append("RES")
    possiblestats.append("SPD")
    possiblestats.append("DEX")
    possiblestats.append("WIS")
    possiblestats.append("ITL")
    possiblestats.append("CRITD")
    possiblestats.append("CRITC")

    eats = open("consumables.txt","r")
    eats = eats.read()
    eats = eats.split()
    number = round(random.randint(0,64))
    name = eats[number]

    statchoice = random.randint(0,9)
    if statchoice == 9 or statchoice == 8:
        num = round(random.normalvariate(10, 5))
    else:
        num = round(random.normalvariate(floornumber, floornumber/4))
    effect = str(possiblestats[statchoice])+" + "+str(num)

    consumtuple = (name, effect)
    return consumtuple

def generateName(LVL, floornumber):
    names = open("monsters.txt", "r")
    names = names.read()
    names = names.split()

    num = round(random.normalvariate(floornumber*4, LVL))

    if num > 443:
        num = 443

    finalname = names[num]

    return finalname
    
