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

GRID_SIZE_CHOICES = { 2, 3, 4, 5, 6, 7, 8}
DEFAULT_GRID_SIZE_CHOICE = 4
MAX_VALUE = 3

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

THEMES_CHOICES = {"classic"}
DEFAULT_THEME_CHOICE = "classic"

# Main objects

class Game:

    def __init__(self, grid_size: int, max_value: int):
        self.__grid_size = grid_size
        self.__grid = [[0 for i in range(grid_size)] for i in range(grid_size)]
        self.__max_value = max_value

    @property
    def grid_size(self):
        return self.__grid_size

    @property
    def grid(self):
        return self.__grid

    @property
    def max_value(self):
        return self.__max_value

    @staticmethod
    def __are_grids_equal(grid1: [[int]], grid2: [[int]]):
        if len(grid1) != len(grid2):
            return False
        for i, row in enumerate(grid1):
            if len(row) != len(grid2[i]):
                return False
            for j, cell in enumerate(row):
                if cell != grid2[i][j]:
                    return False
        return True

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

    @staticmethod
    def __play_grid_up(grid: [[int]]):
        new_grid = Game.__rotate_grid_right(grid)
        return Game.__rotate_grid_left(Game.__standard__play(new_grid))

    @staticmethod
    def __play_grid_down(grid: [[int]]):
        new_grid = Game.__rotate_grid_left(grid)
        return Game.__rotate_grid_right(Game.__standard__play(new_grid))

    @staticmethod
    def __play_grid_right(grid: [[int]]):
        new_grid = Game.__invert_grid_horizontally(grid)
        return Game.__invert_grid_horizontally(Game.__standard__play(new_grid))

    @staticmethod
    def __play_grid_left(grid: [[int]]):
        return Game.__standard__play(grid)

    def __get_empty_cells(self):
        empty_cells = []
        for i in range(self.__grid_size):
            for j in range(self.__grid_size):
                if self.__grid[i][j] == 0:
                    empty_cells.append({"row": i, "column": j})
        return empty_cells

    def __put_in_empty_cell(self, value: int, row: int, column: int):
        if value > self.__max_value or value < 0:
            raise Exception("Incorrect value to put in empty cell")
        if row < 0 or row > self.__grid_size - 1:
            raise Exception("Incorrect row value")
        if column < 0 or column > self.__grid_size - 1:
            raise Exception("Incorrect column value")
        if self.__grid[row][column] != 0:
            raise Exception("Cell not empty")
        self.__grid[row][column] = value

    def __place_random_number(self):
        empty_cells = self.__get_empty_cells()
        cell = empty_cells[randint(0, len(empty_cells) - 1)]
        value = 1 if randint(0, 9) != 9 else 2
        self.__put_in_empty_cell(value, cell['row'], cell['column'])

    def __is_grid_full(self):
        for i in range(self.__grid_size):
            for j in range(self.__grid_size):
                if self.grid[i][j] == 0:
                    return False
        return True

    def __get__possible__moves(self):
        return {
            "up": not Game.__are_grids_equal(self.__grid, Game.__play_grid_up(self.__grid)),
            "down": not Game.__are_grids_equal(self.__grid, Game.__play_grid_down(self.__grid)),
            "right": not Game.__are_grids_equal(self.__grid, Game.__play_grid_right(self.__grid)),
            "left": not Game.__are_grids_equal(self.__grid, Game.__play_grid_left(self.__grid)),
        }

    def is_game_won(self):
        for i in range(self.__grid_size):
            for j in range(self.__grid_size):
                if self.__grid[i][j] == self.__max_value:
                    return True
        return False

    def is_game_lost(self):
        if not self.__is_grid_full():
            return False
        possible_moves = self.__get__possible__moves()
        if possible_moves['up'] or possible_moves['down'] or possible_moves['right'] or possible_moves['left']:
            return False
        return True

    def is_game_finished(self):
        return self.is_game_won() or self.is_game_lost()

    def play(self, command: str):
        grid_before_move = self.__grid.copy()
        if command == "l":
            self.__grid = Game.__play_grid_left(self.__grid)
        elif command == "r":
            self.__grid = Game.__play_grid_right(self.__grid)
        elif command == "u":
            self.__grid = Game.__play_grid_up(self.__grid)
        elif command == "d":
            self.__grid = Game.__play_grid_down(self.__grid)
        else:
            raise Exception("Uncorrect command")
        is_finished = self.is_game_finished()
        if not is_finished and not Game.__are_grids_equal(self.__grid, grid_before_move):
            self.__place_random_number()
        return is_finished

    def reset_game(self):
        self.__grid = [[0 for i in range(self.__grid_size)] for i in range(self.__grid_size)]

    @staticmethod
    def create_game(size: int, max_value: int):
        game = Game(size, max_value)
        empty_cells = game.__get_empty_cells()
        cell = empty_cells[randint(0, len(empty_cells) - 1)]
        game.__put_in_empty_cell(1, cell['row'], cell['column'])
        empty_cells = game.__get_empty_cells()
        cell = empty_cells[randint(0, len(empty_cells) - 1)]
        game.__put_in_empty_cell(2, cell['row'], cell['column'])
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
                                               bg=TILES_BG_COLOR[cell], bd=10)
                current_gui_cell_frame.grid(row=i, column=j)
                current_gui_cell_label = Label(current_gui_cell_frame, width=3, text=theme[cell],
                                               bg=TILES_BG_COLOR[cell],
                                               fg=TILES_FG_COLOR[cell],
                                               font=(TILES_FONT['family'], TILES_FONT['size'], TILES_FONT['weight']))
                current_frames_row.append(current_gui_cell_frame)
                current_labels_row.append(current_gui_cell_label)
            self.__grid_frames.append(current_frames_row)
            self.__grid_labels.append(current_labels_row)

    @staticmethod
    def create_game_gui_and_show(game: Game, theme):
        gui = GameGUI(game, theme)
        gui.bind_controls()
        gui.show()

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
                self.__grid_frames[i][j].config(bg=TILES_BG_COLOR[cell])
                self.__grid_labels[i][j].config(text=self.__theme[cell], bg=TILES_BG_COLOR[cell],
                                                fg=TILES_FG_COLOR[cell])

    def __reset_game_ui(self):
        self.__game.reset_game()
        self.update()

    def play_kp(self, command: str):
        if not self.__game.is_game_finished():
            self.__is_finished = self.__game.play(command)
            self.update()
        if self.__is_finished:
            if self.__game.is_game_won():
                PopUpGUI.create_pop_up_gui_and_show("Victory !","Congratulations, you have won !", "Reset the game",self.__reset_game_ui)
            elif self.__game.is_game_lost():
                PopUpGUI.create_pop_up_gui_and_show("Defeat !","Suck it up looser", "Reset the game",self.__reset_game_ui)
            else:
                PopUpGUI.create_pop_up_gui_and_show("Uhhh what ?","This window shouldn't show up bro", "Reset the game",self.__reset_game_ui)

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

