#Bot Name: Hear! Hear! 
#Email: tasdidtahsin@gmail.com
#Developed by Tasdid Tahsin



import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import random
import time
import pymongo
from pymongo import MongoClient

import dbl

intents = discord.Intents.default()


client = commands.AutoShardedBot(shard_count=2, command_prefix = '.', intents = intents)


client.remove_command('help')


token = 'discordBotToken' 
mongoClusterKey0 = 'MongoDB Cluster Key'


cluster0 = MongoClient(mongoClusterKey0)
db = cluster0['hearhear-bot']


l = {}      #timer trigger library
t = {}      #reminder storage library


TopGG_Token = 'TopGG Token'
dbl.DBLClient(client, TopGG_Token, autopost=True) # Autopost will post your guild count every 30 minutes


@client.event
async def on_ready():
    
    print('Bot Activated!\n')
    print(f'Logged in as {client.user.name}\n')
    print('------------------------------\n')
    act = f'debates in {len(client.guilds)} servers [.help]'
    while True:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=act))
        await asyncio.sleep(1800)



@client.event
async def on_command_error(ctx, error):

    lang = 'en'

    try:
        guild = str(ctx.guild.id)

        collection = db['language']
        find = collection.find_one({'_id': guild})
        lang = find['ln']
    except:
        pass

    if lang == 'en':
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'*You are missing the basic required Permission(s)*')

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'*Command is missing required Argument*')

            
        if isinstance(error, commands.MissingRole):
            await ctx.send(f'*Command is missing required Role*')
        
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send(f'*Command is missing required Role*')
            
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"**The bot is missing required permissions. Please give the bot ADMINISTRATOR Permission to work flawlessly**")

    if lang == 'fr':
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"*Vous n'avez pas la permission nécessaire*")

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"*La commande manque l'argument nécessaire*")


            
        if isinstance(error, commands.MissingRole):
            await ctx.send(f'*Command is missing required Role*')
        
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send(f'*Command is missing required Role*')
            
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"**The bot is missing required permissions. Please give the bot ADMINISTRATOR Permission to work flawlessly**")

#autorole
@client.event
async def on_member_join(member):

    try:
        server = str(member.guild.id)
        collection = db['autorole']
        find = collection.find_one({'_id': server})
        
        r = find['rol']

        role = get(member.guild.roles, name = r)
        await member.add_roles(role) 
    except:
        print("*** Error in AUTO_ROLE")

#Unmute


@client.command()
async def undeafen(ctx, Member: discord.Member):
    await Member.edit(deafen=False)
    await ctx.send(f"> {Member.mention} was undeafened successfully")

@client.command()
async def unmute(ctx, Member: discord.Member):
    
    await Member.edit(mute=False)


    try:
        guild = str(ctx.guild.id)

        collection = db['language']
        find = collection.find_one({'_id': guild})
        lang = find['ln']
        print(lang)
    except:
        lang = 'en'


    if lang == 'en':
        await ctx.send(f"> {Member.mention} was unmuted successfully!")

    if lang == 'fr':
        await ctx.send(f"> {Member.mention} a été réactivé avec succès!")

@client.command()
@commands.has_permissions(administrator = True)
async def setlang(ctx, l):

    if l == 'FR':
        l = 'fr'
    if l == 'EN':
        l = 'en'

    guild = str(ctx.guild.id)

    collection = db['language']
    post = {'_id' : guild, 'ln' : l}
    find = collection.find({'_id': guild})

    if l in ['en', 'fr']:

        key = 69

        for x in find:
            key = x['_id']

        if key == guild:
            collection.delete_one({'_id': guild})
            collection.insert_one(post)
        else:
            collection.insert_one(post)
        if l == 'en':
            await ctx.send(f'Defaulf language for this server was set to ***English (EN)***')

        if l == 'fr':
            await ctx.send(f'La langue par défaut pour ce serveur est réglée à : ***Français (FR)***')
        
    else:
        await ctx.send('No such language in the database. *Contact the support server:* https://discord.gg/xBFPrYC')


@client.command()
@commands.has_permissions(administrator = True)
async def autorole(ctx, *, r):

    guild = str(ctx.guild.id)

    collection = db['autorole']

    post = {'_id': guild, 'rol': r}


    try:
        collection.insert_one(post)
    except:
        collection.delete_one({'_id': guild})
        collection.insert_one(post)   

    lang = 'en'

    try:
        guild = str(ctx.guild.id)

        collection = db['language']
        find = collection.find_one({'_id': guild})
        lang = find['ln']
        print(lang)
    except:
        pass


    if lang == 'en':
        await ctx.send(f'Auto-role set to **{r}**. To disable autorole, just input `.autorole disable`')



    if lang == 'fr':              
        await ctx.send(f"Rôle automatique défini à **{r}**. Pour le désactiver, saisissez `.autorole disable`")


#time

@client.command(aliases = ['time'])
async def _time(ctx):
    import time
    a=int(time.time())
    await ctx.send(f'{str(a)}')



