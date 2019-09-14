import gamelib
import random
import math
import warnings
from sys import maxsize
import json


"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips:

  - You can analyze action frames by modifying on_action_frame function

  - The GameState.map object can be manually manipulated to create hypothetical
  board states. Though, we recommended making a copy of the map to preserve
  the actual current map state.
"""

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        gamelib.debug_write('Random seed: {}'.format(seed))
        #gamelib.debug_write('Methods {}'.format(__dir(gamelib.GameState(self.config, turn))))

    def on_game_start(self, config):
        """
        Read in config and perform any initial setup here
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]
        # This is a good place to do initial setup
        self.scored_on_locations = []




    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        gamelib.debug_write('BIBBA')
        game_state.suppress_warnings(True)  #Comment or remove this line to enable warnings.

        #self.starter_strategy(game_state)
        if game_state.turn_number == 0:
            gamelib.debug_write('BABBA')
            self.build_skeleton(game_state)
        #elif game_state.turn_number % 2 == 0: #TODO not all the time
        else:
            gamelib.debug_write('BOBBA')
            self.build_defences(game_state, 1)
            #self.deploy_defensive_strategy(game_state)
            #pass
        game_state.submit_turn()

    def build_skeleton(self, game_state):
        destructors = [[0, 13], [1, 13], [2, 13], [3, 13], [5, 13], [6, 13], [7, 13], [8, 13], [12, 13], [15, 13], [19, 13], [20, 13], [21, 13], [22, 13], [24, 13], [25, 13], [26, 13], [27, 13]]
        encryptors = [[9, 13], [11, 13], [16, 13], [18, 13]]
        for elt in destructors:
            game_state.attempt_spawn(DESTRUCTOR, elt)
        for elt in encryptors:
            game_state.attempt_spawn(ENCRYPTOR, elt)
            #gamelib.spawn("You have {} cores".format(game_state.get_resource(game_state.CORES)))
    def build_defences(self, game_state, row):
        gamelib.debug_write("HELLO")
        if row == 0:
            turn = game_state.turn_number
            v0 = [[0, 13], [1, 13], [2, 13], [3, 13], [5, 13], [6, 13], [7, 13], [8, 13], [12, 13], [15, 13], [19, 13], [20, 13], [21, 13], [22, 13], [24, 13], [25, 13], [26, 13], [27, 13]]
            v1 = [[9, 13], [11, 13], [16, 13], [18, 13]] # E
            v2 = [[10, 13], [13, 13], [14, 13], [17, 13], [4, 11], [6, 11], [7, 11], [20, 11], [21, 11], [23, 11]] #D
            v3 =  [[11, 11], [12, 11], [15, 11], [16, 11]] # E
            v4 =  [[1, 12], [26, 12], [3, 11], [13, 11], [14, 11], [24, 11], [3, 10], [24, 10]] # D

            # E D E D E D
            v5 = [[5, 9], [6, 9], [7, 9], [8, 9], [9, 9], [10, 9], [11, 9], [12, 9], [13, 9], [14, 9], [15, 9], [16, 9], [17, 9], [18, 9], [19, 9], [20, 9], [22, 9], [6, 8]]
            v6 = [[8, 11], [9, 11], [10, 11], [17, 11], [18, 11], [19, 11], [4, 10], [23, 10], [4, 9], [23, 9], [5, 8], [22, 8]]
            v7 =  [[20, 7], [19, 7], [18, 7], [17, 7], [15, 7], [14, 7], [13, 7], [12, 7], [10, 7], [9, 7], [8, 7], [6, 7]]
            v8 =  [[20, 6], [21, 7], [16, 7], [11, 7]]
            v9 = [[19, 6], [9, 5], [10, 5], [11, 5], [12, 5], [15, 5], [16, 5], [17, 5], [19, 5]]
            v10 = [[8, 5], [13, 5], [14, 5]]
            v11 = [[16, 3], [15, 3], [14, 3], [13, 3], [12, 3]]
            v12 = [[17, 3], [10, 3]]
            v13 = [[12, 1], [13, 1], [15, 1]]

            random.shuffle(v0)
            random.shuffle(v1)
            random.shuffle(v2)
            random.shuffle(v3)
            random.shuffle(v4)

            all_tiers = [v0,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13]

            total_monies = game_state.get_resource(game_state.CORES)
            for i in range(len(all_tiers)):
                if i > 5 and total_monies < 20:
                    return
                for loc in all_tiers[i]:
                    # case for D
                    if i % 2 == 0:
                        if not game_state.contains_stationary_unit(loc) and total_monies < 2:
                            return
                        elif not game_state.contains_stationary_unit(loc):
                            total_monies -=2
                            game_state.attempt_spawn(DESTRUCTOR,loc)
                    # case for E
                    elif i % 2 == 1:
                        if not game_state.contains_stationary_unit(loc) and total_monies < 1:
                            return
                        elif not game_state.contains_stationary_unit(loc):
                            total_monies -=1
                            game_state.attempt_spawn(ENCRYPTOR,loc)
            #Also want to remove superflous items
            all_items = []
            for tier in all_tiers:
                all_items += tier
            for location in game_state.game_map:
                if location not in all_items:
                    game_state.attempt_remove(location)
        if row == 1:
            v0 = [[2, 12], [3, 12], [5, 12], [6, 12], [8, 12], [9, 12], [13, 12], [14, 12], [18, 12], [19, 12], [21, 12], [22, 12], [24, 12], [25, 12]]
            v1 = [[0, 13], [1, 13], [11, 13], [16, 13], [26, 13], [27, 13]]
            v2 = [[1, 12], [10, 12], [12, 12], [15, 12], [17, 12], [26, 12], [3, 10], [7, 10], [8, 10], [9, 10], [18, 10], [19, 10], [20, 10], [24, 10], [4, 9], [23, 9]]
            v3 = [[11, 12], [16, 12], [13, 10], [14, 10]]
            v4 = [[5, 10], [10, 10], [11, 10], [12, 10], [15, 10], [16, 10], [17, 10], [22, 10], [5, 9], [22, 9]]
            v5 = [[7, 12], [20, 12], [6, 8], [7, 8], [8, 8], [9, 8], [10, 8], [12, 8], [13, 8], [14, 8], [15, 8], [17, 8], [18, 8], [19, 8], [21, 8], [21, 7]]
            v6 = [[5, 8], [11, 8], [16, 8], [22, 8], [6, 7], [7, 7], [7, 6]]
            v7 = [[20, 6], [19, 6], [18, 6], [16, 6], [14, 6], [13, 6], [11, 6], [9, 6]]
            v8 =  [[10, 6], [12, 6], [15, 6], [17, 6], [18, 5], [19, 5], [18, 4]]
            v9 = [[7, 13], [20, 13]]
            v10 = [[9, 4], [10, 4], [11, 4], [12, 4], [13, 4], [14, 4], [15, 4], [16, 4]]
            v11 =  [[10, 3], [11, 3]]
            v12 = [[3, 13], [9, 13], [13, 13], [14, 13], [18, 13], [24, 13]]
            v13 =  [[11, 2], [13, 2], [14, 2], [15, 2], [16, 2]]
            v14 = [[14, 1], [15, 1]]

            all_tiers = [v0,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14]
            DFDEDEDEDFEDFEE
            encryptors = [3,5,7,10,13,14]
            filters = [1,9,12]
            destructors = [0,2,4,6,8,11]
            total_monies = game_state.get_resource(game_state.CORES)
            for i in range(len(all_tiers)):
                if i > 5 and total_monies < 20:
                    return
                for loc in all_tiers[i]:
                    # case for D
                    if i in destructors:
                        if not game_state.contains_stationary_unit(loc) and total_monies < 2:
                            return
                        elif not game_state.contains_stationary_unit(loc):
                            total_monies -=2
                            game_state.attempt_spawn(DESTRUCTOR,loc)
                    # case for E
                    elif i in encryptors:
                        if not game_state.contains_stationary_unit(loc) and total_monies < 1:
                            return
                        elif not game_state.contains_stationary_unit(loc):
                            total_monies -=1
                            game_state.attempt_spawn(ENCRYPTOR,loc)
                    elif i in filters:
                        if not game_state.contains_stationary_unit(loc) and total_monies < 3:
                            return
                        elif not game_state.contains_stationary_unit(loc):
                            total_monies -=3
                            game_state.attempt_spawn(FILTER,loc)
                #Also want to remove superflous items
                all_items = []
                for tier in all_tiers:
                    all_items += tier
                for location in game_state.game_map:
                    if location not in all_items:
                        game_state.attempt_remove(location)
            if row == 3:
                v0 = [[2, 11], [3, 11], [4, 11], [6, 11], [7, 11], [8, 11], [9, 11], [13, 11], [14, 11], [18, 11], [19, 11], [20, 11], [21, 11], [23, 11], [24, 11], [25, 11]]
                v1 = [[0, 13], [27, 13], [1, 12], [3, 12], [11, 12], [16, 12], [24, 12], [26, 12]]
                v2 = [[6, 9], [10, 9], [11, 9], [12, 9], [15, 9], [16, 9], [17, 9], [21, 9]]
                v3 = [[10, 11], [11, 11], [12, 11], [15, 11], [16, 11], [17, 11], [4, 9], [5, 9], [22, 9], [23, 9]]
                v4 = [[8, 12], [19, 12]]
                v5 = [[13, 9], [14, 9], [7, 8], [21, 8], [7, 7], [8, 7], [9, 7], [10, 7], [12, 7], [13, 7], [14, 7], [15, 7], [17, 7], [18, 7], [19, 7], [21, 7]]
                v6 = [[7, 9], [9, 9], [18, 9], [20, 9], [6, 8], [22, 8], [11, 7], [16, 7]]
                v7 = [[19, 5], [18, 5], [16, 5], [14, 5], [13, 5], [11, 5], [8, 5], [8, 6]]
                v8 =  [[5, 8], [6, 7], [7, 6], [12, 5], [15, 5], [18, 4]]
                v9 = [[2, 13], [13, 13], [14, 13], [25, 13]]
                v10 = [[17, 4], [10, 3], [11, 3], [12, 3], [13, 3], [14, 3], [15, 3], [17, 3]]
                v11 = [[10, 5], [17, 5], [11, 2]]
                v12 = [[7, 13], [9, 13], [18, 13], [20, 13]]
                v13 = [[12, 2], [12, 1], [14, 1], [15, 1]]
                v14 = [[6, 12], [21, 12]]

                all_tiers = [v0,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14]
                DFDEFEDEDFEDFEF
                encryptors = [3,5,7,10,13]
                filters = [1,4,9,12,14]
                destructors = [0,2,6,8,11]
                total_monies = game_state.get_resource(game_state.CORES)
                for i in range(len(all_tiers)):
                    if i > 5 and total_monies < 20:
                        return
                    for loc in all_tiers[i]:
                        # case for D
                        if i in destructors:
                            if not game_state.contains_stationary_unit(loc) and total_monies < 2:
                                return
                            elif not game_state.contains_stationary_unit(loc):
                                total_monies -=2
                                game_state.attempt_spawn(DESTRUCTOR,loc)
                        # case for E
                        elif i in encryptors:
                            if not game_state.contains_stationary_unit(loc) and total_monies < 1:
                                return
                            elif not game_state.contains_stationary_unit(loc):
                                total_monies -=1
                                game_state.attempt_spawn(ENCRYPTOR,loc)
                        elif i in filters:
                            if not game_state.contains_stationary_unit(loc) and total_monies < 3:
                                return
                            elif not game_state.contains_stationary_unit(loc):
                                total_monies -=3
                                game_state.attempt_spawn(FILTER,loc)
                #Also want to remove superflous items
                all_items = []
                for tier in all_tiers:
                    all_items += tier
                for location in game_state.game_map:
                    if location not in all_items:
                        game_state.attempt_remove(location)
            random.shuffle(v2)




    """
    NOTE: All the methods after this point are part of the sample starter-algo
    strategy and can safely be replaced for your custom algo.
    """

    def opponents_top_heavy(self):
        ## TODO: We want to check if they have a lot of disrupters in the top
        return False
    def generate_defensive_strategy(self):
        """ A description of our priorities in our defensive architecture
        :return: List [level1[(loc,TYPE),], level2[(loc,TYPE)]]
        """
        if self.opponents_top_heavy():


            #TODO: we will do a different strategy
            pass
        else:
            level0 = [((2,13),DESTRUCTOR),((3,13),DESTRUCTOR),((10,13),DESTRUCTOR),((17,13),DESTRUCTOR),((24,13),DESTRUCTOR),
            ((25,13),DESTRUCTOR)]
            level1 = [((9,13),FILTER),((13,13),FILTER),((14,13),FILTER),((18,13),FILTER)]
            level2 = [((0,13),FILTER),((1,13),FILTER),((6,13),FILTER),((7,13),FILTER),((8,13),FILTER),
            ((19,13),FILTER),((20,13),FILTER),((26,13),FILTER),((27,13),FILTER),]
            level3 = [((3,11),DESTRUCTOR),((4,10),DESTRUCTOR),((10,11),DESTRUCTOR),((17,11),DESTRUCTOR),
            ((23,10),DESTRUCTOR),((24,11),DESTRUCTOR)]
            #level4 = []
            return [level0,level1,level2,level3]
    def get_worths(self,type):
        if type == FILTER:
            return 1
        if type == DESTRUCTOR:
            return 6
        if type == ECRYPTOR:
            return 4
    def deploy_defensive_strategy(self, game_state):
        gamelib.debug_write("You have {} cores".format(game_state.get_resource(game_state.CORES)))
        total_monies = game_state.get_resource(game_state.CORES)
        worths = {FILTER:1, DESTRUCTOR:6, ENCRYPTOR:4}
        for level in self.generate_defensive_strategy():
            random.shuffle(level)
            for item in level:
                loc = item[0]
                type = item[1]
                worth = self.get_worths(type)
                gamelib.debug_write("Before {} cores".format(total_monies))
                if worth > total_monies:
                    return
                #    gamelib.debug_write("Only {} cores".format(game_state.get_resource(game_state.CORES)))
                #    return
                #    gamelib.debug_write("no money left {}".format(total_monies))
                #    gamelib.debug_write("a {} is worth {}".format(type, worth))
                #    gamelib.debug_write("destructor is {}".format(DESTRUCTOR))
                #    gamelib.debug_write("filter is {}".format(FILTER))
                #    return
                #print(loc)
                #if game_state.game_map
                gamelib.debug_write("state is {} at coord({},{})".format(game_state.game_map[loc[0],loc[1]],loc[0],loc[1]))
                gamelib.debug_write("is there a unit at coord({},{}): {}".format(loc[0],loc[1],game_state.contains_stationary_unit(loc)))
                gamelib.debug_write("is there a unit at coord({},{}): {}".format(loc[1],loc[0],game_state.contains_stationary_unit([loc[1],loc[0]])))
                total_monies -= worth
                gamelib.debug_write("After {} cores".format(total_monies))
                #gamelib.spawn("You have {} cores".format(game_state.get_resource(game_state.CORES)))



    def starter_strategy(self, game_state):
        """
        For defense we will use a spread out layout and some Scramblers early on.
        We will place destructors near locations the opponent managed to score on.
        For offense we will use long range EMPs if they place stationary units near the enemy's front.
        If there are no stationary units to attack in the front, we will send Pings to try and score quickly.
        """
        # First, place basic defenses
        self.build_defences(game_state)
        # Now build reactive defenses based on where the enemy scored
        self.build_reactive_defense(game_state)

        # If the turn is less than 5, stall with Scramblers and wait to see enemy's base
        if game_state.turn_number < 5:
            self.stall_with_scramblers(game_state)
        else:
            # Now let's analyze the enemy base to see where their defenses are concentrated.
            # If they have many units in the front we can build a line for our EMPs to attack them at long range.
            if self.detect_enemy_unit(game_state, unit_type=None, valid_x=None, valid_y=[14, 15]) > 10:
                self.emp_line_strategy(game_state)
            else:
                # They don't have many units in the front so lets figure out their least defended area and send Pings there.

                # Only spawn Ping's every other turn
                # Sending more at once is better since attacks can only hit a single ping at a time
                if game_state.turn_number % 2 == 1:
                    # To simplify we will just check sending them from back left and right
                    ping_spawn_location_options = [[13, 0], [14, 0]]
                    best_location = self.least_damage_spawn_location(game_state, ping_spawn_location_options)
                    game_state.attempt_spawn(PING, best_location, 1000)

                # Lastly, if we have spare cores, let's build some Encryptors to boost our Pings' health.
                encryptor_locations = [[13, 2], [14, 2], [13, 3], [14, 3]]
                game_state.attempt_spawn(ENCRYPTOR, encryptor_locations)

    def build_defences_bad(self, game_state):
        """
        Build basic defenses using hardcoded locations.
        Remember to defend corners and avoid placing units in the front where enemy EMPs can attack them.
        """
        # Useful tool for setting up your base locations: https://www.kevinbai.design/terminal-map-maker
        # More community tools available at: https://terminal.c1games.com/rules#Download

        # Place destructors that attack enemy units
        destructor_locations = [[0, 13], [27, 13], [8, 11], [19, 11], [13, 11], [14, 11]]
        # attempt_spawn will try to spawn units if we have resources, and will check if a blocking unit is already there
        game_state.attempt_spawn(DESTRUCTOR, destructor_locations)

        # Place filters in front of destructors to soak up damage for them
        filter_locations = [[8, 12], [19, 12]]
        game_state.attempt_spawn(FILTER, filter_locations)

    def build_reactive_defense(self, game_state):
        """
        This function builds reactive defenses based on where the enemy scored on us from.
        We can track where the opponent scored by looking at events in action frames
        as shown in the on_action_frame function
        """
        for location in self.scored_on_locations:
            # Build destructor one space above so that it doesn't block our own edge spawn locations
            build_location = [location[0], location[1]+1]
            game_state.attempt_spawn(DESTRUCTOR, build_location)

    def stall_with_scramblers(self, game_state):
        """
        Send out Scramblers at random locations to defend our base from enemy moving units.
        """
        # We can spawn moving units on our edges so a list of all our edge locations
        friendly_edges = game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_LEFT) + game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_RIGHT)

        # Remove locations that are blocked by our own firewalls
        # since we can't deploy units there.
        deploy_locations = self.filter_blocked_locations(friendly_edges, game_state)

        # While we have remaining bits to spend lets send out scramblers randomly.
        while game_state.get_resource(game_state.BITS) >= game_state.type_cost(SCRAMBLER) and len(deploy_locations) > 0:
            # Choose a random deploy location.
            deploy_index = random.randint(0, len(deploy_locations) - 1)
            deploy_location = deploy_locations[deploy_index]

            game_state.attempt_spawn(SCRAMBLER, deploy_location)
            """
            We don't have to remove the location since multiple information
            units can occupy the same space.
            """

    def emp_line_strategy(self, game_state):
        """
        Build a line of the cheapest stationary unit so our EMP's can attack from long range.
        """
        # First let's figure out the cheapest unit
        # We could just check the game rules, but this demonstrates how to use the GameUnit class
        stationary_units = [FILTER, DESTRUCTOR, ENCRYPTOR]
        cheapest_unit = FILTER
        for unit in stationary_units:
            unit_class = gamelib.GameUnit(unit, game_state.config)
            if unit_class.cost < gamelib.GameUnit(cheapest_unit, game_state.config).cost:
                cheapest_unit = unit

        # Now let's build out a line of stationary units. This will prevent our EMPs from running into the enemy base.
        # Instead they will stay at the perfect distance to attack the front two rows of the enemy base.
        for x in range(27, 5, -1):
            game_state.attempt_spawn(cheapest_unit, [x, 11])

        # Now spawn EMPs next to the line
        # By asking attempt_spawn to spawn 1000 units, it will essentially spawn as many as we have resources for
        game_state.attempt_spawn
        (EMP, [24, 10], 1000)

    def least_damage_spawn_location(self, game_state, location_options):
        """
        This function will help us guess which location is the safest to spawn moving units from.
        It gets the path the unit will take then checks locations on that path to
        estimate the path's damage risk.
        """
        damages = []
        # Get the damage estimate each path will take
        for location in location_options:
            path = game_state.find_path_to_edge(location)
            damage = 0
            for path_location in path:
                # Get number of enemy destructors that can attack the final location and multiply by destructor damage
                damage += len(game_state.get_attackers(path_location, 0)) * gamelib.GameUnit(DESTRUCTOR, game_state.config).damage
            damages.append(damage)

        # Now just return the location that takes the least damage
        return location_options[damages.index(min(damages))]

    def detect_enemy_unit(self, game_state, unit_type=None, valid_x = None, valid_y = None):
        total_units = 0
        for location in game_state.game_map:
            if game_state.contains_stationary_unit(location):
                for unit in game_state.game_map[location]:
                    if unit.player_index == 1 and (unit_type is None or unit.unit_type == unit_type) and (valid_x is None or location[0] in valid_x) and (valid_y is None or location[1] in valid_y):
                        total_units += 1
        return total_units

    def filter_blocked_locations(self, locations, game_state):
        filtered = []
        for location in locations:
            if not game_state.contains_stationary_unit(location):
                filtered.append(location)
        return filtered

    def on_action_frame(self, turn_string):
        """
        This is the action frame of the game. This function could be called
        hundreds of times per turn and could slow the algo down so avoid putting slow code here.
        Processing the action frames is complicated so we only suggest it if you have time and experience.
        Full doc on format of a game frame at: https://docs.c1games.com/json-docs.html
        """
        # Let's record at what position we get scored on
        state = json.loads(turn_string)
        events = state["events"]
        breaches = events["breach"]
        for breach in breaches:
            location = breach[0]
            unit_owner_self = True if breach[4] == 1 else False
            # When parsing the frame data directly,
            # 1 is integer for yourself, 2 is opponent (StarterKit code uses 0, 1 as player_index instead)
            if not unit_owner_self:
                gamelib.debug_write("Got scored on at: {}".format(location))
                self.scored_on_locations.append(location)
                gamelib.debug_write("All locations: {}".format(self.scored_on_locations))


if __name__ == "__main__":
    print("sup")
    algo = AlgoStrategy()
    algo.start()
