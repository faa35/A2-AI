
import copy
import random
import time
import sys
import math
from collections import namedtuple
#import numpy as np

GameState = namedtuple('GameState', 'to_move, move, utility, board, moves')

# MonteCarlo Tree Search support

class MCTS: #Monte Carlo Tree Search implementation
    class Node:
        def __init__(self, state, par=None):
            self.state = copy.deepcopy(state)

            self.parent = par
            self.children = []
            self.visitCount = 0
            self.winScore = 0

        def getChildWithMaxScore(self):
            maxScoreChild = max(self.children, key=lambda x: x.visitCount)
            return maxScoreChild



    def __init__(self, game, state):
        self.root = self.Node(state)
        self.state = state
        self.game = game
        self.exploreFactor = math.sqrt(2)

    def isTerminalState(self, utility, moves):
        return utility != 0 or len(moves) == 0
    def monteCarloPlayer(self, timelimit = 4):
        """Entry point for Monte Carlo tree search"""
        start = time.perf_counter()
        end = start + timelimit
        """
        Use time.perf_counter() above to apply iterative deepening strategy.
         At each iteration we perform 4 stages of MCTS: 
         SELECT, EXPEND, SIMULATE, and BACKUP. Once time is up
        we use getChildWithMaxScore() to pick the node to move to
        """
        while time.perf_counter() < end:
            leaf_node = self.selectNode(self.root)  # SELECT stage
            self.expandNode(leaf_node)  # EXPAND stage
            result = self.simulateRandomPlay(leaf_node)  # SIMULATE stage
            self.backPropagation(leaf_node, result)  # BACK-PROPAGATE stage

        """below, expandNode() only adds children to leaf_node without returning a specific child. 
        As still working with leaf_node after the expansion.Simulate stage is run on the leaf_node (so has more children, but  simulation still uses the leaf_node). 
        So, calling self.simulateRandomPlay(leaf_node), the simulation runs from the leaf_node. 
        and then propagate the result back from this leaf_node."""

        winnerNode = self.root.getChildWithMaxScore()
        assert(winnerNode is not None)
        return winnerNode.state.move



    """Changed "nd" variable to "node" for better readability"""




    """SELECT stage function. walks down the tree using findBestNodeWithUCT()"""
    def selectNode(self, node):
        while node.children:
            node = self.findBestNodeWithUCT(node)
        return node

    
    def findBestNodeWithUCT(self, node):
        return max(node.children, key=lambda child: self.uctValue(node.visitCount, child.winScore, child.visitCount))

    def uctValue(self, parentVisitCount, nodeWinScore, nodeVisitCount):
        if nodeVisitCount == 0:
            return 0 if self.exploreFactor == 0 else sys.maxsize
        return (nodeWinScore / nodeVisitCount) + self.exploreFactor * math.sqrt(math.log(parentVisitCount) / nodeVisitCount)

    """EXPAND stage function. """
    def expandNode(self, node):
        """generate all the possible child nodes and append them to nd's children"""
        stat = node.state
        tempState = GameState(to_move=stat.to_move, move=stat.move, utility=stat.utility, board=stat.board, moves=stat.moves)
        for a in self.game.actions(tempState):
            childNode = self.Node(self.game.result(tempState, a), node)
            node.children.append(childNode)

    """SIMULATE stage function"""
    def simulateRandomPlay(self, node):
        # first use compute_utility() to check win possibility for the current node. IF so, return the winner's symbol X, O or N representing tie
        winStatus = self.game.compute_utility(node.state.board, node.state.move, node.state.board[node.state.move])
        if winStatus == self.game.k:
            assert(node.state.board[node.state.move] == 'X')
            if node.parent is not None:
                node.parent.winScore = -sys.maxsize
            return 'X' if winStatus > 0 else 'O'

        tempState = copy.deepcopy(node.state) # to be used in the following random playout
        to_move = tempState.to_move
        while not self.isTerminalState(tempState.utility, tempState.moves):
            move = random.choice(tempState.moves)
            tempState = self.game.result(tempState, move)

        # determine the result of the random playout
        winStatus = self.game.compute_utility(tempState.board, tempState.move, tempState.board[tempState.move])
        if winStatus == self.game.k:
            return 'X' if tempState.board[tempState.move] == 'X' else 'O'
        else:
            return 'N'  # 'N' means tie


    def backPropagation(self, node, winningPlayer):
        """propagate upword to update score and visit count from
        the current leaf node to the root node."""
        
        while node is not None:
            node.visitCount += 1
            if node.state.to_move != winningPlayer:
                node.winScore += 1
            node = node.parent
