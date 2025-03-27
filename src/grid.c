#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>

#include "grid.h"

void init_grid(struct Grid *grid, int x_size, int y_size) {
    grid -> x_size = x_size;
    grid -> y_size = y_size;
    grid -> cells = (struct Cell *)malloc(x_size * y_size * sizeof(struct Cell));

    if (grid->cells == NULL) {
        printf("Memory allocation failed!\n");
        exit(1); // Exit if memory allocation fails
    }

    for (int i = 0; i < x_size * y_size; i++) {
        grid->cells[i].coordinate.x = i % x_size;
        grid->cells[i].coordinate.y = i / x_size;
        grid->cells[i].alive = false; // Set initial state to dead
        grid->cells[i].player = 0; // 0 means no player
    }
}

void free_grid(struct Grid *grid) {
    free(grid->cells);
}

void print_grid(struct Grid grid) {
    // Dynamically allocate memory for the output string
    int output_str_size = grid.x_size * grid.y_size + grid.y_size + 1;  // +y for newlines and +1 for '\0'
    char *output_str = malloc(output_str_size * sizeof(char));

    if (output_str != NULL) {
        get_grid_str(grid, output_str);
        printf("%s", output_str);
        free(output_str);
    } else {
        printf("Memory allocation failed!\n");
    }
}

void output_grid_to_file(struct Grid grid, char *file_name) {
    // Dynamically allocate memory for the output string
    int output_str_size = grid.x_size * grid.y_size + grid.y_size + 1;  // +y for newlines and +1 for '\0'
    char *output_str = malloc(output_str_size * sizeof(char));

    FILE *file = fopen(file_name, "w");

    if (output_str != NULL) {
        get_grid_str(grid, output_str);

        if (file == NULL) {
            printf("Error opening the file!\n");
        }
        else {
            fprintf(file, "%s", output_str);
            fclose(file);
        }
        
        free(output_str);
    } 
    else {
        printf("Memory allocation failed!\n");
    }
}

void get_grid_str(struct Grid grid, char *output_string) {
    int string_index = 0;
    for (int y = 0; y < grid.y_size; y++) {
        for (int x = 0; x < grid.x_size; x++) {
            struct Coordinate cell_coordinate = {x, y};
            int cell_index = get_index_from_coordinate(grid, cell_coordinate);
            // Convert player number to character
            output_string[string_index] = grid.cells[cell_index].player + '0';
            string_index++;
        }
        output_string[string_index] = '\n';
        string_index++;
    }
    output_string[string_index] = '\0';
}

void set_grid_from_file(struct Grid *grid, char *file_name) {
    FILE *file = fopen(file_name, "r");

    if (file == NULL) {
        printf("Error opening the file!\n");
        return;
    }

    int x = 0, y = 0;
    char status;

    while (fscanf(file, "%c", &status) == 1) {
        if (status == '\n' || status == ' ') {
            continue;
        }

        if (status != '0' && status != '1' && status != '2') {
            printf("Invalid status at position (%d, %d): %c. Only '0', '1' or '2' are valid.\n", x, y, status);
            fclose(file);
            return;
        }

        struct Coordinate coordinate = {x, y};
        int index = get_index_from_coordinate(*grid, coordinate);
        grid->cells[index].alive = (status != '0');
        grid->cells[index].player = status - '0';  // Convert char to int

        x++;
        if (x >= grid->x_size) {
            x = 0;
            y++;
            if (y >= grid->y_size) {
                break;
            }
        }
    }

    fclose(file);
}

bool is_valid_coordinate(struct Grid grid, struct Coordinate coordinate) {
    if (coordinate.x < 0 || coordinate.y < 0) {
        return false;
    }
    
    if (coordinate.x > grid.x_size - 1 || coordinate.y > grid.y_size - 1) {
        return false;
    }
    return true;
}

