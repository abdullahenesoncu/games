#include "Pawn.h"
#include "Board.h"

Pawn::Pawn(const Player& player, const Position& position)
    : ChessPiece(player, position) {}

bool Pawn::canMove(const Board& board, const Position& newPos, bool ctrlCheck) const {
    // If the cell is occupied, pawn cannot move
    if (board.getCell(newPos))
        return false;

    // If the pawn hasn't moved yet and it's moving two squares forward
    if (!moved && (newPos.x - position.x) == 0 && (newPos.y - position.y) == (2 * direction)) {
        // Check if the path is clear and it's not putting own king in check
        if (board.wouldBeInCheck(shared_from_this(), newPos) || !board.isPathClear(position, newPos))
            return false;
        return true;
    }

    // En Passant Condition
    if (canEnpassant(board, newPos))
        return true;

    // Delegate to the base class method for regular moves
    return ChessPiece::canMove(board, newPos, ctrlCheck);
}

bool Pawn::canEnpassant(const Board& board, const Position& newPos) const {
    // Check if the last move was a pawn double-step from the starting position
    if (board.getLastMove().movedPiece == nullptr)
        return false;

    const auto lastMove = board.getLastMove();
    const auto lastPiece = lastMove->movedPiece;
    const auto lastFromPos = lastMove->fromPos;
    const auto lastToPos = lastMove->toPos;

    if (lastPiece->getName() != "Pawn")
        return false;

    const auto lastXFrom = lastFromPos.x;
    const auto lastYFrom = lastFromPos.y;
    const auto lastXTo = lastToPos.x;
    const auto lastYTo = lastToPos.y;

    // Check if the last move was a double step from the starting position
    if (std::abs(lastYTo - lastYFrom) == 2 && lastYTo == position.y) {
        if (newPos.x == lastXTo && newPos.y == position.y + direction &&
            board.getCell(lastXTo, lastYTo + direction) == nullptr) {
            return true;
        }
    }
    return false;
}

void Pawn::enpassant(Board& board, const Position& newPos) {
    const auto lastMove = board.getLastMove();
    const auto lastPiece = lastMove.movedPiece;

    if (!board.removePiece(lastPiece)) {
        // Handle error or do nothing
    }

    lastPiece->getPlayer()->removePiece(lastPiece);
    move(newPos);
}
