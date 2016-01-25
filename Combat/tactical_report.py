#!/usr/bin/python2.7

import attack

target = "war1473"
target_char = attack.characters[target]
attacker = "septeract"
attacker_char = attack.characters[attacker]

prev_dmg = -1000000
best_weapon = "ERROR"
best_armor = "ERROR"

for weapon in attack.weapons:
    attacker_char["weapon"] = weapon
    
    for armor in attack.materials:
        attacker_char["armor"] = armor

        dmg = 0
        for i in xrange(100):
            dmg += attack.attack(attacker, target)
        dmg /= 100

        bad_dmg = 0
        for i in xrange(100):
            bad_dmg += attack.attack(target, attacker)
        bad_dmg /= 100

        #print weapon, armor, dmg, bad_dmg

        dmg -= bad_dmg

        #print weapon, armor, dmg

        if dmg > prev_dmg:
            prev_dmg = dmg
            best_weapon = weapon
            best_armor = armor

if best_weapon == "ERROR":
    print target, "is undefeatable"
elif prev_dmg < 0:
    print "Best weapon choice vs", target, "is", best_weapon, "with", best_armor, "armor, though", target, "averages higher damage"
else:
    print "Best weapon choice vs", target, "is", best_weapon, "with", best_armor, "armor"
