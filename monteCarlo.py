import copy
import random
import time
import sys
import math
from collections import namedtuple

GameState = namedtuple('GameState', 'to_move, move, utility, board, moves')

# MonteCarlo Tree Search support

class MCTS:  # Monte Carlo Tree Search implementation
    class Node:
        def __init__(self, state, par=None):
            self.state = copy.deepcopy(state)
            self.parent = par
            self.children = []
            self.visitCount = 0
            self.winScore = 0

        def getChildWithMaxScore(self):                 #the current node (self) has no children
            maxScoreChild = max(self.children, key=lambda x: x.visitCount) if self.children else self
            return maxScoreChild

    def __init__(self, game, state):
        self.root = self.Node(state)
        self.state = state
        self.game = game
        self.exploreFactor = math.sqrt(2)

    def isTerminalState(self, utility, moves):
        return utility != 0 or len(moves) == 0

    def monteCarloPlayer(self, timelimit=4):
        """Entry point for Monte Carlo tree search"""
        start = time.perf_counter()
        end = start + timelimit

        while time.perf_counter() < end:
            # 1. Selection
            node = self.selectNode(self.root)
            # 2. Expansion
            if not self.game.terminal_test(node.state):
                self.expandNode(node)
                if node.children:
                    node_to_simulate = random.choice(node.children)
                else:
                    node_to_simulate = node
            else:
                node_to_simulate = node
            # 3. Simulation
            winningPlayer = self.simulateRandomPlay(node_to_simulate)
            # 4. Backpropagation
            self.backPropagation(node_to_simulate, winningPlayer)

        winnerNode = self.root.getChildWithMaxScore()
        assert(winnerNode is not None)
        return winnerNode.state.move

    """SELECT stage function. Walks down the tree using findBestNodeWithUCT()"""
    def selectNode(self, nd):
        node = nd
        while node.children:
            node = self.findBestNodeWithUCT(node)
        return node

    def findBestNodeWithUCT(self, nd):
        """Finds the child node with the highest UCT."""
        parentVisit = nd.visitCount
        uct_values = [(self.uctValue(parentVisit, child.winScore, child.visitCount), child) for child in nd.children]
        max_uct, best_child = max(uct_values, key=lambda x: x[0])
        return best_child

    def uctValue(self, parentVisit, nodeScore, nodeVisit):
        """Compute Upper Confidence Value for a node."""
        if nodeVisit == 0:
            return float('inf')
        return (nodeScore / nodeVisit) + self.exploreFactor * math.sqrt(math.log(parentVisit) / nodeVisit)

    """EXPAND stage function."""
    def expandNode(self, nd):
        """Generate all the possible child nodes and append them to nd's children."""
        stat = nd.state
        tempState = GameState(to_move=stat.to_move, move=stat.move, utility=stat.utility, board=stat.board, moves=stat.moves)
        for a in self.game.actions(tempState):
            childNode = self.Node(self.game.result(tempState, a), nd)
            nd.children.append(childNode)

    """SIMULATE stage function"""
    def simulateRandomPlay(self, nd):
        # First, check if current node is terminal
        winStatus = self.game.compute_utility(nd.state.board, nd.state.move, nd.state.board.get(nd.state.move, 'N'))
        if winStatus != 0:
            # Game has already been won at this node
            if winStatus > 0:
                return 'X'
            elif winStatus < 0:
                return 'O'
            else:
                return 'N'  # Tie

        tempState = copy.deepcopy(nd.state)

        # Now roll out the simulation
        while not self.game.terminal_test(tempState):
            player = tempState.to_move
            opponent = self.game.switchPlayer(player)

            # 1. Check if the current player can win in the next move
            winning_move = self.find_winning_move(tempState, player)
            if winning_move:
                tempState = self.game.result(tempState, winning_move)
                break

            # 2. Check if the opponent can win in their next move, and block them
            blocking_move = self.find_winning_move(tempState, opponent)
            if blocking_move:
                tempState = self.game.result(tempState, blocking_move)
            else:
                # 3. Otherwise, play randomly
                possible_moves = self.game.actions(tempState)
                action = random.choice(possible_moves)
                tempState = self.game.result(tempState, action)
            # No need to switch players manually; game.result handles it

        # Determine the winner after simulation
        utility = self.game.utility(tempState, self.state.to_move)
        if utility > 0:
            return 'X'
        elif utility < 0:
            return 'O'
        else:
            return 'N'  # Tie

    def find_winning_move(self, state, current_player):
        """Find if the current player can win in the next move."""
        for move in self.game.actions(state):
            next_state = self.game.result(state, move)
            if self.game.compute_utility(next_state.board, move, current_player) == self.game.k:
                return move
        return None

    def backPropagation(self, nd, winningPlayer):
        """Propagate upward to update score and visit count from
        the current leaf node to the root node."""
        tempNode = nd
        while tempNode is not None:
            tempNode.visitCount += 1
            node_player = self.game.switchPlayer(tempNode.state.to_move)
            if node_player == winningPlayer:
                tempNode.winScore += 1
            elif winningPlayer != 'N' and node_player == self.game.switchPlayer(winningPlayer):
                tempNode.winScore += 0.5  # Reward for blocking opponent
            tempNode = tempNode.parent
