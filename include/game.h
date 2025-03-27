#ifndef GAME_H
#define GAME_H

#include "grid.h"
#include "player.h"

struct Game {
    struct Grid grid;
    struct Player player1;
    struct Player player2;
};

#endif