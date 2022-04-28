import copy
import math
import random

class solver:
    subsets = list()
    album_universe = dict()
    scores = list()
    sorted_score_list = list()
    global_counter = 0

    # parameterized constructor
    def __init__(self, subsets, album_universe):
        self.subsets = subsets
        self.album_universe = album_universe

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

    def localsearch(self):
        winning_list, total = self.solve_heuristic()
        improved = False
        tries = 0

        while not improved:
            ls_total = 0
            ls_album = copy.copy(self.album_universe)
            ls_covered_subsets = dict()
            ls_covered_album = set()
            switched_list = copy.copy(winning_list)
            switched_list.pop(random.choice(list(winning_list.keys())))

            for i in range(5):
                switched_list[self.sorted_score_list[self.global_counter+tries+i][1]] = 1

            for idx in switched_list.keys():
                subset = self.subsets[idx]
                index = idx
                ls_total += self.subsets[index][1]
                if len(ls_covered_album) == len(ls_album.keys()):
                    break
                for j in subset[0]:
                    if j in ls_album and ls_album.get(j) != 1:
                        ls_album[j] = 1
                        ls_covered_album.add(j)
                        ls_covered_subsets[index] = 1
            tries += 1
            print(tries, 'intento')

            print(len(ls_covered_album), len(ls_album.keys()))
            print('Actual->', total,'ls ->', ls_total)
            if ls_total < total and len(ls_covered_album) == len(ls_album.keys()):
                improved = True
                print('Improved')
            if tries == 100:
                improved = True

        print(winning_list.keys())

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
        winning_list, total = self.solve_heuristic()
        print('FIRST SOLUTION', winning_list)
        print('Total picked subsets: ', len(winning_list.keys()))
        improved = False
        tries = 0
        print(total)

        while not improved:
            ls_total = 0
            ls_album = copy.copy(self.album_universe)
            ls_covered_subsets = dict()
            ls_covered_album = set()
            original_list = copy.copy(winning_list)
            switched_list = list(winning_list.keys())
            improved_score = list()

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
                del original_list[improved_score[-x][0]]

            flat_list = [item for sublist in last_two_list for item in sublist]
            print(flat_list)
            print('subsets to replace', subsets_to_replace)

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
            print(found_subset, 'found subset')
            print(cost_sum, 'cost sum')
            if found and cost_sum > found_subset[1]:
                print('mejora encontrada')
                # actualizar el total
                ls_total = total - cost_sum
                ls_total += found_subset[1]
                # actualizar la lista de subsets elegida
                original_list[found_subset[2]] = 1
                print('Improved total', ls_total)
                print('Total new subsets: ', len(original_list.keys()))
                print(winning_list)
                winning_list = original_list
                improved = True

            tries += 1

            if tries == len(improved_score) - 1:
                improved = True

        print(winning_list.keys())



