import sys
from javascript import require, On, Once, console

mineflayer = require("mineflayer", "latest")
pathfinder = require('mineflayer-pathfinder')

"""
// This is an example that uses mineflayer-pathfinder to showcase how simple it is to walk to goals

const mineflayer = require('mineflayer')
const { pathfinder, Movements, goals: { GoalNear } } = require('mineflayer-pathfinder')

if (process.argv.length < 4 || process.argv.length > 6) {
  console.log('Usage : node gps.js <host> <port> [<name>] [<password>]')
  process.exit(1)
}

const bot = mineflayer.createBot({
  host: process.argv[2],
  port: parseInt(process.argv[3]),
  username: process.argv[4] ? process.argv[4] : 'gps',
  password: process.argv[5]
})

const RANGE_GOAL = 1 // get within this radius of the player

bot.loadPlugin(pathfinder)

bot.once('spawn', () => {
  const defaultMove = new Movements(bot)

  bot.on('chat', (username, message) => {
    if (username === bot.username) return
    if (message !== 'come') return
    const target = bot.players[username]?.entity
    if (!target) {
      bot.chat("I don't see you !")
      return
    }
    const { x: playerX, y: playerY, z: playerZ } = target.position

    bot.pathfinder.setMovements(defaultMove)
    bot.pathfinder.setGoal(new GoalNear(playerX, playerY, playerZ, RANGE_GOAL))
  })
})
"""


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

@On(bot, "chat")
def handle_chat(this, username, message, *args):
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
