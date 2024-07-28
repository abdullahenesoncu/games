#ifndef ROOK_H
#define ROOK_H

#include "ChessPiece.h"
#include <vector>
#include <memory>

class Rook : public ChessPiece, public std::enable_shared_from_this<Rook> {
public:
    Rook(const Player& player, const Position& position);
};

#endif // ROOK_H
