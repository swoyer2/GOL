#include <stdio.h>

#include "grid.h"

int main() {
    struct Grid grid;
    init_grid(&grid, 5, 5);  // Create a 5x5 grid
    set_grid_from_file(&grid, "input.txt");
    print_grid(grid);
    set_next_grid_state(&grid);
    printf("\n");
    print_grid(grid);
    output_grid_to_file(grid, "outputs/output.txt");
    printf("\nScore: %d\n", get_score(grid));

    // Free allocated memory
    free_grid(&grid);

    return 0;
}