#Import statements
import random
import argparse
import time

class Dice:
    '''Random Dice for the game with 6 sides'''
    def __init__(self, seed):
        random.seed(seed)

    def roll(self):
        return random.randrange(1, 6)


class Player:
    '''PLayer class'''
    def __init__(self, name):
        self.name = name
        self.Score = 0
        self.winner = 0


class Computer_Player(Player):
    '''Computer player class that inherits from Player'''
    def __init__(self, name):
        Player.__init__(self, name)
        self.type = "Computer"

    def decision(self, turn_total):
        #Uses logic and sets continue turn value for computer
        print(f"Computer Turn:{self.name}")
        print(f"current turn total: {turn_total}")
        print(f"Total Game Score is: {self.Score}")
        print("Enter r to roll, or h to hold")
        #the computer will hold at the lesser of 25 and 100 - x
        if turn_total < min(25, 100 - self.Score):
            return 1
        else:
            return 0

class Human_Player(Player):
    """Human Play class that inherits from Player"""
    def __init__(self, name):
        Player.__init__(self, name)
        self.type = "Human"

    def decision(self, turn_total):
        print(f"Player:{self.name}")
        print(f"current turn total: {turn_total}")
        print(f"Total Game Score is: {self.Score}")
        print("Enter r to roll, or h to hold")
        choice = input()
        if choice == "h":
            return 0
        if choice == "r":
            return 1


class Factory:
    '''Factory class to create a player, either Human or Computer'''
    def createPlayer(name, t):
        if t == "H":
            return Human_Player(name)
        if t == "C":
            return Computer_Player(name)


class Game:
    '''Pig Game Class'''
    def __init__(self, playerTypes):
        self.playerTypes = playerTypes
        self.people = []
        self.die = Dice(0)
        self.winningscore = 100

    def nextTurn(self, player):
        print(f"**********End of turn total: {self.turn(player)}**********")

    def assignPlayers(self):
        self.people.append(Factory.createPlayer("Player1", self.playerTypes.player1))
        self.people.append(Factory.createPlayer("Player2", self.playerTypes.player2))

    def turn(self, player):
        turn_total = 0
        while 1:
            if player.decision(turn_total):
                roll = self.die.roll()
                print(f"Rolled a {roll}")
                if roll != 1:
                    turn_total += roll
                    if player.Score + turn_total >= self.winningscore:
                        player.winner = 1
                        player.Score += turn_total
                        return player.Score
                else:
                    turn_total = 0
                    return 0
            else:
                player.Score += turn_total
                return player.Score

    def playGame(self):
        self.assignPlayers()
        while self.people[0].winner!= 1 and self.people[1].winner!=1:
            for player in self.people:
                self.nextTurn(player)
                if self.people[0].winner == 1 or self.people[1].winner == 1:
                    break
        self.printWinner()
        return

    def printWinner(self):
        player1score = self.people[0].Score
        player2score = self.people[1].Score

        if player1score > player2score:
            print(f"The winner is: {self.people[0].name}")
        if player2score > player1score:
            print(f"The winner is: {self.people[1].name}")
        return




class TimedGameProxy(Game):
    '''Timed Game Version that inherits from Game'''
    def __init__(self, args):
        Game.__init__(self, args)
        self.starttime = time.time()
        self.gametime = 60

    #Overload printWinner, considerations for there being a tie with timed verseion
    def printWinner(self):
        player1score = self.people[0].Score
        player2score = self.people[1].Score

        if player1score > player2score:
            self.people[0].winner = 1
            return self.people[0].name
        if player2score > player1score:
            self.people[1].winner = 1
            return self.people[1].name
        else:
            self.people[0].winner = 1
            self.people[1].winner = 1
            return "It's a tie!"

    #Overload turn, considerations for timed game
    def turn(self, player):
        turn_total = 0
        while 1:
            print((time.time() - self.starttime) >= self.gametime)
            if (time.time() - self.starttime) >= self.gametime:
                print("***** OUT OF TIME ****")
                print(f"The winner is: {self.printWinner()}")
                return 1
            else:
                if player.decision(turn_total):
                    roll = self.die.roll()
                    print(f"Rolled a {roll}")
                    if roll != 1:
                        turn_total += roll
                        if player.Score + turn_total >= self.winningscore:
                            player.winner = 1
                            player.Score += turn_total
                            return player.Score
                    else:
                        turn_total = 0
                        return 0
                else:
                    player.Score += turn_total
                    return player.Score


def main(args):
    if args.timed == 'Y':
        print("Going to time")
        TimedGameProxy(args).playGame()
    else:
        Game(args).playGame()



if __name__ == '__main__':
    '''Main Entry Point'''
    parser = argparse.ArgumentParser()
    parser.add_argument("--player1", help="H/C Human or Computer", type=str, required=True)
    parser.add_argument("--player2", help="H/C Human or Computer", type=str, required=True)
    parser.add_argument("--timed", help="Yes (Y)/No (N) to play timed version", type=str, required=True)
    args = parser.parse_args()
    main(args)