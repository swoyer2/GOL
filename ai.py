import grid
import random
import dataframe

GRID_SIZE = (16, 16)
NEIGHBOR_COUNT = 5
ITERATIONS = 100000
GLOBAL_DF = dataframe.get_df()

USED_CACHE_COUNT = 0
TOTAL_SEARCHED = 0

mutation_rate = 1

# Create a random initial seed (a 2D grid)
def generate_random_seed(size):
    # Generate the seed as a list of lists of '0', '1', '2'
    seed_list = [[random.choice(['0', '1']) for _ in range(size)] for _ in range(size)]

    # Convert the 2D list into a string with rows joined by
    seed_string = ''.join([''.join(row) for row in seed_list])
    
    return seed_string

def bin_to_board(bin):
    board = []
    for bit in bin:
        board.append(int(bit))
    return board

def increment_binary_string(bin_str):
    num = int(bin_str, 2)
    num += 1
    return bin(num)[2:]

def evaluate(seed) -> int:
    global GLOBAL_DF
    global USED_CACHE_COUNT
    global TOTAL_SEARCHED
    score = dataframe.get_score(GLOBAL_DF, seed)
    if score != None:
        USED_CACHE_COUNT += 1
        TOTAL_SEARCHED += 1
        return score
    
    board = grid.Grid(GRID_SIZE)
    board.set_seed(seed)
    count = 0
    while not board.is_repeating_seed():
        board.set_new_board_state()
        score = dataframe.get_score(GLOBAL_DF, board.get_seed())
        if score != None:
            count += score
            USED_CACHE_COUNT += 1
            break
        count += 1
    TOTAL_SEARCHED += 1
    GLOBAL_DF = dataframe.add_score(GLOBAL_DF, seed, count)
    return count

# Generate neighbors by toggling a random cell
def generate_neighbors(seed, num_neighbors=NEIGHBOR_COUNT):
    global mutation_rate
    neighbors = []
    seed_list = [list(row) for row in seed.split('\n')]
    positions = [(i, j) for i in range(len(seed_list)) for j in range(len(seed_list[i]))]

    for _ in range(num_neighbors):
        new_seed_list = [row[:] for row in seed_list]
        num_changes = random.randint(1, int(mutation_rate))
        random_positions = random.sample(positions, num_changes)

        for i, j in random_positions:
            new_seed_list[i][j] = random.choice(['0', '1'])

        new_seed = '\n'.join([''.join(row) for row in new_seed_list])
        neighbors.append(new_seed)

    return neighbors

# Hill climbing algorithm to maximize the score
def hill_climb(seed, iterations=ITERATIONS):
    global mutation_rate
    global USED_CACHE_COUNT
    global TOTAL_SEARCHED
    current_seed = seed
    current_score = evaluate(current_seed)
    
    for _ in range(iterations):
        print(f"""Current iteration: {_} 
Best Score: {current_score} 
Mutation Rate: {int(mutation_rate)} 
Total Searched: {TOTAL_SEARCHED}
Used Cache Count: {USED_CACHE_COUNT}
Cache Success %: {round(USED_CACHE_COUNT / TOTAL_SEARCHED, 2)}\n""")
        neighbors = generate_neighbors(current_seed)
        best_neighbor = max(neighbors, key=evaluate)
        best_score = evaluate(best_neighbor)
        
        # If we found a better seed, update the current seed
        if best_score > current_score:
            current_seed = best_neighbor
            current_score = best_score
            mutation_rate = 1
        else:
            mutation_rate = min(mutation_rate + 0.25, GRID_SIZE[0] * GRID_SIZE[1] - 1)
        
        if _ % 100 == 0:
            dataframe.save_df(GLOBAL_DF)
    
    return current_seed, current_score

def scan_from_starting_seed(seed, iterations=ITERATIONS):
    global TOTAL_SEARCHED
    current_seed = seed
    current_score = evaluate(current_seed)
    
    for _ in range(iterations):
        print(f"""Current iteration: {_} 
Current Seed: {int(seed, 2)}
Best Score: {current_score} 
Mutation Rate: {int(mutation_rate)} 
Total Searched: {TOTAL_SEARCHED}\n""")
        score = evaluate(seed)
        seed = increment_binary_string(seed)
        
        # If we found a better seed, update the current seed
        if  score > current_score:
            current_seed = seed
            current_score = score
        
        if _ % 100 == 0:
            dataframe.save_df(GLOBAL_DF)
    
    return current_seed, current_score

# Main execution
size = GRID_SIZE[0]
initial_seed = generate_random_seed(size)

#scan_from_starting_seed("1001011000000")

optimized_seed, optimized_score = hill_climb("0"*32*32)

print("Optimized Seed:")
print(optimized_seed)
print("Optimized Score:", optimized_score)
dataframe.save_df(GLOBAL_DF)

