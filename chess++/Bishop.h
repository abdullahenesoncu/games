#ifndef BISHOP_H
#define BISHOP_H

#include "ChessPiece.h"
#include <memory>

class Bishop : public ChessPiece, public std::enable_shared_from_this<Bishop> {
public:
    // Constructor initializing the bishop with its player and position
    Bishop(const Player& player, const Position& position);
};

#endif // BISHOP_H
