import discord
import os
import mysql.connector
import math
from battlefunctions import createCharacterCard
from battlefunctions import combat
from battlefunctions import adventure
from noncombat import generateStatBoost
from rgen import generateLevelUp
from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
  host=os.getenv("HOST"),
  user=os.getenv("ADMIN"),
  password=os.getenv("PASSWORD"),
    database=os.getenv("DATABASE")
)
mycursor = mydb.cursor()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
####################### complete section
    if message.content.startswith('|register'):
        if len(message.content.split()) > 1:
            mycursor.execute("SELECT UID FROM users")
            usrs = mycursor.fetchall()
            usrString = []
            for x in usrs:
                usrString.append("".join(x))
                
            regUse = message.content.split()
            
            if str(message.author) not in usrString:
                authorname = str(message.author)
                messauth = authorname[len(authorname)-4:len(authorname)]
                sql = "INSERT INTO users (UID, UNUM, UNAME, EXP) VALUES (%s, %s, %s, %s)"
                val = (str(message.author), messauth, str(regUse[1]), 0)
                mycursor.execute(sql, val)
                mydb.commit()
                await message.channel.send('User '+str(message.author)+" registered with name "+regUse[1])

                sql = "INSERT INTO ustats (user_num, LVL, HP, ATK, DEF, RES, SPD, DEX, WIS, ITL, CRITD, CRITC) VALUES ("+str(messauth)+", 1, 100, 5, 5, 5, 5, 5, 5, 5, 5, 5)"
                mycursor.execute(sql)
                mydb.commit()
                await message.channel.send("Character initialized")

                authorname = str(message.author)
                messauth = authorname[len(authorname)-4:len(authorname)]
                sql = "CREATE TABLE "+messauth+"item (item MEDIUMTEXT, effect1 MEDIUMTEXT, effect2 MEDIUMTEXT, effect3 MEDIUMTEXT, effect4 MEDIUMTEXT);"
                mycursor.execute(sql)
                mydb.commit()
                sql = "CREATE TABLE "+messauth+"ability (name MEDIUMTEXT, effect MEDIUMTEXT, cooldown int, maxcd int);"
                mycursor.execute(sql)
                mydb.commit()
                sql = "CREATE TABLE "+messauth+"equip (item MEDIUMTEXT, effect1 MEDIUMTEXT, effect2 MEDIUMTEXT, effect3 MEDIUMTEXT, effect4 MEDIUMTEXT);"
                mycursor.execute(sql)
                mydb.commit()
                sql = "CREATE TABLE "+messauth+"consumable (item MEDIUMTEXT, effect MEDIUMTEXT);"
                mycursor.execute(sql)
                mydb.commit()
                
            else:
                sql = "UPDATE users SET UNAME = '" +str(regUse[1])+ "' WHERE UID ='"+str(message.author)+"'"
                mycursor.execute(sql)
                mydb.commit()
                await message.channel.send("```"+'User '+str(message.author)+' changed name to '+regUse[1]+"```")
        else:
            await message.channel.send("```"+"Please register in format |Register yournamehere"+"```")
####################### complete section


####################### complete section
    if message.content.startswith("|listplayers"):
        mycursor.execute("SELECT UID FROM users")
        usrs = mycursor.fetchall()
        usrString = []
        for x in usrs:
            usrString.append("".join(x))

        if len(usrString)>0:
            await message.channel.send("```"+str(usrString)+"```")
        else:
            await message.channel.send("```"+"No players"+"```")
####################### complete section
            
