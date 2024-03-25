#include "Bishop.h"

Bishop::Bishop(const Player& player, const Position& position)
: ChessPiece(player, position) {
    this->name = "Bishop";
    this->multipleMove = true;
    this->canJumpOverOthers = false;

    // Initializing possible moves for a bishop
    this->possibleRegularMoves = {
        {1, 1}, {1, -1}, {-1, 1}, {-1, -1}
    };
    // For Bishop, capture moves are the same as regular moves
    this->possibleCaptureMoves = this->possibleRegularMoves;
}