int get_index_from_coordinate(struct Grid grid, struct Coordinate coordinate) {
    // Checks if the coordinate is not valid and returns -1 if it is not so it can be dealt with
    if (!is_valid_coordinate(grid, coordinate)) {
        return -1;
    }

    int index = coordinate.x + coordinate.y * grid.x_size;
    return index;
}

int get_alive_neighbor_count(struct Grid grid, int x, int y) {
    struct Coordinate U = {x, y - 1};
    struct Coordinate L = {x - 1, y};
    struct Coordinate R = {x + 1, y};
    struct Coordinate D = {x, y + 1};
    struct Coordinate UL = {x - 1, y - 1};
    struct Coordinate UR = {x + 1, y - 1};
    struct Coordinate DL = {x - 1, y + 1};
    struct Coordinate DR = {x + 1, y + 1};
    struct Coordinate neighbors[] = {U, L, R, D, UL, UR, DL, DR};

    int count_of_neighbors = 0;
    for (int i = 0; i < 8; i++) {
        int neighbor_index = get_index_from_coordinate(grid, neighbors[i]);
        if (neighbor_index != -1) {
            struct Cell neighbor_cell = grid.cells[neighbor_index];
            if (neighbor_cell.alive) {
                count_of_neighbors += 1;
            }
        }
    }
    return count_of_neighbors;
}

int get_player_from_neighbors(struct Grid grid, int x, int y) {
    struct Coordinate U = {x, y - 1};
    struct Coordinate L = {x - 1, y};
    struct Coordinate R = {x + 1, y};
    struct Coordinate D = {x, y + 1};
    struct Coordinate UL = {x - 1, y - 1};
    struct Coordinate UR = {x + 1, y - 1};
    struct Coordinate DL = {x - 1, y + 1};
    struct Coordinate DR = {x + 1, y + 1};
    struct Coordinate neighbors[] = {U, L, R, D, UL, UR, DL, DR};

    int player_1_count = 0;
    for (int i = 0; i < 8; i++) {
        int neighbor_index = get_index_from_coordinate(grid, neighbors[i]);
        if (neighbor_index != -1) {
            struct Cell neighbor_cell = grid.cells[neighbor_index];
            if (neighbor_cell.player == 1) {
                player_1_count += 1;
            }
        }
    }
    if (player_1_count > 1) {
        return 1;
    }
    else {
        return 2;
    }
}

int get_next_cell_state(struct Grid grid, int cell_index) { 
    struct Cell cell = grid.cells[cell_index];   
    int neighbor_count = get_alive_neighbor_count(grid, cell.coordinate.x, cell.coordinate.y);
    if (neighbor_count < 2) {
        return 0;
    }
    else if (neighbor_count == 2 && cell.alive) {
        return grid.cells[cell_index].player;
    }
    else if (neighbor_count == 3 ) {
        return get_player_from_neighbors(grid, cell.coordinate.x, cell.coordinate.y);
    }
    else if (neighbor_count > 3) {
        return 0;
    }
    return 0;
}

void get_next_grid_state(struct Grid grid, struct Cell *new_cells_array) {
    for (int i = 0; i < grid.x_size * grid.y_size; i++) {
        int next_cell_state = get_next_cell_state(grid, i);
        new_cells_array[i].alive = (next_cell_state != 0);
        new_cells_array[i].player = next_cell_state;
    }
}

void set_next_grid_state(struct Grid *grid) {
    struct Cell *new_cell_array = (struct Cell *)malloc(grid->x_size * grid->y_size * sizeof(struct Cell));
    get_next_grid_state(*grid, new_cell_array);
    free(grid->cells);
    grid -> cells = new_cell_array;
}

int get_score(struct Grid grid) {
    int score = 0;
    for (int i = 0; i < grid.x_size * grid.y_size; i++) {
        if (grid.cells[i].player == 1) {
            score += 1;
        }
        else if (grid.cells[i].player == 2) {
            score -= 1;
        }
    }
    return score;
}