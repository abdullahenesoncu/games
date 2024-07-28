#ifndef PAWN_H
#define PAWN_H

#include "ChessPiece.h"
#include <memory>

class Pawn : public ChessPiece, public std::enable_shared_from_this<Pawn> {
public:
    // Constructor initializing the pawn with its player and position
    Pawn(const Player& player, const Position& position);

    // Override canMove method to implement pawn-specific movement logic
    bool canMove(const Board& board, const Position& newPos, bool ctrlCheck = true) const override;

    // Implement the en passant capture move
    bool canEnpassant(const Board& board, const Position& newPos) const;
    void enpassant(Board& board, const Position& newPos);
};

#endif // PAWN_H
