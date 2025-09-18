# main.py
from strategy import RandomStrategy, StopAfterNOpensStrategy, BetterThanPercentStrategy, MaxAfterNStrategy
from tournament import (
    DeathMatchTournament,
    RoundRobinTournament,
    EliminationTournament,
    LeagueTournament,
    ChampionshipTournament
)


def main():
    # נגדיר את כל האסטרטגיות לשימוש בטורנירים
    strategies = [
        RandomStrategy(),
        StopAfterNOpensStrategy(),
        BetterThanPercentStrategy(),
        MaxAfterNStrategy()
    ]

    print("\n===================")
    print(" DeathMatch")
    print("===================")
    deathmatch = DeathMatchTournament([strategies[0], strategies[1]], win_goal=3)
    winner, log = deathmatch.run()

    print("\n===================")
    print(" Round Robin")
    print("===================")
    rr = RoundRobinTournament(strategies, rounds=2)
    table, log = rr.run()

    print("\n===================")
    print(" Elimination")
    print("===================")
    elim = EliminationTournament(strategies)
    winner, log = elim.run()

    print("\n===================")
    print(" League")
    print("===================")
    league = LeagueTournament(strategies)
    table, log = league.run()

    print("\n===================")
    print(" Championship")
    print("===================")
    champ = ChampionshipTournament(strategies, group_size=2)
    results, log = champ.run()


if __name__ == "__main__":
    main()
