import random
import math
import weakref
from time import sleep


###-------------------------------------------------------------- CLASSES -----------------------------------------------------------------###

class Type():
    '''  For move and pokemon type '''
    def __init__(self, typename):
        self.typename = typename
    
    def setEff(self, supereff, notveryeff, ineff):
        # From attacking move stand point
        self.supereff = supereff
        self.notveryeff = notveryeff
        self.ineff = ineff

    def __str__(self):
        return self.typename

class Category():
    '''  To specify move's category '''
    def __init__(self, ctgname):
        self.ctgname = ctgname

    def __str__(self):
        return f"({self.ctgname} move)"

class Moves():
    '''  Create moves that can be learned by pokemon '''
    def __init__(self, movename, movetype, pwr, acc, category):
        self.movename = movename
        self.movetype = movetype
        self.pwr = pwr
        self.acc = acc
        self.category = category
    
    def addEffect(self, statchgobj, bystage):
        '''  For stat category moves only '''
        self.statchgobj = statchgobj
        self.bystage = bystage

    def getMove(self):
        return self.movename

    def __str__(self):
        return self.movename

    def __repr__(self):
        return self.movename


class UniquePoke():
    '''  Superclass holding basic pokemon characteristics '''

    # List consists all pokemon created
    pokemonlist = []

    def __init__(self, name, poketype1, poketype2, statlist, movedict):
        # Use weakref to add future created object to list
        self.__class__.pokemonlist.append(weakref.proxy(self))
        self.name = name
        self.poketype1 = poketype1
        self.poketype2 = poketype2
        self.xp = 0
        # Assign its base stats
        self.bhp = statlist[0]
        self.batk = statlist[1]
        self.bdef = statlist[2]
        self.bspatk = statlist[3]
        self.bspdef = statlist[4]
        self.bspe = statlist[5]
        self.movedict = movedict

    def __str__(self):
        return self.name


