# GridDroid
Programmatically solving an old puzzle game

## The Game
Grid Droid is a relatively simple android app that supposedly came out late 2011. Since then, I have changed phones twice, but kept my old HTC Droid Incredible 2, with Grid Droid still installed on it.
I love this for a few reasons:
  * Simple puzzles that can be very hard to solve
  * Very quick and responsive user interface
  * 
### Rules
Grid Droid is a game with three difficulties: easy, medium, and hard. On the easy difficulty, all connectors are the same color (red). As you move on to harder difficulties, the game adds another color to the mix.
The board is a 4x5 grid of pieces. A piece may be a blank piece, or have up to 4 connections. In the code, I represent this as North, East, South, and West. You cannot rotate pieces.
You can swap two pieces by dragging one into another. To complete a puzzle, one must connect all the pieces together with respect to color.

## Solving the Game
I started with a list of Pieces and a State. The Pieces are a list of pieces that have not been placed yet, and the State is the current layout of the board. Now, this differs from the game on the phone, as you don't swap pieces between locations. This was done to make the puzzle easier to solve, and it doesnt change the solutions to the puzzle.

I first tried a Depth-First-Search. I created a board that was mostly empty pieces, except for two single connectors. I had high hopes that this would work, but there are many combinations of pieces (around 20 factorial, 2.4e18). The solver got stuck in switching around the blank pieces, when the original connectors were not placed well in the first place. It was recursing down paths that had no chance of being solutions.

## Last Notes

Please excuse the spaghetti code, I am still working on making things better.
