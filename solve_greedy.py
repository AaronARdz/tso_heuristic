class solver:
    subsets = list()
    album_universe = dict()

    # parameterized constructor
    def __init__(self, subsets, album_universe):
        self.subsets = subsets
        self.album_universe = album_universe

    def solve_greedy(self):
        total = 0
        covered_album = set()
        covered_subsets = dict()
        index = None

        # sort tuples by cost value
        sorted_subsets = sorted(self.subsets, key=lambda x: x[1])
        # initialize dictionary with values 0
        print(len(self.album_universe.keys()))

        # select subsets and fill album
        for subset in sorted_subsets:
            if covered_subsets.get(index) == 1:
                total += self.subsets[index][1]
            index = subset[2]
            if len(covered_album) == len(self.album_universe.keys()):
                print(len(covered_album), len(self.album_universe.keys()), 'All covered')
                break
            for j in subset[0]:
                if j in self.album_universe and self.album_universe.get(j) != 1:
                    self.album_universe[j] = 1
                    covered_album.add(j)
                    covered_subsets[index] = 1

        return covered_subsets, total, self.album_universe