#Timer
@client.command(aliases=['timekeep', 't', 'chrono'])
async def timer(ctx, x, y='0s'):
    lang = 'en'


    try:
        guild = str(ctx.guild.id)
        collection = db['language']
        find = collection.find_one({'_id': guild})
        lang = find['ln']
        print(lang)
        print(x, y)
    except:
        pass

    if (x.endswith('m') and y.endswith('s')):
        x = x[:-1]
        y = y[:-1]

        print(x, y)
        min = int(x)
        sec = int(y)   
        time1 = min*60 + sec
        time2 = time1
        time3 = 0
        l[ctx.message.channel.id] = 0
        n = float(1)
        print('TIMEKEEP')


        if lang == 'en':
            await ctx.send(f'**Timer set for {str(int(time2/60))}m {str(time2%60)}s {ctx.message.author.mention}** *If the timer lags due to server latency, use `.r ` to set a background timer for accurate time-keeping.* ')
            msg = await ctx.send(f':clock1: **Timer: **  **` {str(int(time2/60)).zfill(2)} : {str(time2%60).zfill(2)} `**   {ctx.message.author.mention}  `.pause ` to pause')

                    
            while time2 >= 0:

                # Use replace text
                await msg.edit(content = f':clock1: **Timer: **  **` {str(int(time2/60)).zfill(2)} : {str(time2%60).zfill(2)} `**   {ctx.message.author.mention}  `.pause ` to pause')
                
                j = time2 % 5
                if j != 0:
                    time2 = time2 - j    
                    time3 = time3 + j
                    await asyncio.sleep(j-float(n)+1)
                    await msg.edit(content = f':clock1: **Timer: **  **` {str(int(time2/60)).zfill(2)} : {str(time2%60).zfill(2)} `**   {ctx.message.author.mention}  `.pause ` to pause')
                
                
                await asyncio.sleep(4+float(n))
                time2 = time2 - 5
                time3 = time3 + 5



                if time3 == 60:
                    await ctx.send(f':green_circle: **1 minute** **FINISHED** {ctx.message.author.mention}')
                            
                if time2 == 60:
                    await ctx.send(f':orange_circle: **1 minute** **LEFT** {ctx.message.author.mention}')
                        
                if time2 <= 0:
                    del l[ctx.message.channel.id]
                    await ctx.send(f":red_circle: **Time's UP!** Additional 15 seconds are given {ctx.message.author.mention}")
                    await msg.edit(content = f':clock1: **Timer: **  **` 00 : 00 `   {ctx.message.author.mention}**')
                    await asyncio.sleep(15)
                    await ctx.send(f"**Additional time is also FINISHED!** {ctx.message.author.mention}")
                    

                if (l[ctx.message.channel.id] == 1):
                    await ctx.send(f'The timer(s) **Stopped!**')
                    del l[ctx.message.channel.id]
                    print(l)
                    break
                if (l[ctx.message.channel.id] != 0):
                    while True:
                        await msg.edit(content = f':pause_button: **Paused:**  **` {str(int(time2/60)).zfill(2)} : {str(time2%60).zfill(2)} `**   {ctx.message.author.mention}  `.resume ` to resume')
                        await asyncio.sleep(float(n))
                        await msg.edit(content = f':pause_button: **Paused:**  **` {str(int(time2/60)).zfill(2)}   {str(time2%60).zfill(2)} `**   {ctx.message.author.mention}  `.resume ` to resume')
                        await asyncio.sleep(float(n))
                        if (l[ctx.message.channel.id] == 0):
                            break


            
        if lang == 'fr':        
            await ctx.send(f'**Chronomètre réglé pour {str(int(time2 / 60))}m {str(time2 % 60)}s {ctx.message.author.mention}**. *Si le chronomètre ralenti à cause de la latence serveur, utilisez `.r` pour lancer un chronomètre plus précis en arrière-plan* ')
            msg = await ctx.send(f':clock1: **Chronomètre : **  **` {str(int(time2 / 60)).zfill(2)} : {str(time2 % 60).zfill(2)} `**   {ctx.message.author.mention}  `.pause ` pour mettre sur pause')

                    
            while time2 >= 0:

                # Use replace text
                await msg.edit(content = f':clock1: **Chronomètre : **  **` {str(int(time2 / 60)).zfill(2)} : {str(time2 % 60).zfill(2)} `**   {ctx.message.author.mention}  `.pause ` pour mettre sur pause')
                
                j = time2 % 5
                if j != 0:
                    time2 = time2 - j    
                    time3 = time3 + j
                    await asyncio.sleep(j-float(n)+1)
                    await msg.edit(content = f':clock1: **Chronomètre : **  **` {str(int(time2 / 60)).zfill(2)} : {str(time2 % 60).zfill(2)} `**   {ctx.message.author.mention}  `.pause ` pour mettre sur pause')
                

                await asyncio.sleep(4+float(n))
                time2 = time2 - 5
                time3 = time3 + 5



                if time3 == 60:
                    await ctx.send(f':green_circle: **1 minute** **ÉCOULÉE** {ctx.message.author.mention}')
                            
                if time2 == 60:
                    await ctx.send(f':orange_circle: **1 minute** **RESTANTE** {ctx.message.author.mention}')
                        
                if time2 <= 0:
                    del l[ctx.message.channel.id]
                    await ctx.send(f":red_circle: **Le temps est ÉCOULÉ !** 15 secondes de grâce sont accordées {ctx.message.author.mention}")
                    await msg.edit(content = f':clock1: **Chronomètre : **  **` 00 : 00 `   {ctx.message.author.mention}**')
                    await asyncio.sleep(15)
                    await ctx.send(f"**Le temps de grâce est ÉCOULÉ !** {ctx.message.author.mention}")
                    

                if (l[ctx.message.channel.id] == 1):
                    await ctx.send(f'Le(s) chronomètre(s) sont **arrêté(s) !**')
                    del l[ctx.message.channel.id]
                    print(l)
                    break
                if (l[ctx.message.channel.id] != 0):
                    while True:
                        await msg.edit(content = f':pause_button: **En pause :**  **` {str(int(time2 / 60)).zfill(2)} : {str(time2 % 60).zfill(2)} `**   {ctx.message.author.mention}  `.resume ` pour reprendre')
                        await asyncio.sleep(1)
                        await msg.edit(content = f':pause_button: **En pause :**  **` {str(int(time2 / 60)).zfill(2)}  {str(time2 % 60).zfill(2)} `**   {ctx.message.author.mention}  `.resume ` pour reprendre')
                        await asyncio.sleep(float(n))
                        if (l[ctx.message.channel.id] == 0):
                            break

    else:
        if lang == 'en':
            await ctx.send(f'*Syntax error* \n*The command should contain the amount of Minute and the amount of Second in the following syntax* **Nm Ns**\n For example: ***7m 15s, 0m 30s***')
        if lang == 'fr':
            await ctx.send(f'*Erreur de syntaxe*\n*La commande doit contenir le nombre de minutes et de secondes selon le format suivant* **NmNs**\nPar exemple : ***7m 15s, 0m 30s***')


