import copy
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

        # select subsets and fill album
        for subset in self.subsets:
            coincidences = set()
            for j in subset[0]:
                if j in currentAlbum:
                    coincidences.add(j)
            # tup = (len(coincidences) * 2) / subset[1], idx
            tup = len(coincidences), idx
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
            print(len(self.sorted_score_list))
            print(self.global_counter, 'counter')
            print(self.sorted_score_list)

            for i in range(10):
                switched_list[self.sorted_score_list[self.global_counter+i][1]] = 1

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
            print(tries)

            print(len(ls_covered_album), len(ls_album.keys()))
            print(total, ls_total)
            if ls_total < total and len(ls_covered_album) == len(ls_album.keys()):
                improved = True
            if tries == 5:
                improved = True

        print(winning_list.keys())

# 0
# 7.890778490876138
# 16.28158638594216
# 25.343808075828917
# 37.835091709831254
# 50.639895807752445
# 63.54640639624861
# 78.21918230765664
# 93.9197439575593
# 110.16145286197295
# 128.7039348343765
# 152.55802759831937
# 177.81005896526452
# 203.33905239055542
# 229.10047650724164
# 277.2821800749483
# 351.5792831689795
# 426.56310825538367
# 508.38825563554906
# 826.6908609218771
# 649.8535374359797


