#!/usr/bin/python2.7

import attack
import random
import time

if attack.MASK & attack._MAGIC:
    _MAGIC = True
else:
    _MAGIC = False

ATTACKS = ("%p lunges at %e, dealing %d damage!",
           "%p brutalizes %e for %d damage!",
           "%p retaliates for %d damage!",
           "%p ripostes for %d damage!",
           "%p stabs out at %e, dealing %d damage!",
           "%p deals %d damage to %e!",
           "%p attacks %e for %d damage!",
           "%p lashes out at %e for %d damage!")

MAGIC = ("%p casts a spell at %e, dealing %d damage!",
         "%p shouts at %e for %d damage!",
         "%p shouts an incantation, dealing %d damage to %e!")

KILLS = ("%p rips %e apart!",
         "%p murders %e!",
         "%p eats %e's soul!",
         "%p ends %e!",
         "%p kills %e!",
         "%p terminates %e!",
         "%p has defeated %e!",
         "%p has killed %e!")

def mainloop(player0, player1):
    player0_char = attack.characters[player0]
    player1_char = attack.characters[player1]

    player0_char["health"] = attack.max_health(player0)
    player1_char["health"] = attack.max_health(player1)

    dmg = round(attack.attack(player0, player1, True, True),1)
    print player0, "sneak-attacks", player1, "for", dmg, "damage!", "\n", player0 + ":", round(player0_char["health"],1), "hp,", player1 + ":", round(player1_char["health"],1), "hp\n"
    time.sleep(1)

    while round(player0_char["health"],1) > 0 and round(player1_char["health"],1) > 0:
        if round(player1_char["health"],1) > 0:
            dmg = round(attack.attack(player1, player0, False, True),1)
            if dmg > 0:
                print random.choice(ATTACKS).replace("%e",player0).replace("%p",player1).replace("%d",str(dmg)), "\n", player0 + ":", round(player0_char["health"],1), "hp,", player1 + ":", round(player1_char["health"],1), "hp\n"
            else:
                print player1, "misses", player0, "completely!", "\n", player0 + ":", round(player0_char["health"],1), "hp,", player1 + ":", round(player1_char["health"],1), "hp\n"
            time.sleep(1)
        if round(player0_char["health"],1) > 0:
            spell = ""
            if _MAGIC:
                spell = raw_input("Spell: ")
                
            if spell == "":
                dmg = round(attack.attack(player0, player1, False, True),1)
                if dmg > 0:
                    print random.choice(ATTACKS).replace("%e",player1).replace("%p",player0).replace("%d",str(dmg)), "\n", player0 + ":", round(player0_char["health"],1), "hp,", player1 + ":", round(player1_char["health"],1), "hp\n"
                else:
                    print player0, "misses", player1, "completely!", "\n", player0 + ":", round(player0_char["health"],1), "hp,", player1 + ":", round(player1_char["health"],1), "hp\n"
                time.sleep(1)
            else:
                dmg = round(attack.attack(player0, player1, False, True, spell),1)
                if dmg > 0:
                    print random.choice(MAGIC).replace("%e",player1).replace("%p",player0).replace("%d",str(dmg)), "\n", player0 + ":", round(player0_char["health"],1), "hp,", player1 + ":", round(player1_char["health"],1), "hp\n"
                else:
                    print player0, "misses", player1, "completely!", "\n", player0 + ":", round(player0_char["health"],1), "hp,", player1 + ":", round(player1_char["health"],1), "hp\n"
                time.sleep(1)

    if round(player0_char["health"],1) > 0:
        print random.choice(KILLS).replace("%e",player1).replace("%p",player0)

        print "VICTOR:", player0
    elif round(player1_char["health"],1) > 0:
        print random.choice(KILLS).replace("%e",player0).replace("%p",player1)

        print "VICTOR:", player1
    else:
        print player0, "and", player1, "killed each other!"
        print "VICTOR: no-one"

def main(*args, **kwargs):
    player1 = raw_input("Player 1: ")
    if player1 == "":
        player1 = "septeract"
    player2 = raw_input("Player 2: ")
    if player2 == "":
        player2 = "war1473"
        
    mainloop(player1, player2)

if __name__ == "__main__":
    try:
        __exec__
    except:
        main()
