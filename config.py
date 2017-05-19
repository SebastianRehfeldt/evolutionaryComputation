### General ###
runs = 10
generations = 10000
pop_size = 150
prob_muta = 0.1
prob_cross = 0.0
tour_size = 3
elite_percent = 0.1

### Restart ####
should_restart = True
immigrant_perc = 0.9
restart_generations = 500 #100 #250 #500 #1000 #2000


### Cross-Over method (row or block)
cross_over = "row"


### FILES ###
file = ["sudoku_difficult_38.txt"]

#30 runs, 100k generations
final_file1 = ["sudoku_easy_38.txt"]
final_file2 = ["sudoku_medium_29.txt"]
final_file3 = ["sudoku_difficult_24.txt"]
final_file4 = ["sudoku_super_difficult_24.txt"]
final_file5 = ["sudoku_ai_escargot.txt"]



### Run multiple FILES at once ### 
test_files = ["sudoku_easy_38.txt",
			"sudoku_medium_30.txt",
			"sudoku_difficult_28.txt",
]

all_files = ["sudoku_easy_38.txt",
			"sudoku_easy_34.txt",
			"sudoku_medium_30.txt",
			"sudoku_medium_29.txt",
			"sudoku_difficult_28.txt",
			"sudoku_difficult_24.txt",
			"sudoku_super_difficult_24.txt",
			"sudoku_super_difficult_22.txt",
			"sudoku_ai_escargot.txt"
]
