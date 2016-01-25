#!/usr/bin/python2.7

import attack

target = "war1473"
target_char = attack.characters[target]
attacker = "septeract"
attacker_char = attack.characters[attacker]

tot_prev_dmg = -1000000
best_weapon = "ERROR"
best_armor = "ERROR"

for atkweapon in attack.weapons:
    attacker_char["weapon"] = atkweapon

    for atkarmor in attack.materials:
        attacker_char["armor"] = atkarmor

        prev_dmg = 0
        i = 0

        for weapon in attack.weapons:
            target_char["weapon"] = weapon
            
            for armor in attack.materials:
                if armor == "cloth":
                    continue
                target_char["armor"] = armor

                good_dmg = 0
                for i in xrange(100):
                    good_dmg += attack.attack(attacker, target, False)
                good_dmg /= 100

                bad_dmg = 0
                for i in xrange(100):
                    bad_dmg += attack.attack(target, attacker)
                bad_dmg /= 100

                #print weapon, armor, dmg, bad_dmg

                dmg = good_dmg - bad_dmg

                #print weapon, armor, dmg

                prev_dmg += dmg
                i += 1

        prev_dmg /= i

        print atkweapon, atkarmor, prev_dmg

        if prev_dmg > tot_prev_dmg:
            tot_prev_dmg = prev_dmg
            best_weapon = atkweapon
            best_armor = atkarmor

if best_weapon == "ERROR":
    print target, "is undefeatable"
elif tot_prev_dmg < 0:
    print "Best weapon choice overall is", best_weapon, "with", best_armor, "armor, though", target, "averages higher damage"
else:
    print "Best weapon choice overall is", best_weapon, "with", best_armor, "armor"
    
#print tot_good_dmg, "damage vs", tot_bad_dmg, "damage"
