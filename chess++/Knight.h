#ifndef KNIGHT_H
#define KNIGHT_H

#include "ChessPiece.h"
#include <memory>

class Knight : public ChessPiece, public std::enable_shared_from_this<Knight> {
public:
    Knight(const Player& player, const Position& position);
};

#endif // KNIGHT_H
