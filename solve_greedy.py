import copy
import math
import random
import numpy as np

class solver:
    subsets = list()
    album_universe = dict()
    scores = list()
    sorted_score_list = list()
    cardinality = 0
    alpha = 0
    global_counter = 0

    # parameterized constructor
    def __init__(self, subsets, album_universe, k):
        self.subsets = subsets
        self.album_universe = album_universe
        self.cardinality = k

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

        # Yield successive n-sized chunks from lst
        for i in range(0, len(lst), n):
            list_chunks.append(lst[i:i + n])

        flat_chunks = list()

        for chunk in list_chunks:
            random.shuffle(chunk)
            for j in chunk:
                flat_chunks.append(j)

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
        # Divide sorted score list in chunks of size k cardinality
        # Randomized each chunk and return flat list
        sorted_scores = self.chunks(sorted_scores, self.cardinality)

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

    def localsearch_improved(self):
        winning_list, total = self.solve_heuristic()
        print('Total picked subsets: ', len(winning_list.keys()))
        improved = False
        finished = False
        tries = 1
        new_total = 0
        improved_list = list()
        all_tries = 0

        while not finished:
            print('Current total', total)
            if not improved:
                ls_total = 0
                ls_album = copy.copy(self.album_universe)
                ls_covered_subsets = dict()
                ls_covered_album = set()
                switched_list = list(winning_list.keys())
                improved_score = list()
                additional_scores = list()
                print("switched", switched_list)
                current_total = new_total
            else:
                total = new_total
                ls_total = 0
                ls_album = copy.copy(self.album_universe)
                ls_covered_subsets = dict()
                ls_covered_album = set()
                switched_list = improved_list
                tries = 0
                improved_score = list()
                additional_scores = list()
                print("switched", switched_list)



            for x in range(math.floor(len(switched_list)/2) + tries):
                if x >= len(switched_list):
                    print("Ya se checaron todos los subsets elegidos")
                    # finished = True
                    break
                idx = switched_list[x]
                score = 0
                for y in self.subsets[idx][0]:
                    if y in ls_album:
                        ##print(y, 'found y')
                        score += 1
                        del ls_album[y]

                idx_score_tuple = idx, score
                improved_score.append(idx_score_tuple)

            improved_score = sorted(improved_score, key=lambda x: x[1], reverse=True)
            print('imp', improved_score)

            print(len(self.sorted_score_list) - self.global_counter)
            for x in range(len(self.sorted_score_list) - self.global_counter):
                appears = set()
                sorted_sub_idx = self.global_counter + x
                actual_idx = self.sorted_score_list[sorted_sub_idx][1]
                for y in self.subsets[actual_idx][0]:
                    if y in ls_album:
                        appears.add(y)
                        # del ls_album[y] ## maybe remove
                tup = len(appears), self.subsets[actual_idx][2]
                additional_scores.append(tup)

            additional_scores = sorted(additional_scores, key=lambda x: x[0], reverse=True)
            final_album = copy.copy(self.album_universe)

            for x in improved_score:
                if len(ls_covered_album) == len(final_album.keys()):
                    break
                for y in self.subsets[x[0]][0]:
                    if y in final_album and final_album.get(y) != 1:
                        final_album[y] = 1
                        ls_covered_album.add(y)
                        ls_covered_subsets[x[0]] = 1

            print('winning', winning_list)

            for x in additional_scores:
                if len(ls_covered_album) == len(final_album.keys()):
                    break
                for y in self.subsets[x[1]][0]:
                    if y in final_album and final_album.get(y) != 1:
                        final_album[y] = 1
                        ls_covered_album.add(y)
                        ls_covered_subsets[x[1]] = 1

            print('covered', ls_covered_subsets)
            print(len(ls_covered_album), len(final_album.keys()))

            new_count = 0

            for sub in ls_covered_subsets.keys():
                ls_total += self.subsets[sub][1]
                new_count += 1

            print('new total: ', ls_total)
            print('new count', new_count)

            tries += 1
            all_tries += 1
            print(all_tries, 'intento')

            if ls_total < total and len(ls_covered_album) == len(final_album.keys()):
                print('Improved')
                improved = True
                improved_list = list(ls_covered_subsets.keys())
                new_total = ls_total
            else:
                improved = False

            if tries == 100:
                improved = True

            if tries == 60:
                finished = True

        print('Improved list: ',len(improved_list))

    def local_search_swap(self):
        winning_list, total = self.solve_heuristic_randomized()
        print('FIRST SOLUTION', winning_list)
        print('Total picked subsets: ', len(winning_list.keys()))
        current_solution = copy.copy(winning_list)
        new_solution = current_solution
        ls_album = dict()
        improved = False
        finished = False
        current_total = copy.copy(total)
        new_total = current_total
        tries = 0
        global_counter = 0
        print(new_total)

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
                    # finished = True
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
            if len(found_subset) > 0:
                print(found_subset, 'found subset')

            # print(tries, 'tries')
            # print(cost_sum, 'cost')
            if found and cost_sum > found_subset[1]:
                for sub in subsets_to_replace:
                    del current_solution[sub]
                print('mejora encontrada')
                # actualizar el total
                new_total = current_total - cost_sum
                new_total += found_subset[1]
                # actualizar la lista de subsets elegida
                current_solution[found_subset[2]] = 1
                print('Improved total', new_total)
                print('Total new subsets: ', len(current_solution.keys()))
                print(new_solution)
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


