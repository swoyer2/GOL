import square
import random
import ctypes

so_file = "C:/Users/swoye/Desktop/Coding/GOL/solver.so"
c_functions = ctypes.CDLL(so_file)

SIZE_OF_SQUARE = 32

class Grid:
    def __init__(self, size: tuple):
        self.squares = {}
        self.offset_x = 96
        self.offset_y = 96
        self.size = size
        self.seed = None
        self.grid_info = self.init_grid(size) # list

        self.previous_seeds = []
    
    def init_grid(self, size: tuple) -> list:
        grid_info = []
        for y in range(size[1]):
            for x in range(size[0]):
                state = random.randint(0, 2)
                grid_info.append(state)
                self.add_square(x, y, state)
        
        return grid_info
    
    def set_seed(self, seed_str: str) -> None:
        self.seed = seed_str
        total_cells = self.size[0] * self.size[1]

        # Pad if needed
        seed_str = seed_str.zfill(total_cells)

        self.grid_info = []
        idx = 0
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                state = int(seed_str[idx])
                self.grid_info.append(state)
                self.add_square(x, y, state)
                idx += 1
    
    def get_seed(self) -> str:
        seed = ''.join(str(i) for i in self.grid_info)
        return seed
    
    def add_seed_to_previous_seeds(self) -> None:
        self.previous_seeds.append(self.get_seed())
    
    def is_repeating_seed(self) -> bool:
        if self.get_seed() in self.previous_seeds:
            return True
        return False

    def reload(self) -> None:
        self.squares = {}
        self.grid_info = self.init_grid(self.size)

    def clear_board(self) -> None:
        for x, y in self.squares:
            self.set_square_state(x, y, 0)
    
    def add_square(self, x, y, state):
        self.squares[(x, y)] = square.Square(state)
        self.set_square_pos(x, y)
    
    def set_square_pos(self, x, y):
        global SIZE_OF_SQUARE
        true_x = x * SIZE_OF_SQUARE + self.offset_x
        true_y = y * SIZE_OF_SQUARE + self.offset_y
        self.squares[(x, y)].set_pos(true_x, true_y)

    def get_square(self, x, y):
        return self.squares[(x, y)]
    
    def get_all_squares(self):
        all_squares = []
        for square_key in self.squares:
            all_squares.append(self.squares[square_key])
        return all_squares

    def get_state(self, x, y):
        x_max = self.size[0]
        if not self.is_valid_coordinate(x, y):
            return 0
        return self.grid_info[x_max * y + x]

    def is_valid_coordinate(self, x, y) -> bool:
        x_max = self.size[0]
        y_max = self.size[1]
        if x >= x_max:
            return False
        if y >= y_max:
            return False
        if x < 0 or y < 0:
            return False
        return True

    def bound_coordinate(self, x, y):
        x_max = self.size[0]
        y_max = self.size[1]
        new_coordinate = [x, y]
        if x >= x_max:
            new_coordinate[0] = 0
        if y >= y_max:
            new_coordinate[1] = 0
        if x < 0:
            new_coordinate[0] = x_max - 1
        if y < 0:
            new_coordinate[1] = y_max - 1

        return new_coordinate

    def set_square_state(self, x, y, state):
        x_max = self.size[0]
        self.grid_info[x_max * y + x] = state
        self.squares[(x, y)].set_image(state)

    def calculate_next_state(self) -> list[int]:
        # new_state = []
        # for y in range(self.size[1]):
        #     for x in range(self.size[0]):
        #         next_state.append(self.get_square_next_state(x, y))
        c_array = (ctypes.c_int * len(self.grid_info))(*self.grid_info)
        c_functions.get_next_state(c_array, self.size[0])
        new_state = list(c_array)
        return new_state

    def set_new_board_state(self):
        self.add_seed_to_previous_seeds()
        state = self.calculate_next_state()
        self.grid_info = state
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                self.squares[(x, y)].set_image(state[self.size[0] * y + x])


    def get_square_next_state(self, x, y) -> int:
        blue_count, pink_count = self.check_neighbor_count(x, y)
        neighbor_count = blue_count + pink_count
        if neighbor_count < 2:
            return 0
        if neighbor_count > 3:
            return 0
        if neighbor_count == 2 or neighbor_count == 3 and self.get_state(x, y) != 0:
            return self.get_state(x, y)
        if neighbor_count == 3 and self.get_state(x, y) == 0:
            return 1 if blue_count > pink_count else 2
        return 0

    # Returns number of blue and pink neighbors (blue, pink)
    def check_neighbor_count(self, x, y) -> list[int, int]:
        coordinates = [(x - 1, y), # left
                   (x + 1, y), # right
                   (x, y + 1), # down
                   (x, y - 1), # up
                   (x - 1, y - 1), # left up
                   (x + 1, y + 1), # right down
                   (x - 1, y + 1), # left down
                   (x + 1, y - 1)] # right up
        
        coordinates = [self.bound_coordinate(coordinate[0], coordinate[1]) for coordinate in coordinates]

        indexes = [coordinate[1] * self.size[0] + coordinate[0] for coordinate in coordinates] 

        neighbor_count = [0, 0]
        for index in indexes:
            if self.grid_info[index] == 1:
                neighbor_count[0] += 1
            elif self.grid_info[index] == 2:
                neighbor_count[1] += 1
        return neighbor_count
    
    def rotate_state(self, x, y):
        current_state = self.get_state(x, y)
        new_state = (current_state + 1) % 3
        self.set_square_state(x, y, new_state)

    def get_square_pos_from_mouse(self, mouse_pos: tuple):
        global SIZE_OF_SQUARE
        x_mouse, y_mouse = mouse_pos
        # Convert mouse position to grid coordinates
        grid_x = (x_mouse - self.offset_x) // SIZE_OF_SQUARE
        grid_y = (y_mouse - self.offset_y) // SIZE_OF_SQUARE

        if (grid_x, grid_y) in self.squares:
            return grid_x, grid_y
        return None, None

    def get_char_count(self, char) -> int:
        seed = self.get_seed()
        return seed.count(char)