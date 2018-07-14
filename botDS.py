
# id : https://discordapp.com/oauth2/authorize?client_id=465241470182621214&scope=bot&permissions=0
import discord
from discord.ext import commands
import os
import pickle
import random
import aiohttp
from aiohttp import web
import asyncio


TOKEN = 'NDY1MjQxNDcwMTgyNjIxMjE0.DiKpcw.U2WHrB_RYEFKc4X0FSxKDWniDOo'


grid = ['-']*9
listeplayer = []
liste_classe = [
    'eca',
    'eni',
    'iop',
    'cra',
    'feca',
    'sacri',
    'sadi',
    'osa',
    'enu',
    'sram',
    'xel',
    'panda',
    'roub',
    'zobal',
    'elio',
    'steam',
    'ougi',
    'hupper',
]

listeA = []
listeB = []
listeBan = []
def rules():
    print ("Bienvenue dans ce jeu de morpion")
    print ("Pour jouer un coup donner la case a jouer ! (0 en haut a gauche, 2 en haut a droite, 8 en bas a droite)")

def morpion():
    rules()
    return 0

def classement(l, personne):
    n = 0
    for i in range(0, len(l)):
        e = l[i]
        joueur = e[0]
        score = e[1]
        if joueur == personne:
            score = score + 1
            e[1] = score
            n = 1
            break
    if n == 0:
        l.append([personne, 1])
    classer = sorted(l, key=lambda v: v[1], reverse=True)
    return classer


def display(grid):
    for i in range(0,3):
        print("     "+str(grid[3*i]) + "|" + str(grid[3*i+1]) + "|" + str(grid[3*i+2]))
    return

def gagne(grid,player):
    for i in range(0,3):
        if (grid[3*i] == grid[3*i+1] == grid[3*i+2] == player):
            return 1
    for i in range(0,3):
            if (grid[i] == grid[i+3] == grid[i+6]== player):
                return 1
    if (grid[2] == grid[4] == grid[6]== player):
        return 1
    if (grid[0] == grid[4] == grid[8]== player):
        return 1
    else:
        return 0

def play(player, i, grid):
    if (grid[i] != "-"):
        print("case invalide veuillez rejouer")
    else:
        grid[i] = player
    if gagne(grid,player) == 1:
        print ("Le joueur %s a gagne ! felicitation", player)
    display(grid)
    return grid

def clean(grid):
    for i in range(0,9):
        grid[i] = '-'
    return 0



description = '''Bot Python'''
bot = commands.Bot(command_prefix='!', description='on code pas un bot de merde nouuuuus')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def bibi():
    embed = discord.Embed(title="Botons en touche", description="Listes des commandes:", color=0xeee657)
    embed.add_field(name="!mp 'P' I", value="Permet de jouer à un jeu de morpion. Le joueur courant 'X' ou '0' doit passer dans l'argument **P** et la case sur laquelle jouer est **I**.\nLes cases vont de 1 à 9, à lire de gauche à droite et de haut en bas", inline=False)
    embed.add_field(name="!NTM", value = "permet d\'insulter un membre aléatoire du discord et de le mentionner directement, parfait pour vous calmer apres un petit koli vs 3piliers espagnol JAJAJAJA", inline=False)
    await bot.say(embed=embed)


@bot.command()
async def cleanmp():
    clean(grid)
    await bot.say("Le jeu de morpion a été réinitialisé vous pouvez jouer !")

@bot.command(pass_context = True)
async def mp(context, player: str , pos):
    auth = str(context.message.author).split('#')[0]
    try:
        pos = int(pos)
    except:
        await bot.say("Tu te prends pour qui la ? de 1 à 9 les cases, on dirait kyky ca sait pas compter.....")
        return 0
    c = 0
    pos2 = pos - 1
    if player != 'X' and player != 'O':
       await bot.say("T'es con comme sledax toi croix ou round rien d'autre fdp :fencer:")
       return 0
    if pos2 < 0 or pos2 > 9 or grid[pos2] != '-' :
        await bot.say("Mauvaise case espèce de débile")

    else:
        play(player, pos2, grid)
        for i in range(0,9):
            if grid[i] != '-':
                c += 1
        for i in range(0,3):
            await bot.say(str(grid[3*i]) + "  |  " + str(grid[3*i+1]) + "  |  " + str(grid[3*i+2]))
        if c == 9 and gagne(grid,player) == 0:
            await bot.say("Match nul wola NUL NUL NUL")
            clean(grid)
        if gagne(grid,player) == 1:
            await bot.say("Le joueur {} a gagné, mes félicitations {} !".format(player,auth))
            fd = open("classement.txt", "w")
            l = classement(listeplayer, auth)
            # with open('classement.txt', 'wb') as fichier:
            #     mon_pickler = pickle.Pickler(fichier)
            #     mon_pickler.dump(l)
            await bot.say(" :dab: :dab: :dab: :dab: ")
            clean(grid)
            fd.close()