@timer.error
async def timer_error(ctx, error):
    lang = 'en'

    try:
        guild = str(ctx.guild.id)

        collection = db['language']
        find = collection.find_one({'_id': guild})
        lang = find['ln']
        print(lang)
    except:
        pass


    if lang == 'en':
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'If you want to set the timer lower then *1 Minute*, the command should contain the amount of Minutes and the amount of Seconds in the following syntax **Nm Ns**\n For example: ***7m 15s, 0m 30s***')

    if lang == 'fr':
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"*Si vous voulez définir le chronomètre pour moins d'*une minute*, la commande devrait contenir le nombre de minutes et de secondes selon le format suivant* **NmNs**\nPar exemple : ***7m 15s, 0m 30s***")


@client.command(aliases=['r', 'reminder', 'rappel'])
async def remindme(ctx, x, y='0s'):
    lang = 'en'

    try:
        guild = str(ctx.guild.id)

        collection = db['language']
        find = collection.find_one({'_id': guild})
        lang = find['ln']
        print(lang)
    except:
        pass


    if (x.endswith('m') and y.endswith('s')):
        x = x[:-1]
        y = y[:-1]

        print(x, y)
        min = int(x)
        sec = int(y)   
        time1 = min*60 + sec
        time2 = time1
        time3 = 0
        l[ctx.message.channel.id] = 0
        n = 1
    
        if lang == 'en':

            await ctx.send(f'**Reminder set for {str(int(time2/60))}m {str(time2%60)}s {ctx.message.author.mention}**\n*Use* `.t` *command for on-screen timer*')
            t[ctx.message.channel.id] = str(f'{str(int(time2/60)).zfill(2)} : {str(time2%60).zfill(2)}   {ctx.message.author.mention}')

                    
            while time2 >= 0: 
                # Use replace text
                t[ctx.message.channel.id] = str(f'{str(int(time2/60)).zfill(2)} : {str(time2%60).zfill(2)}   {ctx.message.author.mention}')

                await asyncio.sleep(float(n))
                time2 = time2 - 1
                time3 = time3 + 1



                if time3 == 60:
                    await ctx.send(f':green_circle: **1 minute** **FINISHED** {ctx.message.author.mention}')
                            
                if time2 == 60:
                    await ctx.send(f':orange_circle: **1 minute** **LEFT** {ctx.message.author.mention}')
                        
                if time2 == 0:
                    t[ctx.message.channel.id] = '*<Null>*'
                    await ctx.send(f":red_circle: **Time's UP!** Additional 15 seconds are given {ctx.message.author.mention}")
                    await asyncio.sleep(15)
                    await ctx.send(f"**Additional time is also FINISHED!** {ctx.message.author.mention}")
                    del l[ctx.message.channel.id]
                    

                if (l[ctx.message.channel.id] == 1):
                    await ctx.send(f'The timer(s) **Stopped!**')
                    t[ctx.message.channel.id] = '*<Null>*'
                    del l[ctx.message.channel.id]
                    print(l)
                    break
                if (l[ctx.message.channel.id] != 0):
                    msg = await ctx.send(content = f':pause_button: *REMINDER PAUSED:*  **` {str(int(time2/60)).zfill(2)} : {str(time2%60).zfill(2)} `**   {ctx.message.author.mention}  `.resume ` to resume')
                        
                    while True:
                        await msg.edit(content = f':pause_button: *REMINDER PAUSED:*  **` {str(int(time2/60)).zfill(2)} : {str(time2%60).zfill(2)} `**   {ctx.message.author.mention}  `.resume ` to resume')
                        if (l[ctx.message.channel.id] == 0):
                            await ctx.send(f':arrow_forward: *REMINDER RESUMED:*  **` {str(int(time2/60)).zfill(2)} : {str(time2%60).zfill(2)} `**   {ctx.message.author.mention}')
                            break



        if lang == 'fr':
        
            await ctx.send(f"**Rappel réglé pour {str(int(time2 / 60))}m {str(time2 % 60)}s {ctx.message.author.mention}**\n*Utilisez la commande* `.t` *pour afficher un chronomètre à l'écran*")
            t[ctx.message.channel.id] = str(f'{str(int(time2 / 60)).zfill(2)} : {str(time2 % 60).zfill(2)}   {ctx.message.author.mention}')

                    
            while time2 >= 0: 
                # Use replace text
                t[ctx.message.channel.id] = str(f'{str(int(time2 / 60)).zfill(2)} : {str(time2 % 60).zfill(2)}   {ctx.message.author.mention}')

                await asyncio.sleep(float(n))
                time2 = time2 - 1
                time3 = time3 + 1



                if time3 == 60:
                    await ctx.send(f':green_circle: **1 minute** **ÉCOULÉE** {ctx.message.author.mention}')
                            
                if time2 == 60:
                    await ctx.send(f':orange_circle: **1 minute** **RESTANTE** {ctx.message.author.mention}')
                        
                if time2 == 0:
                    t[ctx.message.channel.id] = '*<Null>*'
                    await ctx.send(f":red_circle: **Le temps est ÉCOULÉ !** 15 secondes de grâce sont accordées {ctx.message.author.mention}")
                    await asyncio.sleep(15)
                    await ctx.send(f"**Le temps de grâce est ÉCOULÉ !** {ctx.message.author.mention}")
                    del l[ctx.message.channel.id]
                    

                if (l[ctx.message.channel.id] == 1):
                    await ctx.send(f'Le(s) chronomètre(s) sont **arrêté(s) !**')
                    t[ctx.message.channel.id] = '*<Null>*'
                    del l[ctx.message.channel.id]
                    print(l)
                    break
                if (l[ctx.message.channel.id] != 0):
                    msg = await ctx.send(content = f':pause_button: *LE RAPPEL EST SUR PAUSE :* **` {str(int(time2 / 60)).zfill(2)} : {str(time2 % 60).zfill(2)} `** {ctx.message.author.mention} `.resume` pour reprendre')
                        
                    while True:
                        await msg.edit(content = f':pause_button: *LE RAPPEL EST SUR PAUSE :* **` {str(int(time2 / 60)).zfill(2)} : {str(time2 % 60).zfill(2)} `** {ctx.message.author.mention} `.resume` pour reprendre')
                        if (l[ctx.message.channel.id] == 0):
                            await ctx.send(f':arrow_forward: *LE RAPPEL A REPRIS :* **` {str(int(time2 / 60)).zfill(2)} : {str(time2 % 60).zfill(2)} `** {ctx.message.author.mention}')
                            break

    else:

        if lang == 'en':        
            await ctx.send(f'*Syntax error* \n*The command should contain the amount of Minutes and the amount of Seconds in the following syntax* **Nm Ns**\n For example: ***7m 15s, 0m 30s***')

        if lang == 'fr':
            await ctx.send(f'*Erreur de syntaxe*\n*La commande doit contenir le nombre de minutes et de secondes selon le format suivant* **Nm Ns**\nPar exemple : ***7m 15s, 0m 30s***')