class MyPokemon(UniquePoke):
    '''  To specify my pokemon '''

    def __init__(self, pokeobj, lvl, xp):
        self.pokeobj = pokeobj
        self.lvl = lvl
        # Calculate its stat
        self.shp = math.floor((((self.pokeobj.bhp*2) * self.lvl) / 100) + self.lvl + 10)
        self.satk = math.floor((((self.pokeobj.batk*2) * self.lvl) / 100) + 5)
        self.sdef = math.floor((((self.pokeobj.bdef*2) * self.lvl) / 100) + 5)
        self.sspatk = math.floor((((self.pokeobj.bspatk*2) * self.lvl) / 100) + 5)
        self.sspdef = math.floor((((self.pokeobj.bspdef*2) * self.lvl) / 100) + 5)
        self.sspe = math.floor((((self.pokeobj.bspe*2) * self.lvl) / 100) + 5)
        self.statlist = [self.shp, self.satk, self.sdef, self.sspatk, self.sspdef, self.sspe]
        self.xp = xp
        self.xplimit = self.lvl * 3
        # Assign its moveset after the movedict var
        self.movelist = []
        for k,v in self.pokeobj.movedict.items():
            if k <= self.lvl:
                self.movelist.append(v)
        while len(self.movelist) < 4:
            self.movelist.append("")
        self.movelist = self.movelist[-4:]
        self.move1 = self.movelist[0]
        self.move2 = self.movelist[1]
        self.move3 = self.movelist[2]
        self.move4 = self.movelist[3]

    def showStat(self):
        ''' To show current pokemon stat '''
        print(self.statlist)
        print("Total:", sum(self.statlist))

    def showMoves(self):
        ''' To inform current move available '''
        print("Moves available:\n 1.{:20} 3.{}\n 2.{:20} 4.{}".format(str(self.move1), str(self.move3), str(self.move2), str(self.move4)))

    def doMove(self, foeobj, movenum):
        ''' Retrieves foe's obj and move chosen,
            and do move's work '''
        move = self.movelist[int(movenum)-1]
        print(f"Your {self.pokeobj.name} used {move} on the foe's pokemon!")
        # STAB calculation
        if move.movetype == self.pokeobj.poketype1 or move.movetype == self.pokeobj.poketype1:
            stab = 1.5
        else:
            stab = 1
        # Type effectiveness calculation
        if foeobj.pokeobj.poketype1 in move.movetype.ineff or foeobj.pokeobj.poketype2 in move.movetype.ineff:
            print("It doesn't affect.")
            eff = 0
        elif foeobj.pokeobj.poketype1 in move.movetype.supereff and foeobj.pokeobj.poketype2 in move.movetype.supereff:
            print("It's very effective!")
            eff = 4
        elif bool(foeobj.pokeobj.poketype1 in move.movetype.supereff) ^ bool(foeobj.pokeobj.poketype2 in move.movetype.supereff):
            print("It's very effective!")
            eff = 2
        elif bool(foeobj.pokeobj.poketype1 in move.movetype.notveryeff) ^ bool(foeobj.pokeobj.poketype2 in move.movetype.notveryeff):
            print("It's not very effective!")
            eff = 0.5
        elif foeobj.pokeobj.poketype1 in move.movetype.notveryeff and foeobj.pokeobj.poketype2 in move.movetype.notveryeff:
            print("It's not very effective")
            eff = 0.25
        else:
            eff = 1
        mod = stab * eff
        print(move.category)
        print("Mod =",mod)
        # Use move accuracy chance
        if random.randrange(0, 100) < move.acc:
            if move.category == Phy:
                mydmg = math.floor((((((2*self.lvl)/5 + 2) * move.pwr * self.satk/foeobj.sdef) / 50) + 2) * mod)
                return mydmg
            elif move.category == Spc:
                mydmg = math.floor((((((2*self.lvl)/5 + 2) * move.pwr * self.sspatk/foeobj.sspdef) / 50) + 2) * mod)
                return mydmg
            ### NOT WORKING ###
            elif move.category == Stt:
                foeobj.sdef = assignEffect(move, move.statchgobj, move.bystage)
                foeobj.showStat()
                return 0
        else:
            print("The attack missed!")
            return 0

    def hpLoss(self, hitdmg):
        ''' Decrease current HP '''
        self.shp -= hitdmg

    def getHp(self):
        ''' Return current HP value'''
        return self.shp

    def showHp(self):
        ''' Print current HP state '''
        print(f"*Your {self.pokeobj.name} HP is now {self.shp}.")

    def gainXp(self, xpgain):
        ''' Increase current exp point '''
        self.xp += xpgain
        return f"Your pokemon gained {xpgain} exp points!"

    def getXp(self):
        ''' Get current exp value '''
        print(f"Now Your pokemon has {self.xp} exp.")
        return self.xp
    
    def evalStat(self):
        ''' Evaluate state after battle
            including lvl up, exp now, and new move '''
        print("Current exp:", self.xp, "from", self.xplimit)
        if self.xp >= self.xplimit:
            self.lvl += 1
            self.xp %= self.xplimit
            print(f"\nYour pokemon grew to lvl {self.lvl}!")
            for k,v in self.pokeobj.movedict.items():
                if k == self.lvl and "" not in self.movelist and v not in self.movelist:
                    sleep(0.5)
                    print(f"Your pokemon wants to learn {v}, which move would you want to forget?")
                    sleep(0.3)
                    self.showMoves()
                    update_move = ""
                    while update_move not in [str(num+1) for num in range(len(self.movelist))]:
                        update_move = input(">>")
                    forget = self.movelist[int(update_move)-1]
                    self.movelist[int(update_move)-1] = v
                    print(f"Your pokemon forget {forget}, and now learn {v}")
                elif k == self.lvl and "" in self.movelist and v not in self.movelist:
                    self.movelist[self.movelist.index("")] = v
                    print(f"Your pokemon now learn {v}!")
            self.move1 = self.movelist[0]
            self.move2 = self.movelist[1]
            self.move3 = self.movelist[2]
            self.move4 = self.movelist[3]
            return self.lvl, self.xp
        else:
            return self.lvl, self.xp
        
    def updateState(self, lvl, xp):
        ''' Update stat of mycurrent pokemon
            due to lvl up after battle '''
        self.lvl = lvl
        self.xp = xp
        self.shp = math.floor((((self.pokeobj.bhp*2) * self.lvl) / 100) + self.lvl + 10)
        self.satk = math.floor((((self.pokeobj.batk*2) * self.lvl) / 100) + 5)
        self.sdef = math.floor((((self.pokeobj.bdef*2) * self.lvl) / 100) + 5)
        self.sspatk = math.floor((((self.pokeobj.bspatk*2) * self.lvl) / 100) + 5)
        self.sspdef = math.floor((((self.pokeobj.bspdef*2) * self.lvl) / 100) + 5)
        self.sspe = math.floor((((self.pokeobj.bspe*2) * self.lvl) / 100) + 5)
        self.xplimit = self.lvl * 3
        
    def __str__(self):
        return f"You have a lvl {self.lvl} {self.pokeobj.name}."

    def __repr__(self):
        return self.name


