class Path(object):
    """
    Object representing a path.
    """
    workload = 0.0
    def __init__(self, src_dpid, src_port, dst_dpid, dst_port, path):
        """
        Args:
            src_dpid: src node dpid.
            src_port: src host port.
            dst_dpid: dst node dpid.
            dst_port: dst host port.
            path: path as list of node dpids.
        """
        self.src_dpid = src_dpid
        self.src_port = src_port
        self.dst_dpid = dst_dpid
        self.dst_port = dst_port
        self.path = path
        self.power_consumption = dict((dpid,0) for dpid in path)
        self.total_consumption = 0.0
        self.is_active = False


    @classmethod
    def of(cls, src, dst, path_list, is_active = False):
        path = cls(src.dpid, src.port, dst.dpid, dst.port, path_list)
        path.is_active = is_active
        return path


    def set_total_consumption(self, consumption):
        self.total_consumption = consumption


    def set_power_consumption(self, power_consumption):
        self.power_consumption = power_consumption
        self.total_consumption = sum(power_consumption.values())


    def reverse_path(self):
        reversePath = Path(self.dst_dpid, self.dst_port, self.src_dpid, self.src_port, self.path[::-1])
        reversePath.power_consumption = self.power_consumption
        reversePath.total_consumption = self.total_consumption
        return reversePath


    def __eq__(self, other):
        return self.src_dpid == other.src_dpid and self.src_port == other.src_port \
        and self.dst_dpid == other.dst_dpid and self.dst_port == other.dst_port \
        and self.path == other.path


    def __hash__(self):
        return hash(str(self.path) + str(self.src_dpid) + str(self.src_port) + str(self.dst_dpid) + str(self.dst_port))


    def __str__(self):
        return "{path= " + str(self.path) + ", isActive= " + str(self.is_active) + "}"


    def __repr__(self):
        return "{" + str(self.path) + ", isActive= " + str(self.is_active) + ", src_dpid=" + str(self.src_dpid) + \
        ", src_port=" + str(self.src_port) + ", dst_dpid=" + str(self.dst_dpid) + \
        ", dst_port=" + str(self.dst_port) + "}"