@remindme.error
async def remindme_error(ctx, error):
    lang = 'en'


    try:
        guild = str(ctx.guild.id)

        collection = db['language']
        find = collection.find_one({'_id': guild})
        lang = find['ln']
        print(lang)
    except:
        pass


    if lang == 'en':
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'*If you want to set the timer lower then *1 Minute*, the command should contain the amount of Minute and the amount of Second in the following syntax* **Nm Ns**\n For example: ***7m 15s, 0m 30s***')

    if lang == 'fr':
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"*Si vous voulez définir le chronomètre pour moins d'*une minute*, la commande devrait contenir le nombre de minutes et de secondes selon le format suivant* **NmNs**\nPar exemple : ***7m 15s, 0m 30s***")


@client.command(aliases=['showtimer'])
async def showtimers(ctx):
    lang = 'en'
    try:
        guild = str(ctx.guild.id)
        print(guild)

        collection = db['language']
        find = collection.find_one({'_id': guild})
        lang = find['ln']
    except:
        pass

    print(lang)
    print ('poo')
    if lang == 'en':
        await ctx.send(f'*Timer running in this channel :* **{t.get(ctx.message.channel.id, "<null>")}**')

    if lang == 'fr':
        await ctx.send(f'*Chronomètre en cours sur cette chaîne :* **{t.get(ctx.message.channel.id, "Aucun")}**')

    print('IF SKIPPED!')

@client.command(aliases=['cleartimers'])
async def stop(ctx):
    l[ctx.message.channel.id] = 1
    print(l)

@client.command()
async def pause(ctx):
    l[ctx.message.channel.id] = 2
    print(l)

@client.command()
async def resume(ctx):
    l[ctx.message.channel.id] = 0
    print(l)

#Timer Ends :)



