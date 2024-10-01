    
# Restaurant 1 is regular
# Restaurant 2 is fancy

from typing import override

# Base class for all strategies
class Strategy:
    
    def name(self) -> str:
        raise NotImplementedError

    def action(self, my_moves: list[int], other_moves: list[int]) -> int:
        raise NotImplementedError
    
class Escape(Strategy):

    @override
    def name(self) -> str:
        return "Escape"

    @override
    def action(self, my_moves: list[int], other_moves: list[int]) -> int:
        if my_moves[-1] == other_moves[-1]:
            if my_moves[-1] == 1:
                return 2
            else: 
                return 1
        return my_moves[-1] 

class Follow(Strategy):

    @override
    def name(self) -> str:
        return "Follow"

    @override
    def action(self, my_moves: list[int], other_moves: list[int]) -> int:

        if my_moves[-1] == 1 and my_moves[-1] !=  other_moves[-1]:
            return 2 
            
        if my_moves[-1] == 2 and my_moves[-1] !=  other_moves[-1]:
            return 1
            
        return my_moves[-1] 

class AlwaysSame1(Strategy):
    
    @override
    def name(self) -> str:
        return "AlwaysSame1"

    @override
    def action(self, my_moves: list[int], other_moves: list[int]) -> int:
        return 1
    
class AlwaysSame2(Strategy):

    @override
    def name(self) -> str:
        return "AlwaysSame2"

    @override
    def action(self, my_moves: list[int], other_moves: list[int]) -> int:
        return 2
    
class Flipflop(Strategy):

    @override
    def name(self) -> str:
        return "Flipflop"

    @override
    def action(self, my_moves: list[int], other_moves: list[int]) -> int:
        
        if my_moves[-1] == 1:
            return 2
        return 1

class TwoInARow(Strategy):

    @override
    def name(self) -> str:
        return "TwoInARow"

    @override
    def action(self, my_moves: list[int], other_moves: list[int]) -> int:
        if len(my_moves) > 1:
            if my_moves[-1] == my_moves[-2] and my_moves[-1] == 1:
                return 2
            elif my_moves[-1] == my_moves[-2] and my_moves[-1] == 2:
                return 1
            return my_moves[-1]
        return my_moves[-1]
         
class TwoRegularOneFancy(Strategy):

    @override
    def name(self) -> str:
        return "TwoRegularOneFancy"

    @override
    def action(self, my_moves: list[int], other_moves: list[int]) -> int:
        if len(my_moves) > 1:
            if my_moves[-1] == 1 and my_moves[-2] == 1:
                return 2
            elif my_moves[-1] == 2:
                return 1
            elif my_moves[-1] == 1 and my_moves[-2] == 2:
                return 1 
        return my_moves[-1]
    
class TwoFancyOneRegular(Strategy):

    @override
    def name(self) -> str:
        return "TwoFancyOneRegular"

    @override
    def action(self, my_moves: list[int], other_moves: list[int]) -> int:
        if len(my_moves) > 1:
            if my_moves[-1] == 2 and my_moves[-2] == 2:
                return 1
            elif my_moves[-1] == 1:
                return 2
            elif my_moves[-1] == 2 and my_moves[-2] == 1:
                return 2
        return my_moves[-1]
    
class TwoChanceEscape(Strategy):
    
    @override
    def name(self) -> str:
        return "TwoChanceEscape"

    @override
    def action(self, my_moves: list[int], other_moves: list[int]) -> int:
        if len(my_moves) > 1:
            if my_moves[-1] == other_moves[-1] and my_moves[-2] == other_moves[-2]:
                if my_moves[-1] == 1:
                    return 2
                else: 
                    return 1
            return my_moves[-1]
        return my_moves[-1]

class BayesianFollow(Strategy):
        
    @override
    def name(self) -> str:
        return "BayesianFollow"
    
    def bayesTheorem(self, event: int, given_event: int, other_moves: list[int]) -> float:
        
        p_other_choose_1 = other_moves.count(event) / max(len(other_moves),1)

        p_other_choose_2 = other_moves.count(given_event) / max(len(other_moves),1)

        # Divide list into pairs
        pairs = [(other_moves[i], other_moves[i-1]) for i in range(1, len(other_moves))]

        # Count the number of times the pair (2, 1) occurs
        p_my_choose_2_given_1 = pairs.count((given_event, event)) / max(len(pairs),1)

        return (p_my_choose_2_given_1 * p_other_choose_1 / max(p_other_choose_2, 1))

    @override
    def action(self, my_moves: list[int], other_moves: list[int]) -> int:
        
        last_move = other_moves[-1]

        prob_other_choose_1 = self.bayesTheorem(1, last_move, other_moves)

        prob_other_choose_2 = self.bayesTheorem(2, last_move, other_moves)

        return 1 if prob_other_choose_1 > prob_other_choose_2 else 2

