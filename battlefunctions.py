from rgen import generateStats
from rgen import generateName
from rgen import generateLoot
from rgen import generateEXP
from rgen import generateConsume
import random

def adventure(p1):
    floor = p1.LVL
    combatlog = []
    combatlog.append("")
    combatlog.append([])
    combatlog.append([])
    combatlog.append([1])
    while p1.HP > 0:
        monStats = generateStats(floor)
        monAbility = ""
        monEquip = ""
        monName = generateName(monStats[1],floor)
        enemy = createCharacterCard(monStats, monAbility, monEquip, monName)
        if advcombat(p1, enemy):
            combatlog[0] += p1.name+" defeated "+enemy.name+ "\n"

            droprate = random.randint(0,99)
            if droprate < 10:
                combatlog[1].append(generateLoot(floor))
            droprate = random.randint(0,99)
            if droprate < 10: 
                combatlog[2].append(generateConsume(floor))
            
            expgain = generateEXP(monStats[0])
            combatlog[3][0]+=expgain
            
            floor += 1
        else:
            combatlog[0] += enemy.name+" defeated "+p1.name+ "\n"
            combatlog[0] += "Enemy stats were: "+str(monStats)+"\n"
            combatlog[0] += "Loot gathered: "+str(combatlog[1])+"\n"
            combatlog[0] += "Consumables gathered: "+str(combatlog[2])
            break
        if floor > p1.LVL+20:
            combatlog[0] += "Loot gathered: "+str(combatlog[1])+"\n"
            combatlog[0] += "Consumables gathered: "+str(combatlog[2])
            break
    return combatlog
    

def advcombat (p1, p2):
    dp1 = 0;
    dp2 = 0;
    p1name = p1.name
    p2name = p2.name
    won = False
    while p1.HP>0 and p2.HP>0:
        dp1 += p1.SPD
        dp2 += p2.SPD
        
        if dp1 > 100:
            dp1 = dp1-100;

            didcrit = random.randint(0,100)
            if didcrit<p1.CRITC:
                atkpower = round((max(0, (p1.ATK-p2.DEF)) + max(0, (p1.ITL-p2.RES)) + 5) * (100+p1.CRITD)/100)
            else:
                atkpower = (max(0, (p1.ATK-p2.DEF)) + max(0, (p1.ITL-p2.RES)) + 5)
            p2.HP -= atkpower
            if p2.HP<=0:
                won = True
                break
            
            
        if dp2 >100:
            dp2 = dp2-100;

            didcrit = random.randint(0,100)
            if didcrit<p2.CRITC:
                atkpower = round((max(0, (p2.ATK-p1.DEF)) + max(0, (p2.ITL-p1.RES)) + 5) * (100+p2.CRITD)/100)
            else:
                atkpower = (max(0, (p2.ATK-p1.DEF)) + max(0, (p2.ITL-p1.RES)) + 5)
            p1.HP -= atkpower
            if p1.HP<=0:
                won = False
                break
    return won

def combat (p1, p2):
    dp1 = 0;
    dp2 = 0;
    p1name = p1.name
    p2name = p2.name
    
    combatlog = ""
    while p1.HP>0 and p2.HP>0:
        dp1 += p1.SPD
        dp2 += p2.SPD
        if dp1 > 100:
            dp1 = dp1-100;
            didcrit = random.randint(0,100)
            if didcrit<p1.CRITC:
                atkpower = round((max(0, (p1.ATK-p2.DEF)) + max(0, (p1.ITL-p2.RES)) + 5) * (100+p1.CRITD)/100)
                combatlog += str(p1name)+" crit for "+str(atkpower)+" damage \n"
            else:
                atkpower = (max(0, (p1.ATK-p2.DEF)) + max(0, (p1.ITL-p2.RES)) + 5)
                combatlog += str(p1name)+" hit for "+str(atkpower)+" damage \n"
            p2.HP -= atkpower

            if p2.HP<=0:
                combatlog += str(p2name)+" died \n"
                break
            
            
        if dp2 >100:
            dp2 = dp2-100;
            didcrit = random.randint(0,100)
            if didcrit<p2.CRITC:
                atkpower = round((max(0, (p2.ATK-p1.DEF)) + max(0, (p2.ITL-p1.RES)) + 5) * (100+p2.CRITD)/100)
                combatlog += str(p2name)+" crit for "+str(atkpower)+" damage \n"
            else:
                atkpower = (max(0, (p2.ATK-p1.DEF)) + max(0, (p2.ITL-p1.RES)) + 5)
                combatlog += str(p2name)+" hit for "+str(atkpower)+" damage \n"
            p1.HP -= atkpower
            
            if p1.HP<=0:
                combatlog += str(p1name)+" died \n"
                break
        

    return combatlog