#8ball
@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question):
    lang = 'en'

    try:
        guild = str(ctx.guild.id)

        collection = db['language']
        find = collection.find_one({'_id': guild})
        lang = find['ln']
        print(lang)
    except:
        pass


    if lang == 'en':
        responses = ['Of course!',
                    'Yes, obviously!',
                    'Most likely',
                    'It must happen',
                    'Why not?' 
                    'Hear! Hear!',
                    'Maybe?',
                    "Better you don't find out",
                    'No prediction',
                    "Don't count on it",
                    'Very doubtable',
                    'Not so good']
        await ctx.send(f'*Question from  {ctx.message.author.mention} :* {question}\n    *Answer :* {random.choice(responses)}')


    if lang == 'fr':
        responses = ["Bien sûr!",
                    "Oui, évidemment!",
                    "Très probablement",
                    "Tu peux compter là-dessus",
                    "Pourquoi pas ?",
                    "Hear ! Hear !",
                    "Peut-être ?",
                    "Il vaut mieux ne pas le savoir",
                    "Aucune prévision",
                    "N'y compte pas",
                    'Peu probable',
                    'Passable']
        await ctx.send(f'*Question par {ctx.message.author.mention} :* {question}\n    *Réponse :* {random.choice(responses)}')


#greetings
@client.command(aliases=['hello', 'hi', 'hola', 'hey','Bonjour','Salut','Aloha','Hey'])
async def greetings(ctx):
    lang = 'en'

    try:
        guild = str(ctx.guild.id)

        collection = db['language']
        find = collection.find_one({'_id': guild})
        lang = find['ln']
        print(lang)
    except:
        pass


    if lang == 'en':
        greetings = ['Hey there,', 'Hello,', "What's up? "]
        await ctx.send(f'{random.choice(greetings)} {ctx.message.author.mention}')

    if lang == 'fr':
        greetings = ['Bonjour','Salut','Aloha','Hey','Salut toi','Bonjour','Quoi de neuf ?']
        await ctx.send(f'{random.choice(greetings)} {ctx.message.author.mention}')



#cointoss
@client.command()
async def coinflip(ctx):
    lang = 'en'

    try:
        guild = str(ctx.guild.id)

        collection = db['language']
        find = collection.find_one({'_id': guild})
        lang = find['ln']
        print(lang)
    except:
        pass


    if lang == 'en':
        coin = ['Head', 'Tail']
        await ctx.send(f'The coin shows **{random.choice(coin)}!**')

    if lang == 'fr':
        coin = ['Face', 'Pile']
        await ctx.send(f'La pièce montre **{random.choice(coin)}!**')


#ping
@client.command()
async def ping(ctx):
    await ctx.send(f'Ping: ***{round(client.latency*1000)}*** ms')



#clear
@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount=0,):
    lang = 'en'

    try:
        guild = str(ctx.guild.id)

        collection = db['language']
        find = collection.find_one({'_id': guild})
        lang = find['ln']
        print(lang)
    except:
        pass


    if lang == 'en':
        if amount != 0:
            amount = amount + 1
        await ctx.channel.purge(limit=amount)
        if amount == 0:
            post = '*None of the messages were cleared. Pass a value!*'
        else:
            post = f'Last **{amount - 1}** message(s) till now were cleared by {ctx.message.author.mention}'

        await ctx.send(post)

    if lang == 'fr':
        if amount != 0:
            amount = amount + 1
        await ctx.channel.purge(limit=amount)
        if amount == 0:
            post = "*Aucun messages n'a été effacé. Saisissez une valeur !*"
        else:
            post = f'Les **{amount - 1}** message(s) précédents ont été effacés par {ctx.message.author.mention}'

        await ctx.send(post)


#Team Shuffle
@client.command(aliases=['toss'])
async def matchup(ctx, mod):
    lang = 'en'

    try:
        guild = str(ctx.guild.id)

        collection = db['language']
        find = collection.find_one({'_id': guild})
        lang = find['ln']
        print(lang)
    except:
        pass


    if lang == 'en':
        if(mod=='BP' or mod=='bp'):
            a = ['Team 1' , 'Team 2' , 'Team 3' , 'Team 4' ]
            random.shuffle(a) #shuffle method
            await ctx.send("OG: " + a[0] + "\nOO: " + a[1] + "\nCG: " + a[2] + "\nCO: " + a[3])
        if(mod=='AP' or mod=='ap' or mod=='3v3'):
            b = ['Team 1' , 'Team 2' ]
            random.shuffle(b) #shuffle method
            await ctx.send("GOV: " + b[0] + "\nOPP: " + b[1])

    if lang == 'fr':
        if(mod=='BP' or mod=='bp' or mod=='PB' or mod=='pb'):
            a = ['Équipe 1' , 'Équipe 2' , 'Équipe 3' , 'Équipe 4' ]
            random.shuffle(a) #shuffle method
            await ctx.send("GO: " + a[0] + "\nOO: " + a[1] + "\nGF: " + a[2] + "\nOF: " + a[3])
        if(mod=='AP' or mod=='ap' or mod=='PA' or mod=='pa' or mod=='3v3'):
            b = ['Équipe 1' , 'Équipe 2' ]
            random.shuffle(b) #shuffle method
            await ctx.send("GOV: " + b[0] + "\nOPP: " + b[1])



#Get Motion
@client.command()
async def getmotion(ctx, lng='english'):
    lang = 'en'
    guild = ctx.guild.id

    try:
        collection = db['language']
        find = collection.find_one({'_id': guild})
        lang = find['ln']
        print(lang)
    except:
        pass

    if lang == 'en':
        if(lng == 'english'):
            with open("english.txt") as f:
                lines = f.readlines()
                await ctx.send(f'**Motion: **{random.choice(lines)}')

        elif(lng == 'bangla'):
            with open("bangla.txt") as f:
                lines = f.readlines()
    
                await ctx.send(f'**Motion: **{random.choice(lines)}')

    if lang == 'fr':
        if(lng == 'english' or lng == 'anglais'):
            with open("english.txt") as f:
                lines = f.readlines()
                await ctx.send(f'**Motion: **{random.choice(lines)}')

        elif(lng == 'bangla'):
            with open("bangla.txt") as f:
                lines = f.readlines()
    
                await ctx.send(f'**Motion: **{random.choice(lines)}')