####################### complete section
    if message.content.startswith("|challenge"):
        if len(message.content.split()) > 1:
            otherplayer = message.content.split()
            
            mycursor.execute("SELECT UNUM FROM users WHERE UID='"+str(message.author)+"';")
            userID = mycursor.fetchall()
            userID = userID[0][0]

            mycursor.execute("SELECT * FROM ustats WHERE user_num="+str(userID)+";")
            userStats = mycursor.fetchall()
            userStats = userStats[0]

            mycursor.execute("SELECT * FROM "+str(userID)+"item;")
            userItems = mycursor.fetchall()

            mycursor.execute("SELECT * FROM "+str(userID)+"ability;")
            userAbility = mycursor.fetchall()

            mycursor.execute("SELECT * FROM "+str(userID)+"equip;")
            userequip = mycursor.fetchall()

            mycursor.execute("SELECT UNAME FROM users WHERE UID='"+str(message.author)+"';")
            name = mycursor.fetchall()
            name = name[0][0]
            
            p1 = createCharacterCard(userStats,userAbility,userequip, name)

            mycursor.execute("SELECT UNUM FROM users WHERE UID='"+str(otherplayer[1])+"';")
            userID = mycursor.fetchall()
            userID = userID[0][0]

            mycursor.execute("SELECT * FROM ustats WHERE user_num="+str(userID)+";")
            userStats = mycursor.fetchall()
            userStats = userStats[0]

            mycursor.execute("SELECT * FROM "+str(userID)+"item;")
            userItems = mycursor.fetchall()

            mycursor.execute("SELECT * FROM "+str(userID)+"ability;")
            userAbility = mycursor.fetchall()

            mycursor.execute("SELECT * FROM "+str(userID)+"equip;")
            userequip = mycursor.fetchall()

            mycursor.execute("SELECT UNAME FROM users WHERE UID='"+str(otherplayer[1])+"';")
            name = mycursor.fetchall()
            name = name[0][0]

            p2 = createCharacterCard(userStats,userAbility,userequip, name)

            await message.channel.send("```"+str(combat(p1,p2))+"```")
        else:
            await message.channel.send("```"+"Please challenge in format |challenge otherplayername#discordnumber"+"```")
####################### complete section

####################### complete section
    if message.content.startswith("|unequip"): 
        mycursor.execute("SELECT UNUM FROM users WHERE UID='"+str(message.author)+"';")
        userID = mycursor.fetchall()
        userID = userID[0][0]

        items = message.content.split()
        if len(items) > 1:
            del items[0]

            mycursor.execute("SELECT * FROM "+str(userID)+"equip;")
            equipment = mycursor.fetchall()

            for x in items:
                equipment[int(x)] = ("","","")
            
            mycursor.execute("DELETE FROM "+str(userID)+"equip;")
            mydb.commit()

            for x in equipment:
                if x != ("","",""):
                    sql = "INSERT INTO " +str(userID)+"equip (item, effect1, effect2, effect3, effect4) VALUES (%s, %s, %s, %s, %s)"
                    val = (x[0], x[1], x[2], x[3], x[4])
                    mycursor.execute(sql, val)
        else:
            mycursor.execute("DELETE FROM "+str(userID)+"equip;")
            mydb.commit()
            
        await message.channel.send("```"+"Items have been unequipped"+"```")

    if message.content.startswith("|equip"):
        mycursor.execute("SELECT UNUM FROM users WHERE UID='"+str(message.author)+"';")
        userID = mycursor.fetchall()
        userID = userID[0][0]

        mycursor.execute("SELECT COUNT(*) FROM "+str(userID)+"equip;")
        currentequipped = mycursor.fetchall()
        currentequipped = currentequipped[0][0]
        
        toequipnum = message.content.split()
        del toequipnum[0]
        mycursor.execute("SELECT * FROM "+str(userID)+"item;")
        equipment = mycursor.fetchall()
        toequip = []
        for x in range(len(toequipnum)):
            toequip.append(equipment[int(toequipnum[x])])
        if len(toequip)<=(6-int(currentequipped)):
            for x in toequip:
                sql = "INSERT INTO " +str(userID)+"equip (item, effect1, effect2, effect3, effect4) VALUES (%s, %s, %s, %s, %s)"
                val = (x[0], x[1], x[2], x[3], x[4])
                mycursor.execute(sql, val)
            await message.channel.send("```"+"Items have been equipped"+"```")
        else:
            await message.channel.send("```"+"Too many items selected: amount left is "+str((6-int(currentequipped)))+"```")
