## How to run the program
1. Run `binpacking_Main.py` with python of version 3.0 or above
2. input.txt will be opened automatically 
3. Feel free to make any changes in the inputs in the text file and save by going file > save or ctrl + s if you are on Windows
4. Close the file directly to continue the program
5. Steps 2 to 4 are skipped automatically if the program failed to open input.txt. You can still change the inputs by modifying the input.txt directly (open the input.txt using a text editor) when the program is not open.
6. If there is no issue, the program should display the progress of the algorithm one by one, then the visual look of the maze and the overall results.


## About input.txt
Only the inputs enclosed by `//////////\\\\\\\\\\` and `\\\\\\\\\\//////////` are read by the program, do not modify the enclosers. The location of the room in the maze is represented by coordinates, you can refer to the exampleMaze.png to understand how the coordinates are identified and structured. Left coordinate is the row and right coordinate is the column, for example (1,3) means row is 1 and column is 3.

## Format

### Size of the maze
To enter the size of the maze that the program can traverse.
Must contain only one input.  
>`//////////\\\\\\\\\\`  
(row,column)  
`\\\\\\\\\\//////////`  

### Rubbish Room Locations
To enter the locations of the rubbish rooms with its respective rubbish weight and volume.
Must contain at least one input and you can add more inputs.  
>`//////////\\\\\\\\\\`  
(row,column) : (weight,volume)  
(row,column) : (weight,volume)  
(row,column) : (weight,volume)  
`\\\\\\\\\\//////////`  

### Disposal Room Locations
To enter the locations of the disposal rooms.
Must contain at least one input and you can add more inputs.
>`//////////\\\\\\\\\\`  
(row,column)  
(row,column)  
(row,column)  
`\\\\\\\\\\//////////`  

### Obstacle Room Locations
Obstacle rooms cannot be accessed by the algorithm, they will be avoided in the path.
To enter the locations of the obstacle rooms.
Input is not required but you can add more inputs.
>`//////////\\\\\\\\\\`  
(row,column)  
(row,column)  
(row,column)  
`\\\\\\\\\\//////////`  

### Initial State/Room
To enter the starting location of the algorithm.
Must contain only one input.
>`//////////\\\\\\\\\\`  
(row,column)  
`\\\\\\\\\\//////////`  

### Weight and Volume limit
Must contain only two inputs which are weight limit and volume limit respectively.
>`//////////\\\\\\\\\\`  
weight limit  
volume limit  
`\\\\\\\\\\//////////`  