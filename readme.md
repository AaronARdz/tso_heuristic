# Welcome to my final project of Selected topics of optimization!


# Instances
The instances are available in the root of the project folder.

## Create Datasets

New datasets can be created with the  **define_dataset(number_of_subsets, columns, album_size, rangen, name)**
function in the main.py file, to create new datasets, define the number of datasets, columns, album_size, range of numbers and name, the number of datasets should be greater than the album and the range of numbers.
## Switch to another file

All your files and folders are presented as a tree in the file explorer. You can switch from one to another by clicking a file in the tree.

## Run the program
Go to branch =  final-grasp in ca

To run the program simply declare the  **grasp(name, k, alpha)** function inside the main function in main.py
User  **solver.set_k_best(True)**  or   **solver.set_alpha(True)**  depending on the type of solution you want: 
def grasp(name, k, alpha):
name = the name of the dataset
k = K best cardinality
alpha = alpha based value restriction
Inside the GRASP function you should also define the number of **iterations** and **chunks**

Once you have all of the variables set and ready you can run the  **grasp(name, k, alpha)** function and it will display the  **Initial solution** and the **Best solution**

	> Go to branch =  "final-grasp" in case you are in a different branch

## Libraries needed
- numpy
- csv
- timeit
- copy
- math
- random
