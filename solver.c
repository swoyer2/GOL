int x_from_index(int index, int grid_size_x)
{
    return index % grid_size_x;
}

int y_from_index(int index, int grid_size_x)
{
    return index / grid_size_x;
}

int index_from_coordinate(int x, int y, int grid_size_x, int grid_size_y)
{
    if (x < 0)
        x = grid_size_x - 1;
    else if (x >= grid_size_x)
        x = 0;

    if (y < 0)
        y = grid_size_y - 1;
    else if (y >= grid_size_y)
        y = 0;

    return y * grid_size_x + x;
}

void get_next_state(int *grid, int grid_size_x)
{
    int grid_size_y = grid_size_x; // assuming square grid
    int alive_neighbor_counts[16 * 16] = {0};

    for (int i = 0; i < grid_size_x * grid_size_y; i++)
    {
        int x = x_from_index(i, grid_size_x);
        int y = y_from_index(i, grid_size_x);

        int neighbor_x[8] = {x - 1, x, x + 1, x - 1, x + 1, x - 1, x, x + 1};
        int neighbor_y[8] = {y - 1, y - 1, y - 1, y, y, y + 1, y + 1, y + 1};

        for (int n = 0; n < 8; n++)
        {
            int ni = index_from_coordinate(neighbor_x[n], neighbor_y[n], grid_size_x, grid_size_y);
            if (grid[ni] == 1)
                alive_neighbor_counts[i]++;
        }
    }

    for (int i = 0; i < grid_size_x * grid_size_y; i++)
    {
        if (grid[i] == 1)
        {
            if (alive_neighbor_counts[i] < 2 || alive_neighbor_counts[i] > 3)
                grid[i] = 0;
            // else stays alive (2 or 3)
        }
        else
        {
            if (alive_neighbor_counts[i] == 3)
                grid[i] = 1;
        }
    }
}