#Add Motion
@client.command()
async def addmotion(ctx, *, motion):
    lang = 'en'

    try:
        guild = str(ctx.guild.id)

        collection = db['language']
        find = collection.find_one({'_id': guild})
        lang = find['ln']
        print(lang)
    except:
        pass
    

    server = ctx.guild


    if lang == 'en':
        print('poo')
        channel = client.get_channel(708094525993910343)

        try:
            collection = db['addmotion']
            post = {'_id': motion}
            collection.insert_one(post)

            await channel.send(f'**Motion from {ctx.message.author.mention}, {server}, ID: {ctx.guild.id} : **{motion}')
            await ctx.send(r'**Motion added for review!** *Join here to see the log:* https://discord.gg/VAcjYEN')
        except:
            await ctx.send('The motion already exists in the database!')

    if lang == 'fr':
        channel = client.get_channel(708094525993910343)

        try:
            collection = db['addmotion']
            post = {'_id': motion}
            collection.insert_one(post)

            await channel.send(f'**Motion from {ctx.message.author.mention}, {server} : **{motion}')
            await ctx.send(r'**Motion ajoutée pour révision !** *Joignez ici pour voir le flux :* https://discord.gg/VAcjYEN')
        except:
            ctx.send('La motion existe déjà dans la base de données!')

#REACT-ROLE-MENU

#Add role

@client.event
async def on_raw_reaction_add(payload):

#    _reaction = payload.emoji.name
#
#   if _reaction not in ['🇦', '🇸', '🇩']:
#       print('Wrong Reaction')                                   
#       payload.remove_reaction("_reaction"
    
    collection = db['rolemenu']
    guild = int(payload.guild_id)

    fax = collection.find({'_id': guild})
    
    
    
    for keys in fax:
        key = keys['msgID']
        
    print(key)

    
    if payload.message_id == key:
        print("Hello")
        guild = discord.utils.find(lambda g : g.id == payload.guild_id, client.guilds)
        print(guild)

        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        print(member)

        adj = discord.utils.get(guild.roles, name = 'Adjudicator')
        deb = discord.utils.get(guild.roles, name = 'Debater')
        spec = discord.utils.get(guild.roles, name = 'Spectator')

        if payload.emoji.name == '🇦':
            print(payload.emoji)
            role = adj
            await member.remove_roles(deb, spec)
            print(role)
        elif payload.emoji.name == '🇩':
            print(payload.emoji)
            role = deb
            await member.remove_roles(adj, spec)
            print(role)
        elif payload.emoji.name == '🇸':
            print(payload.emoji)
            role = spec
            await member.remove_roles(deb, adj)
            print(role)        
       
        if payload.user_id != 706179030977740810:
            
            await member.add_roles(role)
            print(payload.user_id)


#removerole

@client.event
async def on_raw_reaction_remove(payload):

    collection = db['rolemenu']
    guild = int(payload.guild_id)

    fax = collection.find({'_id': guild})
    
    for keys in fax:
        key = keys['msgID']
    if key == payload.message_id:
        print("Hello")
        guild = discord.utils.find(lambda g : g.id == payload.guild_id, client.guilds)
        print(guild)
        
        if payload.emoji.name == '🇦':
            print(payload.emoji)
            role = discord.utils.get(guild.roles, name = 'Adjudicator')
            print(role)
        elif payload.emoji.name == '🇩':
            print(payload.emoji)
            role = discord.utils.get(guild.roles, name = 'Debater')
            print(role)
        elif payload.emoji.name == '🇸':
            print(payload.emoji)
            role = discord.utils.get(guild.roles, name = 'Spectator')
            print(role)        
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        print(member)
        await member.remove_roles(role)
        


@client.command(name="announce", help="Requires MANAGE MESSAGES PERMISSION.Format is %announce \"text here in quotes\". Sends text to all debate channels")
@commands.has_permissions(manage_messages = True)
async def announce(ctx, text: str):
    debate_tcs = [channel for channel in ctx.guild.text_channels]
    await asyncio.wait([channel.send(text) for channel in debate_tcs])
    await ctx.send(f"Announcement was sent successfully! {ctx.message.author.mention}")




#create rolemenu


