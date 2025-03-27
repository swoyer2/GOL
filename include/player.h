#ifndef PLAYER_H
#define PLAYER_H

struct Player {
    int edit_count;
};

void init_player(struct Player *player);

void increment_edit_count(struct Player *player);

#endif