@bot.command()
async def rankingmp():
    fd = open("classement.txt", "w")
    if len(listeplayer) == 0:
        await bot.say("Aucun joueur n'est actuellement classé")
    for i in range(0, len(listeplayer)):
        p = listeplayer[i]
        await bot.say("{}. {} -> {} points\n".format(i+1, p[0],p[1]))
        fd.write("{}. {} -> {} points\n".format(i+1, p[0],p[1]))
    fd.close()


#Insulte aléatoire un membre du discord
@bot.command(pass_context = True)
async def swear(context):
    mem = 0 #nombre de membre dans le serveur du bot
    nb = 0 #nombre de ligne du fichier d'insulte
    c = 0 #compteur pour le fichier insulte
    d = 0 #compteur pour prendre un membre random
    if context.message.author == "Sledax#8137" or context.message.author== "ulkile#9617":
        await bot.say("Ptdrrr " + context.message.author.mention + " tu te prends pour qui à vouloir insulter des gens ? t'es la pute de tout le monde")
    #On compte le nombre de ligne dans le fichier pour choisir une ligne aléatoire
    fich = open("insulte.txt")
    for line in fich:
        nb += 1
    n = random.randint(1,nb+1)
    fich.close()

    #On compte le nombre de membres dans le serveur puis on en prend un au hasard
    for server in bot.servers:
        members = server.members
        for m in members:
            mem += 1
        n2 = random.randint(1,mem+1)
        print(n2)
        for m in members:
            d += 1
            if d == n2:
                target = m
                print (target)

    fich = open("insulte.txt")
    for line in fich:
        c += 1
        if c == n:
            line2 = line.split("• ")[1]
    line3 = line2.split("\n")[0]
    line4 = list(line3)
    print(line4)
    print(line4[len(line4)-1 ])
    if line4[len(line4)-1 ] == 'e':
        await bot.say(target.mention + " tu es une " + line2.lower())
    else:
        await bot.say(target.mention + " tu es un " + line2.lower())
    fich.close()

@bot.command()
async def clearD():
    liste_classe = [
        'eca',
        'eni',
        'iop',
        'cra',
        'feca',
        'sacri',
        'sadi',
        'osa',
        'enu',
        'sram',
        'xel',
        'panda',
        'roub',
        'zobal',
        'elio',
        'steam',
        'ougi',
        'hupper',
    ]
    listeA = []
    listeB = []
    listeBan = []

@bot.command(pass_context = True)
async def draft(contexte, side, choix, classe):

    if choix == 'p' and side == 'A':
        listeA.append(classe)
    if choix == 'p' and side == 'B':
        listeB.append(classe)
    elif choix == 'b':
        listeBan.append(classe)
    liste_classe.remove(classe)

    msgPick = "-".join(listeA) + " vs " + "-".join(listeB) + "\n"
    msgBan = "-".join(listeBan) + "\n"
    msgRest = " ".join(liste_classe)
    # await bot.say(msg)
    embed = discord.Embed(title="DRAFT", color=0xeee657)
    embed.add_field(name="Pick", value = msgPick, inline=False)
    embed.add_field(name="Ban", value = msgBan ,inline=False)
    embed.add_field(name="Classes restantes : ", value = msgRest ,inline=False)
    await bot.say(embed=embed)

# @bot.event
# async def on_message(message):
#     if message.content.startswith('t\'es con ?'):
#         await bot.send_message(message.channel, 't\'es con ?')
#         msg = await bot.wait_for_message(content='t\'es con ?')
#         await bot.send_message(message.channel, 't\'es con ?')

bot.run(TOKEN)
