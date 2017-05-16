** Experimental results

*** Run Instructions
To run the experiments run inside the root folder "python sudoku.py" and change the config to the values, you want to test, e.g. set the "prob_cross" to 0 to just evaluate the mutation. The results and plots will be written to files inside the experiments folder.

The final evaluation is based on 30 runs with 100k generations and all files. For development, the number of generations was decreased to 10k generations and only 3 files have been used.



*** Metrics
- Furthermore, it is measured how often the runs found the solution for the sudoku.
- Also the best and average generation for finding the solution are good metrics for the algorithm quality.


- The minimum and average number of conflicts after all generations are metrics used for evaluation. (final_conflicts.csv)
- A plot for the performance over generations can also be used for analysis.