class WildPokemon(UniquePoke):
    ''' To specify wild pokemon '''

    def __init__(self, pokeobj, lvl):
        self.pokeobj = pokeobj
        self.lvl = lvl
        self.yieldXp = (self.lvl * 3) + 2
        # Calculate its stat
        self.shp = math.floor((((self.pokeobj.bhp*2) * self.lvl) / 100) + self.lvl + 10)
        self.satk = math.floor((((self.pokeobj.batk*2) * self.lvl) / 100) + 5)
        self.sdef = math.floor((((self.pokeobj.bdef*2) * self.lvl) / 100) + 5)
        self.sspatk = math.floor((((self.pokeobj.bspatk*2) * self.lvl) / 100) + 5)
        self.sspdef = math.floor((((self.pokeobj.bspdef*2) * self.lvl) / 100) + 5)
        self.sspe = math.floor((((self.pokeobj.bspe*2) * self.lvl) / 100) + 5)
        self.statlist = [self.shp, self.satk, self.sdef, self.sspatk, self.sspdef, self.sspe]
        # Assigning moveset
        self.movelist = []
        for k,v in self.pokeobj.movedict.items():
            if k <= self.lvl:
                self.movelist.append(v)
        while len(self.movelist) < 4:
            self.movelist.append("")
        self.movelist = self.movelist[-4:]
        self.move1 = self.movelist[0]
        self.move2 = self.movelist[1]
        self.move3 = self.movelist[2]
        self.move4 = self.movelist[3]

    def showStat(self):
        ''' To show current pokemon stat '''
        print(self.statlist)
        print("Total:", sum(self.statlist))

    def showMoves(self):
        ''' To inform current move available '''
        return f"Foe's moves:\n 1.{self.move1}\n 2.{self.move2}\n 3.{self.move3}\n 4.{self.move4}"

    def doMove(self, myobj):
        ''' Retrieves my obj and move chosen,
            and do move's work '''
        count = countMoves(self)
        movenum = random.randint(1, count)
        move = self.movelist[movenum-1]
        print(f"Foe's {self.pokeobj.name} used {move} on your pokemon!")
        # STAB calculation
        if move.movetype == self.pokeobj.poketype1 or move.movetype == self.pokeobj.poketype1:
            stab = 1.5
        else:
            stab = 1
        # Type effectiveness calculation
        if myobj.pokeobj.poketype1 in move.movetype.ineff or myobj.pokeobj.poketype2 in move.movetype.ineff:
            print("It doesn't affect.")
            eff = 0
        elif myobj.pokeobj.poketype1 in move.movetype.supereff and myobj.pokeobj.poketype2 in move.movetype.supereff:
            print("It's very effective!")
            eff = 4
        elif bool(myobj.pokeobj.poketype1 in move.movetype.supereff) ^ bool(myobj.pokeobj.poketype2 in move.movetype.supereff):
            print("It's very effective!")
            eff = 2
        elif bool(myobj.pokeobj.poketype1 in move.movetype.notveryeff) ^ bool(myobj.pokeobj.poketype2 in move.movetype.notveryeff):
            print("It's not very effective!")
            eff = 0.5
        elif myobj.pokeobj.poketype1 in move.movetype.notveryeff and myobj.pokeobj.poketype2 in move.movetype.notveryeff:
            print("It's not very effective")
            eff = 0.25
        else:
            eff = 1
        mod = stab * eff
        print(move.category)
        print("Mod =", mod)
        # Use move accuracy chance
        if random.randrange(0, 100) < move.acc:
            if move.category == Phy:
                foedmg = math.floor((((((2*self.lvl)/5 + 2) * move.pwr * self.satk/myobj.sdef) / 50) + 2) * mod)
                return foedmg
            elif move.category == Spc:
                foedmg = math.floor((((((2*self.lvl)/5 + 2) * move.pwr * self.sspatk/myobj.sspdef) / 50) + 2) * mod)
                return foedmg
        else:
            print("The attack missed!")
            return 0

    def hpLoss(self, hitdmg):
        ''' Decrease current HP '''
        self.shp -= hitdmg

    def getHp(self):
        ''' Return current HP value'''
        return self.shp

    def showHp(self):
        ''' Print current HP state '''
        print(f"*Foe's {self.pokeobj.name} HP is now {self.shp}.")
        
    def __str__(self):
        return f"A wild lvl {self.lvl} {self.pokeobj.name} appeared!"

    def __repr__(self):
        return self.name

