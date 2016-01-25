import leviathans_planets as lp
import leviathans_world as game

import random
import copy

lp.blueprints["Clone contract"] = "Cadaver"

@game.loop_hook
def check_clones(world, playerid):
    player = world.players[playerid]
    if "Clone contract" in player.cargo:
        player.cargo.remove("Clone contract")
        world.players.insert(playerid + 1,\
            game.make_playership(world, world.market,\
                                 ["" for i in xrange(random.randrange(100, 200))] ))

        clone = world.players[playerid + 1]
        clone.systemID = player.systemID
        clone.crew[0] = clone.captain = copy.copy(player.captain)

        for x in clone.layer.map:
            for y in x:
                if y.func == "Bridge":
                    y.crew[0] = clone.captain

        lp.update_cargo(world, playerid)
