#ifndef GRID_H
#define GRID_H

#include <stdbool.h>
#include <stdio.h>
#include <stdio.h>

struct Coordinate {
    int x;
    int y;
};

struct Cell {
    struct Coordinate coordinate;
    bool alive;
    int player;
};

struct Grid {
    int x_size;
    int y_size;
    struct Cell *cells;
};

// Function to initialize the grid
void init_grid(struct Grid *grid, int x_size, int y_size);

void free_grid(struct Grid *grid);

// Prints grid out with 1 being alive and 0 being dead
void print_grid(struct Grid grid);

// Output the grid to a file how it would appear as a string
void output_grid_to_file(struct Grid grid, char *file_name);

// Sets grid from a file, format the file like the print output
void set_grid_from_file(struct Grid *grid, char *file_name);

// Converts provided string to a string representation of the grid
// The output_string has to be the length of x*y (area) + y (new lines) + 1 (\0 char)
void get_grid_str(struct Grid grid, char *output_string);

// Checks if coordinate is valid, needs the grid for information on dimensions
bool is_valid_coordinate(struct Grid grid, struct Coordinate coordinate);

// Gets index from coordinate, needs the grid for information on dimensions
int get_index_from_coordinate(struct Grid grid, struct Coordinate coordinate);

// Get count of neighbors of (x,y) that are alive
int get_alive_neighbor_count(struct Grid grid, int x, int y);

// Get the player that the new cell will become based on the cell.player of surrounding cells
int get_player_from_neighbors(struct Grid grid, int x, int y);

// Gets the next cell state based on the rules of GOL (and additional rules)
int get_next_cell_state(struct Grid grid, int cell_index);

// Sets the next grid state based on current state
void set_next_grid_state(struct Grid *grid);

// Returns the score of the grid, +score means player 1 is winning -score means player 2 is winning
int get_score(struct Grid grid);

#endif