@client.command()
@commands.has_permissions(administrator = True)
async def addrolemenu(ctx):
    lang = 'en'

    try:
        guild = str(ctx.guild.id)

        collection = db['language']
        find = collection.find_one({'_id': guild})
        lang = find['ln']
        print(lang)
    except:
        pass
    
    role = get(ctx.guild.roles, name = 'Debater')
    if role == None:
        await ctx.guild.create_role(name = 'Debater', color = discord.Colour(0xe6b60d))
        
    role = get(ctx.guild.roles, name = 'Adjudicator')
    if role == None:
        await ctx.guild.create_role(name = 'Adjudicator', color = discord.Colour(0x22a777))
        
    role = get(ctx.guild.roles, name = 'Spectator')
    if role == None:
        await ctx.guild.create_role(name = 'Spectator', color = discord.Colour(0xffffff))



    if lang == 'en':
        await ctx.channel.purge(limit=1)
        menu = await ctx.send('Please read the instructions carefully and get yourself a role. \n\nIf you are an **Adjudicator**, please react with :regional_indicator_a:\nIf you are a **Debater**, please react with :regional_indicator_d: \nIf you are a **Spectator**, please react with :regional_indicator_s: \n\nThe reactions are shown below this text. Just tap to get your role.')
        
        collection = db['rolemenu']
        guild = int(ctx.guild.id)
        msg = int(menu.id)

        post = {'_id': guild, 'msgID': msg}  

        fax = collection.find({'_id': guild})
        print(fax)
        
        ld = 1

        for mix in fax:
            ld = mix['_id']
            print(f'Hey {ld}')

        if ld == guild:
            collection.delete_one({'_id': guild})
            collection.insert_one(post)
        else:
            collection.insert_one(post)
        
        
        await menu.add_reaction("🇦")
        await menu.add_reaction("🇩")
        await menu.add_reaction("🇸")
        await ctx.send('Role-menu created successfully! *Please delete other messages from the channel to keep it clean. We request you to disable **Send Message** permission to this channel for @everyone*')

    if lang == 'fr':
        await ctx.channel.purge(limit=1)
        menu = await ctx.send("Veuillez lire les instructions attentivement et prenez un rôle.\n\nSi vous êtes **Juge**, veuillez réagir avec :regional_indicator_a:\nSi vous êtes **Débatteur**, veuillez réagir avec :regional_indicator_d:\nSi vous êtes **Spectateur**, veuillez réagir avec :regional_indicator_s:\n\nLes réactions sont affichées sous cette texte. Sélectionnez pour recevoir votre rôle.")
        
        collection = db['rolemenu']
        guild = int(ctx.guild.id)
        msg = int(menu.id)

        post = {'_id': guild, 'msgID': msg}  

        fax = collection.find({'_id': guild})
        print(fax)
        
        ld = 1

        for mix in fax:
            ld = mix['_id']
            print(f'Hey {ld}')

        if ld == guild:
            collection.delete_one({'_id': guild})
            collection.insert_one(post)
        else:
            collection.insert_one(post)
        
        
        await menu.add_reaction("🇦")
        await menu.add_reaction("🇩")
        await menu.add_reaction("🇸")
        await ctx.send("Menu des rôles créé avec succès ! *Veuillez supprimer les autres messages de la chaîne pour la garder propre. Nous recommandons de désactiver la permission **Envoyer Message** pour @everyone*")



#Role Menu Ends

#addhearhear
@client.command(aliases=['callhearhear'])
async def addhearhear(ctx):
    lang = 'en'

    try:
        guild = str(ctx.guild.id)

        collection = db['language']
        find = collection.find_one({'_id': guild})
        lang = find['ln']
        print(lang)
    except:
        pass


    if lang == 'en':
        await ctx.send(f"Add Hear! Hear! to your server with the link below. **Don't forget to VOTE:**\n https://top.gg/bot/706179030977740810")

    if lang == 'fr':
        await ctx.send(f"Ajoutez Hear! Hear! à votre serveur à l'aide du lien ci-dessous. **N'oubliez pas de voter pour nous :**\n https://top.gg/bot/706179030977740810")


#about
@client.command()
async def about(ctx):

    lang = 'en'

    try:
        guild = str(ctx.guild.id)

        collection = db['language']
        find = collection.find_one({'_id': guild})
        lang = find['ln']
    except:
        pass

    if lang == 'en':
        await ctx.send('```This is a productivity bot dedicated to debaters. This bot can time your debates with on-screen timer and give you reminders. It can give you motions to practice debating on discord, help you match-up in 3v3 and BP debates, help you decide things, flip a coin and many more. Use .commands to see them all.\n'
                        f'This bot is created by the debaters, for the debaters. Happy debating!\n\n'

                        f'Developed by       : Tasdid Tahsin [tasdidtahsin#7276]\n'
                        f'Avatar             : Sharaf Ahmed [Sharaf#0596]\n'
                        f'French Translation : Victor Babin [Victor Babin#6142], Étienne Beaulé [Étienne#7236], Thierry Jean, Nuzaba Tasannum [nuzaba.tasannum#2838]\n'
                        f'Credits            : Najib Hayder [Najib#7917], Azmaeen Md Nibras [Nibras#4972]\n'
                        f'Community Support  : Bangla Online Debate Platform\n\nSpecial thanks to the community for adding these wonderful motions.\n'
                    
                        f'</> Coded in Python3 using Discord.py & pymongo library```\n'
                        f'Join the support server and vote for the bot here: https://top.gg/bot/706179030977740810')



    if lang == 'fr':
        await ctx.send("```Ceci est un bot utilitaire dédié aux débatteurs. Ce bot permet de chronométrer vos débats à l'aide d'un affichage de chronomètre et d'alertes. Il peut également fournir des motions de pratiques, aider à l'organisation de joutes 3 v. 3 ou de style parlementaire britannique, aider à prendre des décisions à l'aide d'un outil de pile ou face et bien plus encore. Utilisez .commands pour voir toutes les fonctionnalités.\n"
                        f"Ce bot est créé par les débatteurs pour les débatteurs. Bon débat !\n\n"
                        f'Développé par         : Tasdid Tahsin [tasdidtahsin#7276]\n'
                        f'Avatar                : Sharaf Ahmed [Sharaf#0596]\n'
                        f'Traduction française  : Victor Babin [Victor Babin#6142], Étienne Beaulé [Étienne#7236], Thierry Jean, Nuzaba Tasannum [nuzaba.tasannum#2838]\n'
                        f'Crédits               : Najib Hayder [Najib#7917], Azmaeen Md Nibras [Nibras#4972]\n'
                        f'Support communautaire : Bangla Online Debate Platform\n\nMerci à la communauté pour avoir ajouté ces motions fabuleux.\n'
                    
                        f'</> Programmé en Python3 en utilisant les bibliothèques Discord.py & pymongo```\n'
                        f'Rejoignez le serveur de support ici : https://top.gg/bot/706179030977740810')





