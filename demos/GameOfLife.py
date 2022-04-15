import directpythonplatform as dpp
import time


class GameOfLife:
    def __init__(dimensions, scale, alive=0xFFFFFF, dead=0x000000):
        self.alive = alive
        self.dead = dead
        self.scale = scale
        self.cells = dpp.VBuffer(dimensions)
        self.cells.fill(dead)
        self.next_gen = dpp.VBuffer(dimensions)
        self.dpp.Window(cells, scale)


    def start(self, points):
        for (x, y) in points:
            cells[x][y] = self.alive
        self.window.open()


    def _get_cell_bin(self, x, y):
        if self.cells[x][y] == self.alive:
            return 1
        else:
            return 0


    def _sum_neighbors(self, x, y):
        return (self._get_cell_bin(x - 1, y + 1)
            + self._get_cell_bin(x, y + 1)
            + self._get_cell_bin(x + 1, y + 1)
            + self._get_cell_bin(x + 1, y)
            + self._get_cell_bin(x + 1, y - 1)
            + self._get_cell_bin(x, y - 1)
            + self._get_cell_bin(x - 1, y - 1)
            + self._get_cell_bin(x - 1, y)
        )


    def step(self):
        self.next_gen.fill(dead)
        for i in range(len(grid)):
            for j in range(len(vb[i])):
                sum = self._sum_neighbors(i, j)
                if (cells[i][j] == alive) and ((sum == 2) or (sum == 3)):
                    next_gen[i][j] = alive
                elif (cells[i][j] == dead) and (sum == 3):
                    next_gen[i][j] = alive
        self.cells = self.next_gen
        self.window.write_to_screen()


    def stop():
        self.window.close()


if __name__ == "__main__":
    main()


def main():
    dimensions = (100, 100)
    game = GameOfLife(dimensions, 10)
    initial_points = [(49,50), (50,50), (51,50)]
    game.start(initial_points)
    while True:
        time.sleep(5)
        game.step()
