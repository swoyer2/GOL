#include "player.h"

void init_player(struct Player *player) {
    player -> edit_count = 0;
}

void increment_edit_count(struct Player *player) {
    player -> edit_count++;
}