class BayesianEscape(BayesianFollow):

    @override
    def name(self) -> str:
        return "BayesianEscape"
    
    @override
    def action(self, my_moves: list[int], other_moves: list[int]) -> int:

        last_move = my_moves[-1]

        prob_other_choose_1 = self.bayesTheorem(1, last_move, other_moves)

        prob_other_choose_2 = self.bayesTheorem(2, last_move, other_moves)

        return 1 if prob_other_choose_1 < prob_other_choose_2 else 2

class Round:
    
    def __init__(self, a: Strategy, b: Strategy):
        self.a = a
        self.b = b
        self.a_moves= []
        self.b_moves = []

    def run(self, n: int, a_start: int, b_start: int) -> None:
        
        self.a_moves.append(a_start)

        self.b_moves.append(b_start)

        for _ in range(0, n):
            
            a_moves_before = self.a_moves.copy()

            self.a_moves.append(self.a.action(self.a_moves, self.b_moves))
            
            self.b_moves.append(self.b.action(self.b_moves, a_moves_before))

    def results(self) -> int:
        
        time_spent_together = 0

        for a_loc, b_loc in zip(self.a_moves, self.b_moves):

            if a_loc == b_loc:
                
                if a_loc == 1:

                    time_spent_together += 20

                elif a_loc == 2:
                    
                    time_spent_together += 50

        return time_spent_together

a_strategies: list[Strategy] = [
    AlwaysSame1(),
    AlwaysSame2(),
    Flipflop(),
    TwoInARow(),
    TwoRegularOneFancy(),
    TwoFancyOneRegular(),
    TwoChanceEscape(),
    Escape(),
    Follow(),
    BayesianFollow(),
    BayesianEscape()
]

b_strategies: list[Strategy] = [
    AlwaysSame1(),
    AlwaysSame2(),
    Flipflop(),
    TwoInARow(),
    TwoRegularOneFancy(),
    TwoFancyOneRegular(), 
    TwoChanceEscape(),
    Escape(),
    Follow(),
    BayesianFollow(),
    BayesianEscape()
]

strategy_names: list[str] = [strategy.name() for strategy in a_strategies]

class StrategyTournament:

    def run(self, a_start: int, b_start: int, ticks: int) -> None:
    
        rounds = []

        # Run rounds where all strategies play against each other
        for a in a_strategies:

            for b in b_strategies:

                tournament_round = Round(a, b)
                
                tournament_round.run(ticks, a_start, b_start)

                # Print every round
                print(f"{a.name()} vs {b.name()} = {tournament_round.results()}")

                rounds.append((tournament_round.results(), a.name(), b.name()))

        # Get the total time spent for each strategy a uses
        time_spent_per_strategy_a = []
        
        for name in strategy_names:

            rounds_with_strat = [round for round in rounds if round[1] == name]

            time_spent = sum(round[0] for round in rounds_with_strat)

            time_spent_per_strategy_a.append((name, time_spent))

        # Get the total time spent for each strategy b uses
        time_spent_per_strategy_b = []
        
        for name in strategy_names:

            rounds_with_strat = [round for round in rounds if round[2] == name]

            time_spent = sum(round[0] for round in rounds_with_strat)

            time_spent_per_strategy_b.append((name, time_spent))

        # Print the total time spent for each strategy choice by a and b
        print("\nTotal time spent togheter when A choose strategy:")

        time_spent_per_strategy_a.sort(key=lambda x: x[1])

        for strategy, time in time_spent_per_strategy_a:

            print(f"{strategy} : {time}")

        print("\nTotal time spent togheter when B choose strategy:")

        time_spent_per_strategy_b.sort(key=lambda x: x[1], reverse=True)

        for strategy, time in time_spent_per_strategy_b:
                
            print(f"{strategy} : {time}")

tournament = StrategyTournament()

tournament.run(1, 2, 1000)

            
        
        
