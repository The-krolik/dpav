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

    def start(self, points=[]):
        for (x, y) in points:
            self.cells[x][y] = self.alive
        self.window.open()

    def _get_cell_bin(self, x, y):
        if (x < 0) or (y < 0):
            return 0
        elif (x >= len(self.cells)) or (y >= len(self.cells[x])):
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
        self.window.set_vbuffer(self.next_gen)
        self.cells, self.next_gen = self.next_gen, self.cells


def main():
    dimensions = (50, 50)
    game = GameOfLife(dimensions, 12)
    game.start()

    start = False
    while game.window.is_open():
        if "s" in game.window.eventq:
            if start == True:
                start = False
            else:
                start = True
        if not start:
            if game.window.events["mouse"]:
                pos = game.window.get_mouse_pos()
                game.cells[pos] = game.alive
            elif "0" in game.window.eventq:
               game.cells.clear() 
        else:
            game.step()
            time.sleep(0.5)


if __name__ == "__main__":
    main()
