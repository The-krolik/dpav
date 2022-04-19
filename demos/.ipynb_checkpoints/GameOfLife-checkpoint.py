import directpythonplatform as dpp
import time


class GameOfLife:
    def __init__(self, dimensions, scale, alive=0xFFFFFF, dead=0x000000):
        self.alive = alive
        self.dead = dead
        self.scale = scale
        self.cells = dpp.VBuffer(dimensions)
        self.cells.fill(dead)
        self.next_gen = dpp.VBuffer(dimensions)
        self.window = dpp.Window(self.cells, scale)

    def start(self, points):
        for (x, y) in points:
            self.cells[x][y] = self.alive
        self.window.open()

    def _get_cell_bin(self, x, y):
        if (x >= len(self.cells)) or (y >= len(self.cells[x])):
            return 0
        if self.cells[x][y] == self.alive:
            return 1
        else:
            return 0

    def _sum_neighbors(self, x, y):
        return (
            self._get_cell_bin(x - 1, y + 1)
            + self._get_cell_bin(x, y + 1)
            + self._get_cell_bin(x + 1, y + 1)
            + self._get_cell_bin(x + 1, y)
            + self._get_cell_bin(x + 1, y - 1)
            + self._get_cell_bin(x, y - 1)
            + self._get_cell_bin(x - 1, y - 1)
            + self._get_cell_bin(x - 1, y)
        )

    def step(self):
        self.next_gen.fill(self.dead)
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                sum = self._sum_neighbors(i, j)
                if (self.cells[i][j] == self.alive) and ((sum == 2) or (sum == 3)):
                    self.next_gen[i][j] = self.alive
                elif (self.cells[i][j] == self.dead) and (sum == 3):
                    self.next_gen[i][j] = self.alive
        self.cells, self.next_gen = self.next_gen, self.cells

    def stop():
        self.window.close()


def main():
    dimensions = (100, 100)
    game = GameOfLife(dimensions, 7)
    initial_points = [(49, 50), (50, 50), (51, 50)]
    game.start(initial_points)

    start = False
    while game.window.is_open():

        if "a" in game.window.eventq:
            start = True

        if not start:
            if game.window.events["mouse"]:
                pos = game.window.get_mouse_pos()
                game.window.vbuffer.write_pixel(pos, game.alive)
        else:
            game.step()
            time.sleep(1)


if __name__ == "__main__":
    main()
