import numpy
import math

class CTMLink:
    def __init__(self, **kwargs):
        self.rho = None
        self.qs = None
        self.length = None
        self.lm = None
        self.num_lanes = None
        self.fd = None

        self.demands = None
        self.supplies = None

        for k,v in kwargs.items():
            self.__dict__[k] = v

    def start(self, time_step, total_time):
        self.time_step = time_step
        self.total_time = total_time
        total_steps = int(total_time/self.time_step)

        num_cells = int(self.length/self.lm)
        self.num_cells = num_cells

        self.rho = numpy.zeros((num_cells, total_steps+1))
        self.qs = numpy.zeros((num_cells, total_steps))

        self.demands = [0 for _ in range(self.num_cells)]
        self.supplies = [0 for _ in range(self.num_cells)]



    def get_outflow(self, step):
        return self.qs[self.num_cells-1,step]

    def get_upstream_density(self, step):
        return self.rho[0, step]

    def get_downstream_density(self, step):
        return self.rho[self.num_cells-1, step]

    def compute_demand_supplies(self, step):
        for cell_index in range(self.num_cells):
            self.demands[cell_index] = self.num_lanes*self.fd.get_demand(self.rho[cell_index,step])
            self.supplies[cell_index] = self.num_lanes*self.fd.get_supply(self.rho[cell_index, step])

        return self.supplies[0], self.demands[self.num_cells-1]

    def update(self, step, inflow, outflow):

        for cell_index in range(self.num_cells):
            if cell_index==0:
                up_flow = inflow

            if cell_index < self.num_cells-1:
                flow = min(self.demands[cell_index], self.supplies[cell_index+1])
            else:
                flow = outflow

            self.qs[cell_index, step] = flow

            self.rho[cell_index,step+1] = self.rho[cell_index,step] + (up_flow-self.qs[cell_index, step])*self.time_step/(self.lm*self.num_lanes)

            up_flow = self.qs[cell_index, step]
