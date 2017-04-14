from collections import defaultdict
from path import Path

class PathTable(object):
    """
    Lookup tables for paths. This way we can avoid having to compute
    all paths each time we need to do efficiency computations.
    """

    def __init__(self):
        self.paths = defaultdict(lambda: defaultdict(set))


    def has_path(self, src, dst):
        """
        Checks if the lookup table has an entry for the given src-dst.
        Args:
            src: source id.
            dst: destination id.
        Returns:
            True iff an entry exists, False otherwise.
        """
        return src in self.paths and dst in self.paths[src]


    def get_path(self, src, dst):
        """
        Gets path from lookup table.
        Args:
            src: source id.
            dst: destination id.
        Returns:
            path as list if exists, None otherwise
        """
        if src in self.paths and dst in self.paths[src]:
            return list(self.paths[src][dst])

        return []


    def put_path(self, path, src=None, dst=None):
        """
        Stores a new path in the lookup table.
        Also stores the reverse direction of the path.

        Args:
            path: path obj to store.
            src: source id. If not supplied inferrs that path[0] is src. Defaults to None.
            dst: destination id. If not supplied inferrs that path[-1] is dst. Defaults to None.
        """

        if path:
            if not src or not dst:
                src, dst = path.src_dpid, path.dst_dpid

            if src != dst:
                if path in self.paths[src][dst]:
                    #print "\tHas already path:\t{}".format(path)
                    self.set_path_active(src, dst, path)
                else:
                    #print "\tInserting path:\t{}".format(path)
                    self.paths[src][dst].add(path)
        else:
            print "Empty path received"


    def has_active_paths(self, src, dst):
        paths = self.get_active_paths(src, dst)
        return (paths != None and len(paths) > 0)


    def get_active_paths(self, src = None, dst = None):
        """
        Returns active (currently used) paths.

        If src and dst are both defined then it returns a list containing
        all paths active between src and dst.

        If only src is given, it returns a dictionary using the destination
        as key and the paths as values.

        Args:
            src: source dpid. Defaults to None.
            dst: destination dpid. Defaults to None.
        """
        all_active_paths = defaultdict(lambda: defaultdict(set))

        if src and dst:
            return self.get_active_paths_between_src_dst(src, dst)
        else:
            for src in self.paths:
                for dst in self.paths[src]:
                    all_active_paths[src][dst] = self.get_active_paths_between_src_dst(src, dst)
            return all_active_paths


    def get_active_paths_between_src_dst(self, src, dst):
        if src in self.paths and dst in self.paths[src]:
            return [path for path in self.paths[src][dst] if path.is_active]
        return set()


    def print_active_paths(self):
        print "------ Active Path -----\n"
        active_paths = self.get_active_paths()
        for src in active_paths:
            for dst in active_paths[src]:
                print "({}-{}):\t{}\n\n".format(src, dst, active_paths[src][dst])
        print "------ End Active Path -----\n"


    def set_path_active(self, src, dst, path, is_active=True):
        if src in self.paths and dst in self.paths[src]:
            for p in self.paths[src][dst]:
                if p == path:
                    p.is_active = is_active


    def __str__(self):
        s = ""
        for key1 in self.paths:
            i = 3
            for key2 in self.paths[key1]:
                s += "({}, {}): {}\n".format(key1, key2, self.paths[key1][key2])
                i -= 1
                if i == 0:
                    break
        return s[:-1]


    def __repr__(self):
        return self.__str__()