class Area():
    ''' Create area consisting a range of wild pokemon '''

    # List consists of all area created
    arealist = []

    def __init__(self, areaname, wildict):
        # Use weakref to add future created object to list
        self.__class__.arealist.append(weakref.proxy(self))
        self.areaname = areaname
        self.wildict = wildict

    def __str__(self):
        return self.areaname

##############################################################################################################################################


###-------------------------------------------------------- IN-GAME FUNCTIONS -------------------------------------------------------------###

def chooseArea():
    ''' To ask for user's input to choose which area to go '''
    print("Area available:")
    for i in range(len(Area.arealist)):
        print(f" {i+1}.{Area.arealist[i]}")
    # Undesired input handling
    choose_area = ''
    while choose_area not in [str(num+1) for num in range(len(Area.arealist))]:
        print("Which area would you go into?")
        choose_area = input("> ")
    sleep(1)
    print()
    area = Area.arealist[int(choose_area)-1]
    print(f"You are now in {area}\n")
    return area

def countMoves(pokemon):
    ''' To count how many movse a pokemon knows yet '''
    count = 0
    for move in pokemon.movelist:
        if move != "":
            count += 1
    return count

def askQuit():
    ''' To ask for user's input to continue playing or not '''
    valid = False
    while not valid:
        # Asking for user's input to continue
        stay = input("Keep going? [Y/n] ").lower()
        if stay == 'y':
            # Back to battle loop
            sleep(0.5)
            valid = True
            exit = False
            print()
            print("------------------------------")
            print("------------------------------")
            print()
            return valid, exit
        elif stay == 'n':
            # Exit the game
            print("\n~Have a nice day!~")
            valid = True
            exit = True
            return valid, exit
        # Undesired input handling
        else:
            pass

def assignEffect(move, statobj, bystage):
    ### NOT WORKING ###
    print("awal", statobj)
    # When lowering stat
    if move.bystage < 0:
        multiplier = 2 / (2+(-move.bystage))
        print(multiplier)
        statobj *= multiplier
        print(statobj)
        print(f"The {statobj} stat was lowered by {-bystage} stage!")
        return statobj
    # When increasing stat
    elif move.bystage > 0:
        multiplier = (2+move.bystage) / 2
        print(multiplier)
        statobj *= multiplier
        print(statobj)
        print(f"The {statobj} stat was rose by {bystage} stage!")
        return statobj
##############################################################################################################################################


###------------------------------------------------------INFORMATIONS INITIATION-----------------------------------------------------------###

# All type initiation
Empty = Type("")
Normal = Type("Normal")
Fire = Type("Fire")
Water = Type("Water")
Electric = Type("Electric")
Grass = Type("Grass")
Ice = Type("Ice")
Fighting = Type("Fighting")
Poison = Type("Poison")
Ground = Type("Ground")
Flying = Type("Flying")
Psychic = Type("Psychic")
Bug = Type("Bug")
Rock = Type("Rock")
Ghost = Type("Ghost")
Dragon = Type("Dragon")
Dark = Type("Dark")
Steel = Type("Steel")

