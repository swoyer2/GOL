# Directories
BUILD_DIR := ./build
SRC_DIR := ./src
INC_DIR := ./include
TEST_DIR := ./tests

# Compiler and Flags
CC := gcc
CFLAGS := -Wall -Wextra -I$(INC_DIR)

# Source and Object Files
SRCS := $(wildcard $(SRC_DIR)/*.c)
OBJS := $(SRCS:$(SRC_DIR)/%.c=$(BUILD_DIR)/%.o)

# Executable
PROG := GOL

# Rule to create the program from object files
$(PROG): $(OBJS)
	$(CC) $(OBJS) -o $(PROG)

# Rule to create object files from source files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

# Clean Rule to remove object files and the program
clean:
	rm -rf $(BUILD_DIR) $(PROG)

# Phony targets (not actual files)
.PHONY: clean
