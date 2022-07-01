import copy
import numpy as np
from player import Player
import math

class Evolution:
    def __init__(self):
        self.game_mode = "Neuroevolution"

    def roulette_wheel(self , players , num_player):
        _sum = sum([player.fitness for player in players])
        probability = [player.fitness / _sum for player in players]
        nex_generation = np.random.choice(players, size=num_player, p=probability)
        return nex_generation

    def SUS(self,  num_players, players):
        next_generation = []
        sum_e_g = np.sum([player.fitness for player in players]) 
        e_g = sum_e_g / num_players
        s = np.random.uniform(0, e_g, 1)
        points = [n * e_g + s for n in range(num_players)]
        for point in points:
            n = 0
            fitness = 0
            while fitness < point:
                fitness += players[n].fitness
                n += 1
            next_generation.append(players[n - 1])
        return next_generation

    def q_tournament(self, num_players, players, q):
        choose_players = []
        for i in range(num_players):
            random = np.random.choice(players, q)
            choose_players.append(max(random, key=lambda player: player.fitness))

        return choose_players
    
    def next_population_selection(self, players, num_players):
        """
        Gets list of previous and current players (μ + λ) and returns num_players number of players based on their
        fitness value.

        :param players: list of players in the previous generation
        :param num_players: number of players that we return
        """
        # TODO (Implement top-k algorithm here)
        # TODO (Additional: Implement roulette wheel here)
        # TODO (Additional: Implement SUS here)
        # TODO (Additional: Learning curve)
        #sort_list = sorted(players, key=lambda player: player.fitness, reverse=True)
        self.save(players)
        sort_list= self.q_tournament(num_players, players,25)
        return sort_list[: num_players]


    def save(self , players):
        
        sort_list = sorted(players, key=lambda player: player.fitness, reverse=True)
        max_ = sort_list[0].fitness
        min_ = sort_list[-1].fitness
        n = len([player.fitness for player in players])
        mean_ = (sum([player.fitness for player in players])) / n
        #save min max mean
        data = f"{mean_},{max_},{min_}\n"
        with open("json.rj", "a") as f:
            f.write(data)
        f.close()
        



    def crossover(self, parent1, parent2):
        crossover_prob = 0.7
        random_number = np.random.uniform(0, 1, 1)
        if random_number > crossover_prob:
            return parent1, parent2

        else:
            cross_place = math.floor(parent1.shape[0] / 2)
            child1_array = np.concatenate((parent1[:cross_place], parent2[cross_place:]), axis=0)
            child2_array = np.concatenate((parent2[:cross_place], parent1[cross_place:]), axis=0)
        return child1_array, child2_array
        
        
    def mutation(self, child):
        p_weight=0.2
        p_bios=0.6
        random_num = np.random.uniform(0, 1, 1)
        if random_num <= p_weight:
            child.nn.weight1 += np.random.normal(0, 0.3, child.nn.weight1.shape)
        if random_num <= p_weight:
            child.nn.weight2 += np.random.normal(0, 0.3, child.nn.weight2.shape)
        if random_num <= p_bios:
            child.nn.bayas1 += np.random.normal(0, 0.3, child.nn.bayas1.shape)
        if random_num <= p_bios:
            child.nn.bayas2 += np.random.normal(0, 0.3, child.nn.bayas2.shape)
        return child
        
        
        
   


    def generate_new_population(self, num_players, prev_players=None):
        """
        Gets survivors and returns a list containing num_players number of children.

        :param num_players: Length of returning list
        :param prev_players: List of survivors
        :return: A list of children
        """
        first_generation = prev_players is None
        if first_generation:
            return [Player(self.game_mode) for _ in range(num_players)]
        else:
            
            new_players_parents =  self.SUS(num_players  ,prev_players)
            #new_players_parents =  self.q_tournament( num_players  ,prev_players, 25)
            children = []
            for i in range( 0, len(new_players_parents) , 2) :
                parent1_mom = new_players_parents[i]
                parent2_dad = new_players_parents[i+1]
                clone_child1 = self.clone_player(parent1_mom)
                clone_child2 = self.clone_player(parent2_dad)
                clone_child1.nn.weight1 ,  clone_child2.nn.weight1 = self.crossover(parent1_mom.nn.weight1 , parent2_dad.nn.weight1)
                clone_child1.nn.weight2 , clone_child2.nn.weight2  = self.crossover(parent1_mom.nn.weight2 , parent2_dad.nn.weight2)
                clone_child1.nn.bayas1, clone_child2.nn.bayas1 = self.crossover(parent1_mom.nn.bayas1, parent2_dad.nn.bayas1)
                clone_child1.nn.bayas2, clone_child2.nn.bayas2 = self.crossover(parent1_mom.nn.bayas2, parent2_dad.nn.bayas2)
                clone_child1 = self.mutation(clone_child1 )
                clone_child2 = self.mutation(clone_child2 )
                children.append(clone_child1)
                children.append(clone_child2)

            return children



    def clone_player(self, player):
        """
        Gets a player as an input and produces a clone of that player.
        """
        new_player = Player(self.game_mode)
        new_player.nn = copy.deepcopy(player.nn)
        new_player.fitness = player.fitness
        return new_player
