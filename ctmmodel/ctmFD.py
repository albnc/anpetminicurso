

class CTMFD:
    def __init__(self, density_bps, vf_bps):
        self.density_bps = density_bps
        self.flow_bps = vf_bps
        self.ramp_impact = None

        self._capacity = max(self.flow_bps)
        self._ind = self.flow_bps.index(self._capacity)
        self._kc = self.density_bps[self._ind]

    def get_flow(self, density):
        for p in range(len(self.density_bps)-1):
            if self.density_bps[p] <= density < self.density_bps[p+1]:
                alpha = (density-self.density_bps[p])/(self.density_bps[p+1]-self.density_bps[p])

                flow = (1-alpha)*self.flow_bps[p] + alpha*self.flow_bps[p+1]
                return flow
        return 0

    def get_capacity(self):
        pass

    def get_kc(self):
        return self._kc

    def get_demand(self, density):
        return self.get_flow(min(density, self._kc))

    def get_supply(self, density):
        return self.get_flow(max(density, self._kc))

    def is_concave(self):
        speeds = []
        for p in range(len(self.density_bps)-1):
            v = (self.flow_bps[p+1]-self.flow_bps[p])/(self.density_bps[p+1]-self.density_bps[p])
            speeds.append(v)

        for p in range(len(speeds)-1):
            if speeds[p] < speeds[p+1]:
                # print("invalid",self.flow_bps, self.density_bps, speeds)
                return False

        return True

if __name__ == '__main__':
    # density_bps = [0,0.015,0.03,0.06,0.09]
    # flow_bps = [0,0.45, 0.59, 0.3, 0.0]
    density_bps = [0, 0.017563117362133968, 0.035126234724267937, 0.07025246944853587, 0.07008377530828344]
    flow_bps = [0, 0.4024672292169058, 0.43052086144126855, 0.45317907546313985, 0]


    import pylab

    fd = CTMFD(density_bps, flow_bps)
    print(fd.is_concave())
    print(fd._kc)
    print(fd._kc, fd._capacity,fd.get_flow(fd.get_kc()))

    densities = []
    supplies = []
    demands = []
    flows = []
    for i in range(100):
        densities.append(i*0.001)
        flows.append(fd.get_flow(densities[i]))
        demands.append(fd.get_demand(i))
        supplies.append(fd.get_supply(i))

    pylab.plot(densities, flows)
    # pylab.plot(densities, demands)
    # pylab.plot(densities, supplies)
    pylab.show()