from collections import defaultdict

class PathTable(object):
    """
    Lookup tables for paths. This way we can avoid having to compute
    all paths each time we need to do efficiency computations.
    """

    def __init__(self):
        self.paths = defaultdict(lambda: defaultdict(set))
        self.reverse = defaultdict(lambda: defaultdict(set))


    def has_path(self, src, dst):
        """
        Checks if the lookup table has an entry for the given src-dst.
        Args:
            src: source id.
            dst: destination id.
        Returns:
            True iff an entry exists, False otherwise.
        """
        if src in self.paths:
            return dst in self.paths[src]
        elif src in self.reverse:
            return dst in self.reverse[src]
        return False


    def get_path(self, src, dst):
        """
        Gets path from lookup table.
        Args:
            src: source id.
            dst: destination id.
        Returns:
            path as list if exists, None otherwise
        """
        if src in self.paths:
            return list(self.paths[src][dst])
        elif src in self.reverse:
            return list(self.reverse[src][dst])
        return None


    def put_path(self, path, src=None, dst=None):
        """
        Stores a new path in the lookup table.
        Also stores the reverse direction of the path.
        Args:
            path: path to store.
            src: source id. If not supplied inferrs that path[0] is src.
            dst: destination id. If not supplied inferrs that path[-1] is dst.
        """
        if path:
            if not src or not dst:
                src, dst = path[0], path[-1]
            self.paths[src][dst].add(path)
            self.reverse[dst][src].add(path[::-1])
        else:
            print "Empty path received"


    def __str__(self):
        s = ""
        for key1 in self.paths:
            for key2 in self.paths[key1]:
                s += "({}, {}): {}\n".format(key1, key2, self.paths[key1][key2])
        return s[:-1]