####################### complete section
    if message.content.startswith("|levelup"):
        mycursor.execute("SELECT UNUM FROM users WHERE UID='"+str(message.author)+"';")
        userID = mycursor.fetchall()
        userID = userID[0][0]

        mycursor.execute("SELECT EXP FROM users WHERE UID='"+str(message.author)+"';")
        userxp = mycursor.fetchall()
        userxp = userxp[0][0]

        mycursor.execute("SELECT * FROM ustats WHERE user_num="+str(userID))
        userstats = mycursor.fetchall()
        userstats = userstats[0]

        mycursor.execute("SELECT LVL FROM ustats WHERE user_num="+str(userID))
        userlvl = mycursor.fetchall()
        userlvl = userlvl[0][0]

        EXPneeded = round(71*math.log(userlvl)**2 +1)
        if userxp > EXPneeded:
            userxp -=EXPneeded
            x = generateLevelUp(userstats)
            sql = "UPDATE ustats SET LVL= %s, HP = %s, ATK = %s, DEF= %s, RES=%s, SPD = %s, DEX = %s, WIS = %s, ITL = %s, CRITD = %s, CRITC = %s WHERE user_num = "+str(userID)
            val = (x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10])
            mycursor.execute(sql, val)
            mydb.commit()
            mycursor.execute("UPDATE users SET EXP = "+str(userxp)+" WHERE UNUM = "+str(userID))
            await message.channel.send("```"+str(message.author)+" has levelled up!"+"```")
        else:
            await message.channel.send("```"+"Not enough EXP"+"```")
        

        
        
####################### complete section
    if message.content.startswith("|items"):
        mycursor.execute("SELECT UNUM FROM users WHERE UID='"+str(message.author)+"';")
        userID = mycursor.fetchall()
        userID = userID[0][0]

        page = message.content.split()
        mycursor.execute("SELECT * FROM "+str(userID)+"item;")
        userItems = mycursor.fetchall()

        itemsLog = ""
        page[1] = str(int(page[1])-1)
        for x in range(int(page[1])*10, int(page[1])*10+10):
            if x > len(userItems)-1:
                itemsLog += "No more items \n"
            else:
                itemsLog += str(x)+": "+str(userItems[x])+"\n"
        await message.channel.send("```"+itemsLog+"```")

    if message.content.startswith("|consumables"):
        mycursor.execute("SELECT UNUM FROM users WHERE UID='"+str(message.author)+"';")
        userID = mycursor.fetchall()
        userID = userID[0][0]

        mycursor.execute("SELECT * FROM "+str(userID)+"consumable;")
        userConsumables = mycursor.fetchall()

        page = message.content.split()
        consumablesLog = ""
        page[1] = str(int(page[1])-1)
        for x in range(int(page[1])*10, int(page[1])*10+10):
            if x > len(userConsumables)-1:
                consumablesLog += "No more consumables \n"
            else:
                consumablesLog += str(x)+": "+str(userConsumables[x])+"\n"
        await message.channel.send("```"+consumablesLog+"```")


    if message.content.startswith("|use"):
        mycursor.execute("SELECT UNUM FROM users WHERE UID='"+str(message.author)+"';")
        userID = mycursor.fetchall()
        userID = userID[0][0]

        mycursor.execute("SELECT * FROM "+str(userID)+"consumable;")
        userConsumables = mycursor.fetchall()

        tousenum = message.content.split()
        
        toconsume = userConsumables[int(tousenum[1])]
        del userConsumables[int(tousenum[1])]

        #drop from table
        sql = "DELETE FROM "+str(userID)+"consumable;"
        mycursor.execute(sql)
        mydb.commit()
        for x in userConsumables:
            sql = "INSERT INTO " +str(userID)+"consumable (item, effect) VALUES (%s, %s)"
            val = (x[0], x[1])
            mycursor.execute(sql, val)
            mydb.commit()

        mycursor.execute("SELECT * FROM ustats WHERE user_num="+str(userID))
        userstats = mycursor.fetchall()
        userstats = userstats[0]
        x = generateStatBoost(userstats, toconsume)


        sql = "UPDATE ustats SET LVL= %s, HP = %s, ATK = %s, DEF= %s, RES=%s, SPD = %s, DEX = %s, WIS = %s, ITL = %s, CRITD = %s, CRITC = %s WHERE user_num = "+str(userID)
        val = (x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11])
        mycursor.execute(sql, val)
        mydb.commit()
            
        await message.channel.send("```"+"Consumables have been used"+"```")
        
