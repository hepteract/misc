#!/usr/bin/python2.7

import attack

weapons = {}

for armor in attack.materials:
    prev_dmg = 0
    prev_bad_dmg = 1000000
    best_weapon = ""
    worst_weapon = ""

    for weapon in attack.weapons:
        weapons[weapon] = 0

        for i in xrange(1000):
            weapons[weapon] += attack._attack(weapon, armor, False )
        weapons[weapon] /= 1000

        if weapons[weapon] > prev_dmg:
            best_weapon = weapon
            prev_dmg = weapons[weapon]

        if weapons[weapon] < prev_bad_dmg:
            worst_weapon = weapon
            prev_bad_dmg = weapons[weapon]

    print "Best weapon versus", armor, "armor is", best_weapon, "with", round(prev_dmg, 1), "damage"
    #5print "Worst weapon versus", armor, "armor is", worst_weapon, "with", round(prev_bad_dmg, 1), "damage"
