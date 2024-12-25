# TicTacToe with Adversarial Search

## Overview

This project is an implementation of the classic **TicTacToe game** enhanced with **Adversarial Search algorithms**, including:

- **MinMax**
- **MinMax with Alpha-Beta Pruning**
- **Monte Carlo Tree Search (MCTS)**

The game supports variable board sizes (e.g., 3x3, 4x4, 5x5) and allows players to play against an AI opponent. The AI's decision-making is based on the implemented algorithms, ensuring competitive gameplay.

## Features

1. **Flexible Gameplay**:

   - Adjustable board sizes.
   - Configurable win conditions (e.g., 3 in a row for 3x3, 4 in a row for 4x4).

2. **Adversarial Search Algorithms**:

   - **MinMax**: Exhaustive search to evaluate all possible moves.
   - **Alpha-Beta Pruning**: Optimized version of MinMax to skip irrelevant branches.
   - **Monte Carlo Tree Search (MCTS)**: Simulates games to estimate the best move.

3. **Customizable Time Limit**:

   - The AI’s search can be restricted by a timer to limit decision time.

4. **GUI with Tkinter**:

   - A user-friendly interface for gameplay.
   - Dropdown menu to select AI strategies.

## Requirements

- **Python 3.7+**
- Required libraries: `numpy`

Install the necessary libraries using pip:

```bash
pip install numpy
```

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/your-username/tictactoe-adversarial-search.git
cd tictactoe-adversarial-search
```

### Run the Game

Run the game with the default 3x3 board:

```bash
python main.py
```

To play with a different board size (e.g., 4x4):

```bash
python main.py 4
```

### How to Play

1. Launch the game to open the **Tkinter GUI**.
2. Select the AI strategy from the dropdown menu (Random, MinMax, AlphaBeta, or Monte Carlo).
3. Take your turn as **X** by clicking on a square.
4. The AI will make its move as **O**, based on the selected algorithm.
5. The game continues until there is a winner or a draw.

## Implementation Details

### Algorithms

#### MinMax

The MinMax algorithm searches the entire game tree to find the best move. It is ideal for smaller boards like 3x3.

#### Alpha-Beta Pruning

Alpha-Beta Pruning optimizes MinMax by skipping unnecessary branches, improving efficiency.

#### Monte Carlo Tree Search (MCTS)

MCTS simulates random games from the current state and backpropagates results to estimate the best move.

### Evaluation Function

For MinMax and Alpha-Beta with a cutoff depth, an evaluation function assesses the potential of a board state by:

- Counting lines where a player is close to completing the win condition.
- Weighing these potential wins to guide the AI’s decisions.

### Time Limit

The time limit restricts the AI's computation time per move. The AI uses iterative deepening to progressively explore deeper levels of the game tree within the allocated time.

#### How It Works

The time is measured in seconds and is applied in algorithms like MinMax with cutoff, AlphaBeta with cutoff, and Monte Carlo Tree Search.

When a positive time limit is set (e.g., timer = 5), the AI will:

1. Start its decision-making process.

2. Continue searching for the best move until the allotted time expires.

3. Return the best move found within the time limit, even if it hasn't fully explored all possible moves.

If the timer is set to -1, it means:

1. Unlimited time is allowed.

2. The AI will perform a complete search (to maximum depth or until the game is solved).

## File Structure

```
.
├── main.py          # Main script for the game and GUI
├── games.py         # Core game logic and adversarial search algorithms
├── monteCarlo.py    # Monte Carlo Tree Search implementation
├── utils.py         # Utility functions (optional)
```

## Example Gameplay

- **3x3 Board**: The AI should never lose and will always at least tie.
  ```
   python .\tic-tac-toe.py
  ```
- **4x4 Board**: The AI’s performance depends on the time limit and algorithm used.
  ```
  python .\tic-tac-toe.py 4
  ```
- **5x5 Board**:
  ```
  python .\tic-tac-toe.py 5
  ```

## Questions to Consider

1. Why might the AI sometimes exceed the set time limit?
   - The recursive nature of search algorithms may cause the AI to complete a deep branch before stopping.
2. How can this be resolved?
   - Check the timer at every node during the search.
   - Use iterative deepening to progressively refine the AI’s decisions within the time limit.

## Future Enhancements

- Add multiplayer mode.
- Improve the evaluation function for larger boards.
- Visualize the AI’s decision-making process.

## Assignment description
See the docx file for the assignment description