class PopUpGUI:

    def __init__(self,title, text, button_text,button_action):
        self.__title = title
        self.__text = text
        self.__button_text = button_text
        self.__button_action = button_action
        self.__root = Tk()
        self.__root.title(self.__title)
        self.__frame = Frame(self.__root)
        self.__text = Label(self.__frame, text=self.__text)
        self.__launch_button = Button(self.__frame, text=self.__button_text, activebackground="blue", fg="red",
                                      command=self.__button_action)



    def show(self):
        self.__text.pack()
        self.__launch_button.pack()
        self.__frame.pack()
        self.__root.mainloop()
        self.__root.focus_set()

    @staticmethod
    def create_pop_up_gui_and_show(title, text, button_text,action):
        popup = PopUpGUI(title,text,button_text,action)
        popup.show()

class ConfigGUI:

    def __init__(self):
        self.__root = Tk()
        self.__root.title("Welcome to 2048 !")
        self.__frame = Frame(self.__root)
        self.__theme = StringVar(self.__root)
        self.__theme.set(DEFAULT_THEME_CHOICE)
        self.__grid_size = StringVar(self.__root)
        self.__grid_size.set(DEFAULT_GRID_SIZE_CHOICE)
        self.__welcome_text = Label(self.__frame, text="Welcome in 2048 !")
        self.__explanation_text = Label(self.__frame, text="Please configure your game  :)")
        self.__grid_size_text = Label(self.__frame, text="Please enter a grid size :")
        self.__grid_size_choices = OptionMenu(self.__frame, self.__grid_size, *GRID_SIZE_CHOICES)
        self.__theme_text = Label(self.__frame, text="Please choose a theme :")
        self.__theme_choices = OptionMenu(self.__frame, self.__theme, *THEMES_CHOICES)
        self.__launch_button = Button(self.__frame, text="Play !", activebackground="blue", fg="red",
                                      command=self.__launch_game)

    @staticmethod
    def create_config_gui_and_show():
        gui = ConfigGUI()
        gui.show()

    def show(self):
        self.__welcome_text.pack()
        self.__explanation_text.pack()
        self.__grid_size_text.pack()
        self.__grid_size_choices.pack()
        self.__theme_text.pack()
        self.__theme_choices.pack()
        self.__launch_button.pack()
        self.__frame.pack()
        self.__root.mainloop()
        self.__root.focus_set()

    def __launch_game(self):
        game = Game.create_game(int(self.__grid_size.get()), MAX_VALUE)
        GameGUI.create_game_gui_and_show(game, THEMES[self.__theme.get()])


def play():
    ConfigGUI.create_config_gui_and_show()


if __name__ == '__main__':
    play()
