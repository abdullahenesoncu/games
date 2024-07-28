#ifndef KING_H
#define KING_H

#include "ChessPiece.h"
#include "Position.h"
#include "Board.h" // Assume the Board class has methods like isCheck, isPathClear, isUnderAttack
#include "Rook.h"
#include <memory>

class King : public ChessPiece {
public:
    // Constructor initializing the King with its player and position
    King(const Player& player, const Position& position);

    // Check if the king can perform castling with a given rook
    bool canCastle(std::shared_ptr<Rook> rook, const Board& board) const;

    // Perform the castling move
    void castle(std::shared_ptr<Rook> rook, Board& board);
};

#endif // KING_H
