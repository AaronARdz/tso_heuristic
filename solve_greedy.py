import copy
import math
import random
import numpy as np

class Solver:
    subsets = list()
    album_universe = dict()
    scores = list()
    sorted_score_list = list()
    chunk_size = 0
    cardinality = 0
    alpha = 0
    global_counter = 0
    best_score = 0
    worst_score = 0
    allow_alpha = False
    allow_k_best = False

    # parameterized constructor
    def __init__(self, subsets, album_universe, k, alpha, chunk_size):
        self.subsets = subsets
        self.album_universe = album_universe
        self.cardinality = k
        self.alpha = alpha
        self.chunk_size = chunk_size

    def set_alpha(self, value):
        self.allow_alpha = value

    def set_k_best(self, value):
        self.allow_k_best = value

    def solve_greedy(self):
        total = 0
        covered_album = set()
        covered_subsets = dict()
        index = None
        xd = 0

        # sort tuples by cost value
        sorted_subsets = sorted(self.subsets, key=lambda x: x[1])
        # print("columns", len(sorted_subsets[0][0]))
        # initialize dictionary with values 0
        print(len(self.album_universe.keys()), 'album keys')

        # select subsets and fill album
        for subset in sorted_subsets:
            xd += subset[1]
            if covered_subsets.get(index) == 1:
                total += self.subsets[index][1]
            index = subset[2]
            if len(covered_album) == len(self.album_universe.keys()):
                break
            for j in subset[0]:
                if j in self.album_universe and self.album_universe.get(j) != 1:
                    self.album_universe[j] = 1
                    covered_album.add(j)
                    covered_subsets[index] = 1

        return covered_subsets, total, self.album_universe

    def solve_heuristic(self):
        total = 0
        covered_album = set()
        covered_subsets = dict()
        index = None
        idx = 0
        counter = 0
        # initialize dictionary with values 0
        subset_score = list()
        currentAlbum = copy.copy(self.album_universe)

        # select subsets and set scores
        for subset in self.subsets:
            coincidences = set()
            for j in subset[0]:
                if j in currentAlbum:
                    coincidences.add(j)
            tup = (len(coincidences) * 2) / subset[1], idx
            # tup = subset[1], idx
            subset_score.append(tup)
            idx += 1

        # sort tuples by cost value
        sorted_scores = sorted(subset_score, key=lambda x: x[0], reverse=True)
        self.sorted_score_list = copy.copy(sorted_scores)

        # select subsets and fill album
        for score in sorted_scores:
            counter += 1
            score_idx = score[1]
            subset = self.subsets[score_idx]
            if covered_subsets.get(index) == 1:
                total += self.subsets[index][1]
            index = score_idx
            if len(covered_album) == len(currentAlbum.keys()):
                break
            for j in subset[0]:
                if j in currentAlbum and currentAlbum.get(j) != 1:
                    currentAlbum[j] = 1
                    covered_album.add(j)
                    covered_subsets[index] = 1

        self.global_counter = copy.copy(counter-1)

        return covered_subsets, total

    def chunks(self, lst, n):
        list_chunks = list()
        # print('Best Score: ', self.best_score, 'Worst score: ', self.worst_score)
        # print('alpha: ', self.alpha * (self.best_score - self.worst_score))
        picked = 0

        # Yield successive n-sized chunks from lst
        for i in range(0, len(lst), n):
            list_chunks.append(lst[i:i + n])

        flat_chunks = list()

        for chunk in list_chunks:
            max_score = chunk[0][0]
            min_score = chunk[-1][0]
            random.shuffle(chunk)
            k_counter = copy.copy(self.cardinality)
            for j in chunk:
                # Normalize scores with best and worst of chunk
                # Select subsets based in cardinality
                if self.allow_alpha:
                    normalized_score = (j[0] - min_score) / (max_score - min_score) * 100
                    if normalized_score > self.alpha * (self.best_score - self.worst_score):
                        picked += 1
                        flat_chunks.append(j)
                if self.allow_k_best and self.cardinality <= self.chunk_size:
                    if k_counter > 0:
                        picked += 1
                        k_counter -= 1
                        flat_chunks.append(j)
                # Normalize scores with best and worst of full candidate list
                # normalized_score = (j[0] - self.worst_score) / (self.best_score - self.worst_score) * 100
                # if normalized_score > self.alpha * (self.best_score - self.worst_score):
                #     picked += 1
                #     flat_chunks.append(j)

        # print(picked)
        # print(len(lst))

        self.sorted_score_list = copy.copy(flat_chunks)
        return flat_chunks

    def solve_heuristic_randomized(self):
        total = 0
        covered_album = set()
        covered_subsets = dict()
        index = None
        idx = 0
        counter = 0
        # initialize dictionary with values 0
        subset_score = list()
        currentAlbum = copy.copy(self.album_universe)

        # select subsets and set scores
        for subset in self.subsets:
            coincidences = set()
            for j in subset[0]:
                if j in currentAlbum:
                    coincidences.add(j)
            tup = (len(coincidences) * 2) / subset[1], idx
            # tup = subset[1], idx
            subset_score.append(tup)
            idx += 1

        # sort tuples by cost value
        sorted_scores = sorted(subset_score, key=lambda x: x[0], reverse=True)
        self.best_score = sorted_scores[0][0]
        self.worst_score = sorted_scores[-1][0]
        # Divide sorted score list in chunks of size k cardinality
        # Randomized each chunk and return flat list
        sorted_scores = self.chunks(sorted_scores, self.chunk_size)

        # select subsets and fill album
        for score in sorted_scores:
            counter += 1
            score_idx = score[1]
            subset = self.subsets[score_idx]
            if covered_subsets.get(index) == 1:
                total += self.subsets[index][1]
            index = score_idx
            if len(covered_album) == len(currentAlbum.keys()):
                break
            for j in subset[0]:
                if j in currentAlbum and currentAlbum.get(j) != 1:
                    currentAlbum[j] = 1
                    covered_album.add(j)
                    covered_subsets[index] = 1

        self.global_counter = copy.copy(counter-1)

        return covered_subsets, total


    def local_search_swap(self):
        winning_list, total = self.solve_heuristic_randomized()
        current_solution = copy.copy(winning_list)
        new_solution = current_solution
        ls_album = dict()
        improved = False
        finished = False
        current_total = copy.copy(total)
        new_total = current_total
        tries = 0
        global_counter = 0
        switched_list = list()
        improved_score = list()

        while not finished:
            if not improved:
                ls_album = copy.copy(self.album_universe)
                switched_list = list(new_solution.keys())
                current_solution = copy.copy(new_solution)
                improved_score = list()
                current_total = new_total
            elif improved:
                tries = 0
                ls_album = copy.copy(self.album_universe)
                switched_list = list(new_solution.keys())
                improved_score = list()
                current_total = new_total

            for x in range(math.floor(len(switched_list))):
                if x >= len(switched_list):
                    print("Ya se checaron todos los subsets elegidos")
                    finished = True
                    break
                idx = switched_list[x]
                score = 0
                coincidences = list()
                for y in self.subsets[idx][0]:
                    if y in ls_album:
                        ##print(y, 'found y')
                        score += 1
                        coincidences.append(y)
                        del ls_album[y]

                idx_score_tuple = idx, score, coincidences
                improved_score.append(idx_score_tuple)
            # encontrar los subsets elegidos que aportan menos
            improved_score = sorted(improved_score, key=lambda x: x[1], reverse=True)
            # print('improved', improved_score)


            # encontrar los items de los subsets anteriores
            last_two_list = list()

            # buscar combinaciones
            found = False
            count = 0
            cost_sum = 0
            subsets_to_replace = []
            for x in range(len(improved_score)):
                if count == 2:
                    break
                x += tries + 1
                last_two_list.append(improved_score[-x][2])
                count += 1
                cost_sum += self.subsets[improved_score[-x][0]][1]
                subsets_to_replace.append(improved_score[-x][0])
                # del current_solution[improved_score[-x][0]]

            flat_list = [item for sublist in last_two_list for item in sublist]
            # print(flat_list)
            # print('subsets to replace', subsets_to_replace)

            # buscar esos items en un subset
            found_subset = []
            for s in self.sorted_score_list:
                result = all(elem in self.subsets[s[1]][0] for elem in flat_list)
                if result == True:
                    ## dont quit, save subset info to compare
                    found_subset = self.subsets[s[1]]
                    found = True
                    break

            # comparar costos
            # if len(found_subset) > 0:
                # print(found_subset, 'found subset')

            # print(tries, 'tries')
            # print(cost_sum, 'cost')
            if found and cost_sum > found_subset[1]:
                for sub in subsets_to_replace:
                    del current_solution[sub]
                # print('mejora encontrada')
                # actualizar el total
                new_total = current_total - cost_sum
                new_total += found_subset[1]
                # actualizar la lista de subsets elegida
                current_solution[found_subset[2]] = 1
                # print('Improved total', new_total)
                # print('Total new subsets: ', len(current_solution.keys()))
                # print(new_solution)
                new_solution = current_solution
                improved = True
            else:
                improved = False

            tries += 1
            global_counter += 1

            if tries == len(improved_score) - 1:
                finished = True

            if global_counter == 1000:
                finished = True

        return new_total, new_solution,


