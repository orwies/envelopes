import random
from game_class import Game, GameResult
from strategy import RandomStrategy, StopAfterNOpensStrategy, BetterThanPercentStrategy, MaxAfterNStrategy


class Tournament:
    """
    Base tournament class
    """
    def __init__(self, strategies):
        self.strategies = strategies
        self.log = []

    def run(self):
        raise NotImplementedError("Must implement run() in subclass")


class DeathMatchTournament(Tournament):
    """
    Two strategies, first to X wins
    """
    def __init__(self, strategies, win_goal=3):
        super().__init__(strategies)
        self.win_goal = win_goal

    def run(self):
        wins = {s.__class__.__name__: 0 for s in self.strategies}
        round_num = 1
        while max(wins.values()) < self.win_goal:
            print(f"\n--- Round {round_num} ---")
            results = [Game.start_game(s) for s in self.strategies]
            chosen_values = [r._GameResult__chosen_value for r in results]

            if chosen_values[0] > chosen_values[1]:
                winner = self.strategies[0].__class__.__name__
            elif chosen_values[1] > chosen_values[0]:
                winner = self.strategies[1].__class__.__name__
            else:
                winner = None

            if winner:
                wins[winner] += 1
                print(f"Winner: {winner}")
            else:
                print("Draw")

            self.log.append((round_num, chosen_values, winner))
            round_num += 1

        final_winner = max(wins, key=wins.get)
        print(f"\nDeathMatch Winner: {final_winner}")
        return final_winner, self.log


class RoundRobinTournament(Tournament):
    """
    All vs All for N rounds
    """
    def __init__(self, strategies, rounds=2):
        super().__init__(strategies)
        self.rounds = rounds

    def run(self):
        points = {s.__class__.__name__: 0 for s in self.strategies}
        for i in range(len(self.strategies)):
            for j in range(i + 1, len(self.strategies)):
                for r in range(self.rounds):
                    s1, s2 = self.strategies[i], self.strategies[j]
                    res1 = Game.start_game(s1)
                    res2 = Game.start_game(s2)
                    v1, v2 = res1._GameResult__chosen_value, res2._GameResult__chosen_value
                    if v1 > v2:
                        points[s1.__class__.__name__] += 3
                        winner = s1.__class__.__name__
                    elif v2 > v1:
                        points[s2.__class__.__name__] += 3
                        winner = s2.__class__.__name__
                    else:
                        points[s1.__class__.__name__] += 1
                        points[s2.__class__.__name__] += 1
                        winner = None
                    self.log.append(((s1.__class__.__name__, s2.__class__.__name__), (v1, v2), winner))
                    print(f"{s1.__class__.__name__} vs {s2.__class__.__name__}: Winner = {winner}")
        print("\nFinal Points:", points)
        return points, self.log


class EliminationTournament(Tournament):
    """
    Single elimination bracket
    """
    def run(self):
        players = self.strategies[:]
        round_num = 1
        while len(players) > 1:
            print(f"\n--- Round {round_num} ---")
            next_round = []
            random.shuffle(players)
            if len(players) % 2 == 1:
                bye = players.pop()
                print(f"{bye.__class__.__name__} gets a bye")
                next_round.append(bye)
            for i in range(0, len(players), 2):
                s1, s2 = players[i], players[i+1]
                res1, res2 = Game.start_game(s1), Game.start_game(s2)
                v1, v2 = res1._GameResult__chosen_value, res2._GameResult__chosen_value
                winner = s1 if v1 >= v2 else s2
                print(f"{s1.__class__.__name__} vs {s2.__class__.__name__} → Winner: {winner.__class__.__name__}")
                self.log.append((s1.__class__.__name__, s2.__class__.__name__, winner.__class__.__name__))
                next_round.append(winner)
            players = next_round
            round_num += 1
        final_winner = players[0].__class__.__name__
        print(f"\nElimination Winner: {final_winner}")
        return final_winner, self.log


