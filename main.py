# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import pandas as pd
import numpy as np
import csv
import solve_greedy as sv
import timeit


## 1 step, Create columns
## 2 create cost value
## 3 iterate through list of columns and select random index
## 4 save random index number in a dictionary to make sure there's no duplicates
## 6 adjust the size of the dictionary to fit the specified album length
def create_album(size, subset):
    subset_values = subset.flatten()
    subset_len = len(subset_values)
    album = dict()
    while len(album.keys()) <= size - 1:
        random_index = np.random.randint(subset_len, size=1)[0]
        value = subset_values[random_index]
        if value not in album:
            album[value] = 0
        else:
            value = subset_values[random_index - 1]
            album[value] = 0

    return album


def create_subsets(number_of_subsets, columns, rangen):
    subsets = np.random.randint(rangen, size=(number_of_subsets, columns))
    return subsets


def create_cost_values(number_of_subsets):
    # return np.random.rand(number_of_subsets)
    mu, sigma = 3., 1.  # mean and standard deviation
    return np.random.lognormal(mu, sigma, number_of_subsets)


def define_dataset(number_of_subsets, columns, album_size, rangen, name):
    subs = create_subsets(number_of_subsets, columns, rangen)
    cost_values = create_cost_values(number_of_subsets)
    album_list = create_album(album_size, subs)

    subset_with_cost = list()

    for i in range(len(subs)):
        tup = [subs[i], cost_values[i], i]
        subset_with_cost.append(tup)

    with open(f'{name}.csv', "w", newline='') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(map(lambda x: [x], album_list.keys()))
        writer.writerows(subset_with_cost)


def read_data_set(name):
    with open(f'{name}.csv', newline='') as f:
        reader = csv.reader(f)
        temp_dict = dict()
        temp_list = list()
        for line in reader:
            new_line = line
            if len(new_line) == 1:
                temp_dict[new_line[0]] = 0
            else:
                # int_subset = map(lambda x: [x], new_line[0][1:-1].split())
                # print(int_subset)
                split_line = [new_line[0][1:-1].split(), float(new_line[1]), int(new_line[2])]
                temp_list.append(split_line)
    return temp_list, temp_dict


def grasp(name, k, alpha):
    start = timeit.default_timer()
    sub, alb = read_data_set(name)
    solutions = list()

    for i in range(500):
        solver = sv.Solver(sub, alb, k, alpha, chunk_size=10)
        solver.set_alpha(True)
        total, solution = solver.local_search_swap()
        number_of_subsets = solution.keys()
        tup = total, len(number_of_subsets)
        solutions.append(tup)

    solutions = sorted(solutions, key=lambda x: x[0], reverse=False)

    # for sol in solutions:
    #    print(sol)

    print('Best Solution: ', solutions[0])
    print('Worst Solution: ', solutions[-1])
    stop = timeit.default_timer()
    print('Time: ', stop - start)


if __name__ == '__main__':
    # number_of_subsets, columns, album_size, rangen
    define_dataset(4000, 10, 200, 400, 'medium_dataset_9')

    ds_list = ['mini_dataset_1',
               'mini_dataset_2',
               'mini_dataset_3',
               'medium_dataset_1',
               'medium_dataset_2',
               'medium_dataset_3',
               'big_dataset_1',
               'big_dataset_2',
               'big_dataset_3']

    grasp('mini_dataset_9', 2, .9)
    grasp('mini_dataset_9', 2, .5)
    grasp('mini_dataset_9', 2, .1)
    # for ds in ds_list:
    #     start = timeit.default_timer()
    #     sub, alb = read_data_set(ds)
    #     solver = sv.solver(sub, alb)
    #     winning_list, total, albs = solver.solve_heuristic()
    #     print(ds)
    #     print(len(winning_list.keys()), 'picked subsets')
    #     print(len(sub), 'total subs')
    #     print(total)
    #     stop = timeit.default_timer()
    #     print('Time: ', stop - start)
    #     print('----------------------------------------')

    # start = timeit.default_timer()
    # sub, alb = read_data_set("mini_dataset_2")
    # solver = sv.solver(sub, alb)
    # winning_list, total, albs = solver.solve_heuristic()
    # print("mini")
    # print('picked subsets', winning_list,)
    # print('total subs', len(sub))
    # print(total)
    # stop = timeit.default_timer()
    # print('Time: ', stop - start)

    # Local Search
