# Solving the Sudoku Puzzle using an Evolutionary Algorithm

This project was done as a student work for a course at the University of Coimbra


## Goals of Assignment

"Search for evolutionary algorithms that solve this problem. Implement at least two variants, and analyze statistically their performance. You may use others proposals (and code), but we will valorize positively your own solution."


## Test Cases & Evaluation

The algorithm is tested on Suduko puzzles of different orders which can be found here:
http://www.ee.cityu.edu.hk/~rcheung/FPT/FPT09/comp/benchmarks.html

Consult also examples from:
https://www.researchgate.net/publication/224180108_Solving_Sudoku_with_genetic_operations_that_preserve_building_blocks

Measurements:
- generation when optimal solution was found
- conflicts after some fixed generations or time
- runtime


## Implementation

### Representation
- 2D chromosome

### Cross-over
- uniform, one-point, two-points cross-over on whole sub-blocks (points are limited to links between sub-blocks)
- How about fixed initial points? - fix later by random swap in sub-block, not allow to change

### Mutation
- for each sub-block: swap non-fixed integers


## Variants
- Simple as described above
- More complex operators: maybe forbid incorrect mutations which create duplicates in columns or rows
- add restart

## Related Papers
- Solving, Rating and Generating Sudoku Puzzles with GA - Timo Mantere and Janne Koljonen
- Solving Sudoku with Genetic Operations that Preserve Building Blocks - Yuji Sato, Member, IEEE, and Hazuki Inoue
- Product Geometric Crossover for the Sudoku Puzzle - Alberto Moraglio, Julian Togelius, Simon Lucas