class LeagueTournament(Tournament):
    """
    Full league (home and away)
    """
    def run(self):
        table = {s.__class__.__name__: {"games": 0, "wins": 0, "losses": 0, "points": 0} for s in self.strategies}
        for i in range(len(self.strategies)):
            for j in range(i + 1, len(self.strategies)):
                for _ in range(2):  # home and away
                    s1, s2 = self.strategies[i], self.strategies[j]
                    res1, res2 = Game.start_game(s1), Game.start_game(s2)
                    v1, v2 = res1._GameResult__chosen_value, res2._GameResult__chosen_value
                    table[s1.__class__.__name__]["games"] += 1
                    table[s2.__class__.__name__]["games"] += 1
                    if v1 > v2:
                        table[s1.__class__.__name__]["wins"] += 1
                        table[s2.__class__.__name__]["losses"] += 1
                        table[s1.__class__.__name__]["points"] += 3
                        winner = s1
                    elif v2 > v1:
                        table[s2.__class__.__name__]["wins"] += 1
                        table[s1.__class__.__name__]["losses"] += 1
                        table[s2.__class__.__name__]["points"] += 3
                        winner = s2
                    else:
                        table[s1.__class__.__name__]["points"] += 1
                        table[s2.__class__.__name__]["points"] += 1
                        winner = None
                    print(f"{s1.__class__.__name__} vs {s2.__class__.__name__} → Winner: {winner.__class__.__name__ if winner else 'Draw'}")
        print("\nFinal League Table:")
        for team, stats in table.items():
            print(team, stats)
        return table, self.log


class ChampionshipTournament(Tournament):
    """
    Groups + playoffs
    """
    def __init__(self, strategies, group_size=2):
        super().__init__(strategies)
        self.group_size = group_size

    def run(self):
        random.shuffle(self.strategies)
        groups = [self.strategies[i:i+self.group_size] for i in range(0, len(self.strategies), self.group_size)]
        print("\n--- Group Stage ---")
        group_results = {}
        qualifiers = []
        for idx, group in enumerate(groups):
            print(f"\nGroup {idx+1}: {[s.__class__.__name__ for s in group]}")
            table = {s.__class__.__name__: 0 for s in group}
            for i in range(len(group)):
                for j in range(i+1, len(group)):
                    s1, s2 = group[i], group[j]
                    res1, res2 = Game.start_game(s1), Game.start_game(s2)
                    v1, v2 = res1._GameResult__chosen_value, res2._GameResult__chosen_value
                    if v1 > v2:
                        table[s1.__class__.__name__] += 3
                        winner = s1
                    elif v2 > v1:
                        table[s2.__class__.__name__] += 3
                        winner = s2
                    else:
                        table[s1.__class__.__name__] += 1
                        table[s2.__class__.__name__] += 1
                        winner = None
                    print(f"{s1.__class__.__name__} vs {s2.__class__.__name__} → {winner.__class__.__name__ if winner else 'Draw'}")
            group_results[f"Group {idx+1}"] = table
            top2 = sorted(table.items(), key=lambda x: x[1], reverse=True)[:2]
            qualifiers.extend([s for s, _ in top2])
        print("\n--- Playoffs ---")
        while len(qualifiers) > 1:
            next_round = []
            for i in range(0, len(qualifiers), 2):
                s1_name, s2_name = qualifiers[i], qualifiers[i+1]
                s1 = next(s for s in self.strategies if s.__class__.__name__ == s1_name)
                s2 = next(s for s in self.strategies if s.__class__.__name__ == s2_name)
                res1, res2 = Game.start_game(s1), Game.start_game(s2)
                v1, v2 = res1._GameResult__chosen_value, res2._GameResult__chosen_value
                winner = s1 if v1 >= v2 else s2
                print(f"{s1_name} vs {s2_name} → Winner: {winner.__class__.__name__}")
                next_round.append(winner.__class__.__name__)
            qualifiers = next_round
        print(f"\nChampionship Winner: {qualifiers[0]}")
        return {"groups": group_results, "winner": qualifiers[0]}, self.log
