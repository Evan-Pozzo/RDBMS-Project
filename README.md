This code utilizes an array called tableArray that is full of Table objects for each table created in the program.
Each Table includes an array for the table's primary key, candidate keys, data columns, and an array of functionalDependencies objects. 
Each functionalDependencies object includes an array representing the determinant, an array representing the dependent, and a boolean value that specifies if the dependency is an MVD.

The format I use for taking input is in testInput.txt. starting the program and then copying the contents of the text file into the terminal should be all you need to get the code to run.