####################### complete section            
    if message.content.startswith("|inspect"):  
        
        if len(message.content.split()) > 1:
            otherplayer = message.content.split()
            mycursor.execute("SELECT UNUM FROM users WHERE UID='"+str(otherplayer[1])+"';")
            userID = mycursor.fetchall()
            userID = userID[0][0]

        else:
            mycursor.execute("SELECT UNUM FROM users WHERE UID='"+str(message.author)+"';")
            userID = mycursor.fetchall()
            userID = userID[0][0]
        inspectlog = ""
        mycursor.execute("SELECT * FROM ustats WHERE user_num="+str(userID)+";")
        stats = mycursor.fetchall()
        stats = stats[0]

        mycursor.execute("SELECT * FROM "+str(userID)+"equip;")
        userequip = mycursor.fetchall()

        possiblestats = []
        possiblestats.append("user_num")
        possiblestats.append("LVL")
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
        for x in range(12):
            inspectlog += str(possiblestats[x])
            inspectlog += ": "
            inspectlog += str(stats[x])
            inspectlog += "\n"

        mycursor.execute("SELECT EXP FROM users WHERE UID='"+str(message.author)+"';")
        userxp = mycursor.fetchall()
        userxp = userxp[0][0]
        inspectlog += "EXP: "+str(userxp)+"\n"

        EXPneeded = round(71*math.log(stats[1])**2 +1)
        inspectlog += "EXP until lvl up: "+str(EXPneeded)+"\n"

        inspectlog = inspectlog + "Equipment: "+str(userequip)+"\n"

        await message.channel.send("```"+inspectlog+"```")
####################### complete section
            
    if message.content.startswith("|adventure"):
        mycursor.execute("SELECT UNUM FROM users WHERE UID='"+str(message.author)+"';")
        userID = mycursor.fetchall()
        userID = userID[0][0]

        mycursor.execute("SELECT * FROM ustats WHERE user_num="+str(userID)+";")
        userStats = mycursor.fetchall()
        userStats = userStats[0]

        mycursor.execute("SELECT * FROM "+str(userID)+"item;")
        userItems = mycursor.fetchall()

        mycursor.execute("SELECT * FROM "+str(userID)+"ability;")
        userAbility = mycursor.fetchall()

        mycursor.execute("SELECT * FROM "+str(userID)+"equip;")
        userequip = mycursor.fetchall()

        mycursor.execute("SELECT UNAME FROM users WHERE UID='"+str(message.author)+"';")
        name = mycursor.fetchall()
        name = name[0][0]
            
        p1 = createCharacterCard(userStats,userAbility,userequip, name)
        result = adventure(p1)
        for x in result[1]:
            sql = "INSERT INTO " +str(userID)+"item (item, effect1, effect2, effect3, effect4) VALUES (%s, %s, %s, %s, %s)"
            val = (x[0], x[1], x[2], x[3], x[4])
            mycursor.execute(sql, val)
            mydb.commit()
        for x in result[2]:
            sql = "INSERT INTO " +str(userID)+"consumable (item, effect) VALUES (%s, %s)"
            val = (x[0], x[1])
            mycursor.execute(sql, val)
            mydb.commit()

        mycursor.execute("SELECT EXP FROM users WHERE UID='"+str(message.author)+"';")
        xp = mycursor.fetchall()
        xp = xp[0][0]
        
        xp = xp + result[3][0]
        sql = "UPDATE users SET EXP = "+str(xp)+" WHERE UID='"+str(message.author)+"';"
        mycursor.execute(sql)
        mydb.commit()
        await message.channel.send("```"+result[0]+"```")
        await message.channel.send("```"+str(result[3][0])+" EXP gained!"+"```")

client.run(os.getenv("TOKEN"))