#commands
@client.command(aliases = ['commands', 'HELP'])
async def help(ctx):
    lang = 'en'

    try:
        guild = str(ctx.guild.id)

        collection = db['language']
        find = collection.find_one({'_id': guild})
        lang = find['ln']
        print(lang)
    except:
        pass


    if lang == 'en':
        await ctx.send(f">   **Hear! Hear! bot all commands:**\n\n"

                        f" ** Debate **"

                        f"```~ addmotion   : add a motion in the database\n"
                        f"~ getmotion   : .getmotion english | .getmotion  bangla\n" 
                        f"~ matchup     : .matchup AP | .toss BP ~ Get matchup```\n"

                        f" ** Time Keeping **"

                        f"```~ timer       : .t | .timer ~ set a on-screen timer\n"
                        f"~ remindme    : .r | .remindme ~ set a reminder\n"
                        f"~ showtimers  : show the running background timer\n"
                        f"~ pause       : pause the timer(s)\n"
                        f"~ resume      : resume the timer(s)\n"
                        f"~ stop        : stop the timer(s)```\n"

                        f" ** Utility **"
                                               
                        f"```~ setlang     : EN | FR ~ .setlang en ~ .setlang fr\n"
                        f"~ coinflip    : .coinflip ~ HEAD or TAIL\n"
                        f"~ ping        : see bot latency\n"
                        f'~ announce    : .announce "ANNOUNCEMENT IN THE QUOTES" ~ Announces a message to all the text channel. Requires MANAGE MESSAGES PERMISSION\n\n'
                        f"~ time        : show unix time```\n"
                        
                        f" ** Moderation **"

                        f"```~ clear       : delete the given amount of messages\n" 
                        f"~ unmute      : .unmute @mention\n"
                        f"~ undeafen    : .undeafen @mention```\n"
                                                
                        f" ** Role Management **"  

                        f"```~ autorole    : .autorole rolename ~ requires administration permission\n"                        
                        f"~ addrolemenu : Add a Get-Role Menu to the channel ~ 'Hear! Hear!' Role must be above 'Debater', 'Adjudicator', 'Spectator' roles.``` \n"                        
                        
                        f" ** Fun **"

                        f"```~ greetings   : .hello | .hi | .hola\n"
                        f"~ 8ball       : ask a question and see your luck```\n"

                        f" ** Everything Else **"
                    
                        f"```~ commands    : shows this menu\n"
                        f"~ addhearhear : get a link to add the bot to your server\n"
                        f"~ about       : learn more and meet the team```\n"
                        
                        
                        f"> ***Please use a dot  `.`  before the commands***")


    if lang == 'fr':
        await ctx.send(f"```Toutes les commandes de Hear! Hear! :\n \n"

                        f"~ 8ball       : poser une question et découvrir son avenir!\n"
                        f"~ addmotion   : ajouter une motion à la base de données\n"
                        f"~ clear       : supprimer le nombre de messages spécifié\n"
                        f"~ getmotion   : .getmotion english | .getmotion bangla\n"
                        f"~ greetings   : .hello | .hi | .hola\n"
                        f"~ commands    : afficher ce menu\n"
                        f"~ matchup     : .matchup AP | .toss BP ~ Get matchup\n"
                        f"~ ping        : afficher la latence du bot\n"
                        f"~ timer       : .t | .timer ~ régler un chrono à l'écran\n"
                        f"~ remindme    : .r | .remindme ~ régler un rappel\n"
                        f"~ showtimers  : afficher les chronomètres d'arrière-plan en cours" 
                        f"~ pause       :mettre le(s) chrono(s) sur pause\n"
                        f"~ resume      : reprendre le chrono(s)\n"
                        f"~ stop        : arrêter le(s) chrono(s)\n"
                        f"~ time        : afficher le temps UNIX\n"
                        f"~ coinflip    : .coinflip ~ PILE ou FACE\n"
                        f"~ addhearhear : recevoir un lien pour ajouter le bot à votre serveur\n"
                        f"~ about       : apprenez en davantage et rencontrez l'équipe\n"
                        f"~ addrolemenu : Ajouter un menu de rôle à la chaîne ~ les rôles 'Debater', 'Adjudicator' et 'Spectator' doivent être créés en premier, avec 'Hear! Hear!' qui les supplante.\n"
                        f"~ unmute      : .unmute @mention\n"
                        f"~ setlang     : EN | FR ~ .setlang fr ~ .setlang en\n\n"
                        f"Veuillez insérez un point (.) avant les commandes```")



client.run(token)
