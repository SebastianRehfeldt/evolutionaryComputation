# Solving the Sudoku Puzzle using an Evolutionary Algorithm

This project was done as a student work for a course at the University of Coimbra


## Goals of Assignment

"Search for evolutionary algorithms that solve this problem. Implement at least two variants, and analyze statistically their performance. You may use others proposals (and code), but we will valorize positively your own solution."


## Test Cases & Evaluation

The project uses sudokus from the following paper:
https://www.researchgate.net/publication/224180108_Solving_Sudoku_with_genetic_operations_that_preserve_building_blocks

Measurements:
- best, average generation when solution was found
- best, average conflicts after fixed number of generations
- plot for performance over runs


## Implementation

### Representation
- 2D chromosome

### Cross-over
- block or row swap cross-over
- givens are swapped to original places afterwards
- sub-blocks were transformed into valid permutations in case duplicated numbers exist

### Mutation
- for each sub-block: swap non-given numbers

### Random Immigrants
- as the algorithm often gets stuck in local optima, the population is refreshed with new individuals after a certain amount of generation without improvement

### Variants
- Mutation only
- Mutation + Cross-over (swap blocks or rows)
- Random Immigrants

## Run instructions
- run "python sudoku.py" in this folder
- change in "sudoku.py" and "utils.py" the file names how results should be saved
- change also the selection of test files here
- should be changed to a approach where less manual modifications would be necessary
- adjust configuration to switch approaches, files and to decrease number of runs/ generations for development
- experimental results and setup descriptions are inside the "experiments" folder

## Related Papers
- Solving, Rating and Generating Sudoku Puzzles with GA - Timo Mantere and Janne Koljonen
- Solving Sudoku with Genetic Operations that Preserve Building Blocks - Yuji Sato, Member, IEEE, and Hazuki Inoue
- Product Geometric Crossover for the Sudoku Puzzle - Alberto Moraglio, Julian Togelius, Simon Lucas