# Type effectiveness initiation
Empty.setEff([], [], [])
Normal.setEff([], [Rock, Steel], [Ghost])
Fire.setEff([Grass, Ice, Bug, Steel], [Fire, Water, Rock, Dragon], [])
Water.setEff([Fire, Ground, Rock], [Water, Grass, Dragon], [])
Electric.setEff([Water, Flying], [Electric, Grass, Dragon], [Ground])
Grass.setEff([Water, Ground, Rock], [Fire, Grass, Poison, Flying, Bug, Dragon, Steel], [])
Ice.setEff([Grass, Ground, Flying, Dragon], [Fire, Water, Ice, Steel], [])
Fighting.setEff([Normal, Ice, Rock, Dark, Steel], [Poison, Flying, Psychic, Bug], [Ghost])
Poison.setEff([Grass], [Poison, Ground, Rock, Ghost], [Steel])
Ground.setEff([Fire, Electric, Poison, Rock, Steel], [Grass, Bug], [Flying])
Flying.setEff([Grass, Fighting, Bug], [Electric, Rock, Steel], [])
Psychic.setEff([Fighting, Poison], [Psychic, Steel], [Dark])
Bug.setEff([Grass, Psychic, Dark], [Fire, Fighting, Poison, Flying, Rock, Steel], [])
Rock.setEff([Fire, Ice, Flying, Bug], [Fighting, Ground, Steel], [])
Ghost.setEff([Psychic, Ghost], [Dark], [Normal])
Dragon.setEff([Dragon], [Steel], [])
Dark.setEff([Psychic, Ghost], [Fighting, Dark], [])
Steel.setEff([Ice, Rock], [Fire, Water, Electric, Steel], [])

# Move category initiation
Phy = Category("Physical")
Spc = Category("Special")
Stt = Category("Stat")

# Available moves initiation
Tackle = Moves("Tackle", Normal, 40, 100, Phy)
Scratch = Moves("Scratch", Normal, 40, 100, Phy)
Pound = Moves("Pound", Normal, 40, 100, Phy)

Leer = Moves("Leer", Empty, 0, 100, Stt)

Peck = Moves("Peck", Flying, 45, 100, Phy)
Metal_Claw = Moves("Metal Claw", Steel, 45, 95, Phy)
Mud_Shot = Moves("Mud Shot", Ground, 45, 95, Spc)
Vine_Whip = Moves("Vine Whip", Grass, 45, 95, Phy)
Ember = Moves("Ember", Fire, 45, 95, Spc)
Bubble = Moves("Bubble", Water, 45, 95, Spc)
Thunder_Shock = Moves("Thunder Shock", Electric, 45, 95, Spc)
Slam = Moves("Slam", Normal, 50, 90, Phy)
Shock_Wave = Moves("Shock Wave", Electric, 60, 85, Spc)

# Available pokemon initiation
Pikachu = UniquePoke("Pikachu", Electric, Steel, [35, 55, 40, 50, 50, 90], movedict={2:Leer, 4:Thunder_Shock, 7:Peck, 12:Mud_Shot, 14:Shock_Wave})
Treecko = UniquePoke("Treecko", Dragon, Ground, [40, 45, 35, 65, 55, 70], movedict={2:Tackle, 4:Peck, 7:Vine_Whip})
Torchic = UniquePoke("Torchic", Fire, Fighting, [45, 60, 40, 70, 50, 45], movedict={2:Scratch, 4:Metal_Claw, 7:Ember})
Mudkip = UniquePoke("Mudkip", Water, Ground, [50, 70, 50, 50, 50, 40], movedict={2:Pound, 4:Mud_Shot, 7:Bubble})
Poochyena = UniquePoke("Poochyena", Dark, Ghost, [38, 30, 41, 30, 30, 35], movedict={2:Scratch, 2:Peck, 4:Slam})
Zigzagoon = UniquePoke("Zigzagoon", Normal, Rock, [35, 55, 35, 30, 41, 60], movedict={2:Tackle, 2:Scratch, 4:Pound})
Wurmple = UniquePoke("Wurmple", Bug, Poison, [45, 45, 35, 20, 30, 20], movedict={2:Pound, 2:Tackle, 4:Peck})

# Available areas initiation
Route_101 = Area("Route 101", {Poochyena:[2,3], Zigzagoon:[2,3]})
Route_103 = Area("Route 103", {Poochyena:[2,4], Zigzagoon:[2,4], Wurmple:[2,4]})
Victory_Road = Area("Victory Road", {Treecko:[9,12], Torchic:[9,12], Mudkip:[9,12], Poochyena:[9,12], Zigzagoon:[9,12], Wurmple:[9,12]})

###############################################################################################################################################
###############################################################################################################################################


