from collections import defaultdict
from path import Path

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
            path: path obj to store.
            src: source id. If not supplied inferrs that path[0] is src. Defaults to None.
            dst: destination id. If not supplied inferrs that path[-1] is dst. Defaults to None.
        """

        if path and src != dst:
            if not src or not dst:
                src, dst = path.path[0], path.path[-1]

            self.paths[src][dst].add(path)
            self.reverse[dst][src].add(path.reverse_path())
        else:
            if src != dst:
                print "Empty path received"


    def has_active_paths(self, src, dst):
        paths = self.get_active_paths(src, dst)
        reverse_paths = self.get_active_paths(dst, src)
        return (paths != None and len(paths) > 0) or (reverse_paths != None and len(reverse_paths) > 0)


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
            paths = self.get_active_paths_between_src_dst(src, dst)
            if paths:
                return paths
            return self.get_active_paths_between_src_dst(dst, src)
        elif src:
            print "Only src provided"
            src_paths = self.paths[src]
            for dst in src_paths:
                all_active_paths[src][dst] = self.get_active_paths_between_src_dst(src, dst)
            return all_active_paths[src]
        else:
            print "Fetching all paths"
            for src in self.paths:
                for dst in self.paths[src]:
                    #src_dst_paths = self.paths[src][dst]
                    all_active_paths[src][dst] = self.get_active_paths_between_src_dst(src, dst)
            return all_active_paths


    def get_active_paths_between_src_dst(self, src, dst):
        if src in self.paths and dst in self.paths[src]:
            src_dst_paths = self.paths[src][dst]
            return [path for path in src_dst_paths if path.is_active]
        elif src in self.reverse and dst in self.reverse[src]:
            src_dst_paths = self.reverse[src][dst]
            return [path for path in src_dst_paths if path.is_active]
        return set()


    def print_active_paths(self):
        print "------ Active Path -----\n"
        active_paths = self.get_active_paths()
        for src in active_paths:
            for dst in active_paths[src]:
                print "({}-{}):\t{}\n\n".format(src, dst, active_paths[src][dst])
        print "------ End Active Path -----\n"


    def set_path_active(self, src, dst, path):
        if src in self.paths:
            if dst in self.paths[src][dst]:
                for p in self.paths[src][dst]:
                    if p == path:
                        p.is_active = True
            else:
                if src in self.reverse:
                    if dst in self.reverse[src][dst]:
                        for p in self.reverse[src][dst]:
                            if p == path:
                                p.is_active = True
                    else:
                        print "1 No path for given dst"

                elif dst in self.reverse:
                    if src in self.reverse[dst][src]:
                        for p in self.reverse[dst][src]:
                            if p == path:
                                p.is_active = True
                    else:
                        print "1 No path for given src"
                else:
                    print "2 No path for given dst"
        else:
            print "3 no path for given src"


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
