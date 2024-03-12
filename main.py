import sys
from javascript import require, On

mineflayer = require("mineflayer")
pathfinder = require('mineflayer-pathfinder')
pvp = require('mineflayer-pvp').plugin

if len(sys.argv) > 3:
    host = sys.argv[1]
    port = sys.argv[2]
    username = sys.argv[3]
else:
    host = 'cinrg.aternos.me'
    port = '60465'
    username = 'can_pooper'

bot = mineflayer.createBot({
    "host": host,
    "port": port,
    "username": username,
})

mcData = require('minecraft-data')(bot.version)

bot.loadPlugin(pathfinder.pathfinder)
bot.loadPlugin(pvp)

attacking = False
ignored_usernames = []

@On(bot, 'chat')
def handle_chat(this, username, message, *args):
    global attacking
    
    if username == bot.username:
        return

    cmd, *cmdargs = message.split()
    if cmd == '.quit':
        bot.quit()
        sys.exit()
    
    elif cmd == '.where':
        pos = bot.entity.position
        bot.chat(f"{pos.toString()}")
    
    elif cmd == '.come':
        movements = pathfinder.Movements(bot, mcData)
        player = bot.players[username]
        target = player.entity
        pos = target.position

        bot.pathfinder.setMovements(movements)
        bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, 1))
    
    elif cmd == '.attack':
        attacking = not attacking
        bot.chat(f'now {"attacking muahaha" if attacking else "no longer attacking"}')

    elif cmd == '.hp':
        bot.chat(f'On {bot.health} hp')
    
    elif cmd == '.ignore':
        if len(cmdargs) > 0:
            ignore_name = cmdargs[0]
            if ignore_name in ignored_usernames:
                ignored_usernames.remove(ignore_name)
                bot.chat(f'now no longer ignoring {ignore_name}')
            else:
                ignored_usernames.append(ignore_name)
                bot.chat(f'now ignoring {ignore_name}')

@On(bot, 'physicsTick')
def handle_physics_tick(this):
    global ignored_usernames
    global attacking
    
    # filter seems to be broken
    filter = lambda a: (a.type == 'mob' 
                        and a.position.distanceTo(bot.entity.position) <= 32 
                        and a.displayName != 'Armor Stand' 
                        and a.username not in ignored_usernames)
    
    entity = bot.nearestEntity(filter)
    if entity and attacking:
        print(repr(entity.username), ignored_usernames)
        bot.pvp.attack(entity)