def main():
    ''' This is the main function of the program '''

    # Greetings
    print("\nWelcome to The Pokemon World!")
    print("-----------------------------")
    sleep(0.5)

    # My pokemon starting initiation
    lvl_now = 11
    xp_now = 0
    my_pokemon = MyPokemon(Pikachu, lvl=lvl_now, xp=xp_now)
    
    # Battle scene
    exit = False
    while not exit:
        # Ask for chosen area
        area = chooseArea()
        sleep(0.3)

        # Pokemon update  and wild pokemon initiation every starting battle scene
        my_pokemon.updateState(lvl_now, xp_now)
        random_poke = random.choice(list(area.wildict))
        lvl_min, lvl_max = area.wildict[random_poke]
        wild_pokemon = WildPokemon(random_poke, lvl=random.randint(lvl_min, lvl_max))

        # Testing stat changing move
        Leer.addEffect(wild_pokemon.sdef, -1)

        # Print current pokemon state
        print(f"{my_pokemon} ({my_pokemon.sspe})")
        my_pokemon.showStat()
        print()
        print(f"{wild_pokemon} ({wild_pokemon.sspe})")
        wild_pokemon.showStat()
        print()
        my_pokemon.showHp()
        wild_pokemon.showHp()

        # Battle loop
        while my_pokemon.getHp() > 0 and wild_pokemon.getHp() > 0:
            print()
            my_pokemon.showMoves()

            # Asking for user's intended move
            count = countMoves(my_pokemon)
            choose_move = ''
            while choose_move not in [str(num+1) for num in range(count)]:
                print("Which move would you use?")
                choose_move = input("> ")
            sleep(0.5)
            print()

            # When your speed is faster
            if my_pokemon.sspe >= wild_pokemon.sspe:
                # Your damage calculations
                mydmg = my_pokemon.doMove(wild_pokemon, choose_move)
                wild_pokemon.hpLoss(mydmg)
                wild_pokemon.showStat()
                # If the enemy survives
                if wild_pokemon.getHp() > 0:
                    wild_pokemon.showHp()
                    sleep(0.5)
                    foedmg = wild_pokemon.doMove(my_pokemon)
                    my_pokemon.hpLoss(foedmg)
                    if my_pokemon.getHp() <= 0:
                        # Exit the battle
                        print("Your pokemon has fainted.")
                        print("You have been thrown out of the game")
                        exit = True
                    elif my_pokemon.getHp() > 0:
                        my_pokemon.showHp()
                        sleep(1)
                        print("\n------------------------------")
                # Else if the enemy faints
                elif wild_pokemon.getHp() <= 0:
                    # Update xp and level gains
                    print("The foe's pokemon has fainted!")
                    sleep(0.5)
                    print(my_pokemon.gainXp(wild_pokemon.yieldXp))
                    lvl_now, xp_now = my_pokemon.evalStat()
                    sleep(0.3)
                    # my_pokemon.updateState(lvl_now, xp_now)
                    valid, exit = askQuit()
                            
            # When your speed is lower
            elif my_pokemon.sspe < wild_pokemon.sspe:
                # The opponent's damage calculation
                foedmg = wild_pokemon.doMove(my_pokemon)
                my_pokemon.hpLoss(foedmg)
                # If your pokemon faints
                if my_pokemon.getHp() <= 0:
                    print("Your pokemon has fainted.")
                    print("You have been thrown out of the game")
                    exit = True
                # Else if your pokemon survives
                elif my_pokemon.getHp() > 0:
                    my_pokemon.showHp()
                    mydmg = my_pokemon.doMove(wild_pokemon, choose_move)
                    wild_pokemon.hpLoss(mydmg)
                    sleep(0.5)
                    # If the enemy survives
                    if wild_pokemon.getHp() > 0:
                        wild_pokemon.showHp()
                        sleep(1)
                        print("\n------------------------------")
                    # Else if the enemy faints
                    elif wild_pokemon.getHp() <= 0:
                        # Update xp and level gains
                        print("The foe's pokemon has fainted!")
                        sleep(0.5)
                        print(my_pokemon.gainXp(wild_pokemon.yieldXp))
                        lvl_now, xp_now = my_pokemon.evalStat()
                        sleep(0.3)
                        # my_pokemon.updateState(lvl_now, xp_now)
                        valid, exit = askQuit()


if __name__ == '__main__':
    main()