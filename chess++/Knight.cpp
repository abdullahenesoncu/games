#include "Knight.h"

Knight::Knight(const Player& player, const Position& position)
: ChessPiece(player, position) {
    this->name = "Knight";
    this->canJumpOverOthers = true;
    this->multipleMove = false;

    // Initializing possible moves for a knight
    this->possibleRegularMoves = {
        {1, 2}, {2, 1},
        {-1, 2}, {-2, 1},
        {-1, -2}, {-2, -1},
        {1, -2}, {2, -1}
    };
    // For Knight, capture moves are the same as regular moves
    this->possibleCaptureMoves = this->possibleRegularMoves;
}