class createCharacterCard:
    def __init__ (self, ustats, uability, uequip, name):
        self.name = name
        self.LVL=ustats[1]
        self.HP=ustats[2]
        self.ATK=ustats[3]
        self.DEF=ustats[4]
        self.RES=ustats[5]
        self.SPD=ustats[6]
        self.DEX=ustats[7]
        self.WIS=ustats[8]
        self.ITL=ustats[9]
        self.CRITD=ustats[10]
        self.CRITC=ustats[11]
        self.abilities = uability
        self.equipment = uequip


        #abilites are skills
        #equips are passives

        
        for x in self.equipment:
            for y in x:
                command = y.split()
                if len(command)>1:
                    statChange = command[0]
                    changetype = command[1]
                    changevalue = int(command[2])

                    if statChange == "HP":
                        if changetype == "+":
                            self.HP += changevalue
                        elif changetype == "-":
                            self.HP -= changevalue
                        elif changetype == "*":
                            self.HP *= changevalue
                        elif changetype == "/":
                            self.HP /= changevalue

                    if statChange == "ATK":
                        if changetype == "+":
                            self.ATK += changevalue
                        elif changetype == "-":
                            self.ATK -= changevalue
                        elif changetype == "*":
                            self.ATK *= changevalue
                        elif changetype == "/":
                            self.ATK /= changevalue

                    if statChange == "DEF":
                        if changetype == "+":
                            self.DEF += changevalue
                        elif changetype == "-":
                            self.DEF -= changevalue
                        elif changetype == "*":
                            self.DEF *= changevalue
                        elif changetype == "/":
                            self.DEF /= changevalue

                    if statChange == "RES":
                        if changetype == "+":
                            self.RES += changevalue
                        elif changetype == "-":
                            self.RES -= changevalue
                        elif changetype == "*":
                            self.RES *= changevalue
                        elif changetype == "/":
                            self.RES /= changevalue

                    if statChange == "SPD":
                        if changetype == "+":
                            self.SPD += changevalue
                        elif changetype == "-":
                            self.SPD -= changevalue
                        elif changetype == "*":
                            self.SPD *= changevalue
                        elif changetype == "/":
                            self.SPD /= changevalue

                    if statChange == "DEX":
                        if changetype == "+":
                            self.DEX += changevalue
                        elif changetype == "-":
                            self.DEX -= changevalue
                        elif changetype == "*":
                            self.DEX *= changevalue
                        elif changetype == "/":
                            self.DEX /= changevalue

                    if statChange == "WIS":
                        if changetype == "+":
                            self.WIS += changevalue
                        elif changetype == "-":
                            self.WIS -= changevalue
                        elif changetype == "*":
                            self.WIS *= changevalue
                        elif changetype == "/":
                            self.WIS /= changevalue

                    if statChange == "ITL":
                        if changetype == "+":
                            self.ITL += changevalue
                        elif changetype == "-":
                            self.ITL -= changevalue
                        elif changetype == "*":
                            self.ITL *= changevalue
                        elif changetype == "/":
                            self.ITL /= changevalue

                    if statChange == "CRITD":
                        if changetype == "+":
                            self.CRITD += changevalue
                        elif changetype == "-":
                            self.CRITD -= changevalue
                        elif changetype == "*":
                            self.CRITD *= changevalue
                        elif changetype == "/":
                            self.CRITD /= changevalue

                    if statChange == "CRITC":
                        if changetype == "+":
                            self.CRITC += changevalue
                        elif changetype == "-":
                            self.CRITC -= changevalue
                        elif changetype == "*":
                            self.CRITC *= changevalue
                        elif changetype == "/":
                            self.CRITC /= changevalue

            

