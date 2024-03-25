#include "King.h"

King::King(const Player& player, const Position& position)
: ChessPiece(player, position) {
    this->name = "King";
    this->multipleMove = false;
    this->canJumpOverOthers = false;

    // Initializing possible moves for a king
    this->possibleRegularMoves = {
        {0, 1}, {1, 0}, {0, -1}, {-1, 0},
        {1, 1}, {1, -1}, {-1, 1}, {-1, -1}
    };
    // For King, capture moves are the same as regular moves
    this->possibleCaptureMoves = this->possibleRegularMoves;
}

bool King::canCastle(std::shared_ptr<Rook> rook, const Board& board) const {
    // Early exit if either the king or rook has moved
    if (this->moved || rook->hasMoved()) return false;

    // Check if the king is currently in check
    if (board.isCheck(this->getPlayer())) return false;

    Position rookPos = rook->getPosition();
    int direction = (rookPos.x > this->position.x) ? 1 : -1;
    int checkRange = (direction == -1) ? 3 : 2;

    // Check if the path is clear and no squares the king will cross are under attack
    for (int i = 1; i <= checkRange; ++i) {
        Position step = {this->position.x + i * direction, this->position.y};
        if (!board.isPathClear(this->position, rookPos) || board.isUnderAttack(step, this->getPlayer())) {
            return false;
        }
    }
    return true;
}

void King::castle(std::shared_ptr<Rook> rook, Board& board) {
    Position rookPos = rook->getPosition();
    int direction = (rookPos.x > this->position.x) ? 1 : -1;

    // Calculate new positions for the king and rook
    Position newKingPos = {this->position.x + 2 * direction, this->position.y};
    Position newRookPos = {newKingPos.x - direction, this->position.y}; // Rook moves next to the king

    // Perform the moves
    board.movePiece(shared_from_this(), newKingPos);
    board.movePiece(rook, newRookPos);
}