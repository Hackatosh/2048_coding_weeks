from random import randint
from tkinter import *
import tkinter.font as tkFont

# Config

TILES_BG_COLOR = {0: "#9e948a", 1: "#eee4da", 2: "#ede0c8", 3: "#f1b078", \
                  4: "#eb8c52", 5: "#f67c5f", 6: "#f65e3b", \
                  7: "#edcf72", 8: "#edcc61", 9: "#edc850", \
                  10: "#edc53f", 11: "#edc22e", 12: "#5eda92", \
                  13: "#24ba63"}

TILES_FG_COLOR = {0: "#776e65", 1: "#776e65", 2: "#776e65", 3: "#f9f6f2", \
                  4: "#f9f6f2", 5: "#f9f6f2", 6: "#f9f6f2", 7: "#f9f6f2", \
                  8: "#f9f6f2", 9: "#f9f6f2", 10: "#f9f6f2", \
                  11: "#f9f6f2", 12: "#f9f6f2", 13: "#f9f6f2"}

TILES_FONT = {"family": "Verdana", "size": 40, "weight": 'bold'}

THEMES = {
    'classic': {
        0: ' ',
        1: '2',
        2: '4',
        3: '8',
        4: '16',
        5: '32',
        6: '64',
        7: '128',
        8: '256',
        9: '512',
        10: '1024',
        11: '2048'
    }
}


class Game:

    def __init__(self, grid_size: int, max_value: int):
        self.__size = grid_size
        self.__grid = [[0 for i in range(grid_size)] for i in range(grid_size)]
        self.__max_value = max_value

    @property
    def size(self):
        return self.__size

    @property
    def grid(self):
        return self.__grid

    @property
    def max_value(self):
        return self.__max_value

    def is_grid_full(self):
        for i in range(self.__size):
            for j in range(self.__size):
                if self.grid[i][j] == 0:
                    return False
        return True

    def is_game_won(self):
        for i in range(self.__size):
            for j in range(self.__size):
                if self.__grid[i][j] == self.__max_value:
                    return True
        return False

    def is_game_finished(self):
        return self.is_game_won() or self.is_grid_full()

    def get_empty_cells(self):
        empty_cells = []
        for i in range(self.__size):
            for j in range(self.__size):
                if self.__grid[i][j] == 0:
                    empty_cells.append({"row": i, "column": j})
        return empty_cells

    def put_in_empty_cell(self, value: int, row: int, column: int):
        if value > self.__max_value or value < 0:
            raise Exception("Incorrect value to put in empty cell")
        if row < 0 or row > self.__size - 1:
            raise Exception("Incorrect row value")
        if column < 0 or column > self.__size - 1:
            raise Exception("Incorrect column value")
        if self.__grid[row][column] != 0:
            raise Exception("Cell not empty")
        self.__grid[row][column] = value

    def place_random_number(self):
        empty_cells = self.get_empty_cells()
        cell = empty_cells[randint(0, len(empty_cells) - 1)]
        value = 1 if randint(0, 9) != 9 else 2
        self.put_in_empty_cell(value, cell['row'], cell['column'])

    # standard play to the left
    @staticmethod
    def __standard__play(grid: [[int]]):
        new_grid = []
        for row in grid:
            new_row = [0 for i in row]
            current_value = 0
            current_index = 0
            for value in row:
                if value != 0:
                    if current_value != 0:
                        if value == current_value:
                            new_row[current_index] = current_value + 1
                            current_index += 1
                            current_value = 0
                        else:
                            new_row[current_index] = current_value
                            current_index += 1
                            current_value = value
                    else:
                        current_value = value
            if current_value != 0:
                new_row[current_index] = current_value
            new_grid.append(new_row)
        return new_grid

    @staticmethod
    def __rotate_grid_left(grid: [[int]]):
        column_number = len(grid[0])
        new_grid = []
        for i in range(column_number):
            new_row = [x[i] for x in grid]
            new_grid.append(new_row[::-1])
        return new_grid

    @staticmethod
    def __rotate_grid_right(grid: [[int]]):
        new_grid = Game.__rotate_grid_left(Game.__rotate_grid_left(Game.__rotate_grid_left(grid)))
        return new_grid

    @staticmethod
    def __invert_grid_horizontally(grid: [[int]]):
        return [x[::-1] for x in grid]

    def __play_up(self):
        grid = Game.__rotate_grid_right(self.__grid)
        self.__grid = Game.__rotate_grid_left(Game.__standard__play(grid))

    def __play_down(self):
        grid = Game.__rotate_grid_left(self.__grid)
        self.__grid = Game.__rotate_grid_right(Game.__standard__play(grid))

    def __play_right(self):
        grid = Game.__invert_grid_horizontally(self.__grid)
        self.__grid = Game.__invert_grid_horizontally(Game.__standard__play(grid))

    def __play_left(self):
        grid = self.__grid
        self.__grid = Game.__standard__play(grid)

    def play(self, command: str):
        if command == "l":
            self.__play_left()
        elif command == "r":
            self.__play_right()
        elif command == "u":
            self.__play_up()
        elif command == "d":
            self.__play_down()
        else:
            raise Exception("Uncorrect command")
        is_finished = self.is_game_finished()
        if not is_finished:
            self.place_random_number()
        return is_finished

    @staticmethod
    def create_game(size: int, max_value: int):
        game = Game(size, max_value)
        empty_cells = game.get_empty_cells()
        cell = empty_cells[randint(0, len(empty_cells) - 1)]
        game.put_in_empty_cell(1, cell['row'], cell['column'])
        empty_cells = game.get_empty_cells()
        cell = empty_cells[randint(0, len(empty_cells) - 1)]
        game.put_in_empty_cell(2, cell['row'], cell['column'])
        return game


