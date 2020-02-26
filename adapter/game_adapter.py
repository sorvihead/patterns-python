class Light:
    def __init__(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
        self.lights = []
        self.obstacles = []

    def set_dim(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]

    def set_lights(self, lights):
        self.lights = lights
        self.generate_lights()

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
        self.generate_lights()

    def generate_lights(self):
        return self.grid.copy()


class System:
    def __init__(self):
        self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
        self.map[5][7] = 1  # Источники света
        self.map[5][2] = -1  # Стены

    def get_lightening(self, light_mapper):
        self.lightmap = light_mapper.lighten(self.map)


class MappingAdapter:
    def __init__(self, adaptee: Light):
        self.adaptee = adaptee

    def lighten(self, grid):
        lights = [(j, i) for i in range(len(grid)) for j in range(len(grid[i]))
                  if grid[i][j] > 0]
        obstacles = [(j, i) for i in range(len(grid)) for j in range(len(grid[i]))
                     if grid[i][j] < 0]

        self.adaptee.set_dim((len(grid[0]), len(grid)))
        self.adaptee.set_lights(lights)
        self.adaptee.set_obstacles(obstacles)
        return self.adaptee.generate_lights()


if __name__ == '__main__':
    s = System()
    print(s.map[5])
    l = Light((0, 0))
    a = MappingAdapter(l)
    s.get_lightening(a)
    print(s.lightmap)
