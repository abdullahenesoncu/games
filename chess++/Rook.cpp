#include "Rook.h"

Rook::Rook(const Player& player, const Position& position)
: ChessPiece(player, position) {
    this->name = "Rook";
    this->multipleMove = true;
    this->canJumpOverOthers = false;

    // Initializing possible moves for a rook
    this->possibleRegularMoves = {
        {0, 1}, {1, 0}, {0, -1}, {-1, 0}
    };
    // For Rook, capture moves are the same as regular moves
    this->possibleCaptureMoves = this->possibleRegularMoves;
}