class GameGUI:

    def __init__(self, game: Game, theme):
        self.__game = game
        self.__theme = theme
        self.__is_finished = game.is_game_finished()
        self.__root = Tk()
        self.__root.title("2048")
        self.__background = Frame(self.__root)
        self.__grid_frames = []
        self.__grid_labels = []
        for i, row in enumerate(game.grid):
            current_frames_row = []
            current_labels_row = []
            for j, cell in enumerate(row):
                current_gui_cell_frame = Frame(self.__background,
                                               bg=TILES_BG_COLOR[cell],bd=10)
                current_gui_cell_frame.grid(row=i, column=j)
                current_gui_cell_label = Label(current_gui_cell_frame,width=3, text=theme[cell], bg=TILES_BG_COLOR[cell],
                                               fg=TILES_FG_COLOR[cell], font=(TILES_FONT['family'], TILES_FONT['size'], TILES_FONT['weight']))
                current_frames_row.append(current_gui_cell_frame)
                current_labels_row.append(current_gui_cell_label)
            self.__grid_frames.append(current_frames_row)
            self.__grid_labels.append(current_labels_row)

    def show(self):
        for row in self.__grid_labels:
            for label in row:
                label.pack()
        self.__background.pack()
        self.__root.mainloop()
        self.__root.focus_set()

    def update(self):
        for i, row in enumerate(self.__game.grid):
            for j, cell in enumerate(row):
                print(TILES_BG_COLOR[cell])
                self.__grid_frames[i][j].config(bg=TILES_BG_COLOR[cell])
                self.__grid_labels[i][j].config(text=self.__theme[cell],bg=TILES_BG_COLOR[cell], fg=TILES_FG_COLOR[cell])

    def play_kp(self, command: str):
        if not self.__game.is_game_finished():
            self.__is_finished = self.__game.play(command)
        self.update()

    def kp_left(self, event):
        self.play_kp("l")

    def kp_right(self, event):
        self.play_kp("r")

    def kp_up(self, event):
        self.play_kp("u")

    def kp_down(self, event):
        self.play_kp("d")

    def bind_controls(self):
        self.__root.bind('<Left>', self.kp_left)
        self.__root.bind('<Right>', self.kp_right)
        self.__root.bind('<Up>', self.kp_up)
        self.__root.bind('<Down>', self.kp_down)


def play():
    theme = THEMES['classic']
    game = Game.create_game(5, 11)
    gui = GameGUI(game, theme)
    gui.bind_controls()
    gui.show()



if __name__ == '__main__':
    play()
