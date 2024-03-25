#include "ChessPiece.h"
#include "Board.h" // Including the complete declaration

ChessPiece::ChessPiece(const Player& player, const Position& pos)
    : player(player), position(pos), canJumpOverOthers(false), multipleMove(false), moved(false) {
    // Initialize possible moves here if they're common for all pieces
    // Otherwise, they should be initialized in the constructor of derived classes
}

bool ChessPiece::canMove(const Board& board, const Position& newPos, bool ctrlCheck) const {
    // Check if the new position is the same as the current position
    if (newPos == position) {
        return false;
    }

    // Check if the new position is out of bounds
    if (newPos.x < 0 || newPos.x > 7 || newPos.y < 0 || newPos.y > 7) {
        return false;
    }

    // Calculate the difference in position
    PositionDelta diff = {newPos.x - position.x, newPos.y - position.y};

    // Check if the move is in the possible moves list for pieces that move to a single square
    if (!multipleMove) {
        auto it = std::find(possibleRegularMoves.begin(), possibleRegularMoves.end(), diff);
        if (it == possibleRegularMoves.end()) {
            return false;
        }
    } else {
        // For pieces that can move multiple squares, check if the move is valid
        bool ok = false;
        for (int i = 1; i <= 8; ++i) {
            if (diff.x % i == 0 && diff.y % i == 0) {
                Position step = {diff.x / i, diff.y / i};
                if (std::find(possibleRegularMoves.begin(), possibleRegularMoves.end(), step) != possibleRegularMoves.end()) {
                    ok = true;
                    break;
                }
            }
        }
        if (!ok) {
            return false;
        }
    }

    // Check if there is a piece at the new position belonging to the same player
    ChessPiece* pieceAtNewPos = board.getCell(newPos);
    if (pieceAtNewPos && pieceAtNewPos->getPlayer() == player) {
        return false;
    }

    // If ctrlCheck is true, check if the move would put or leave the king in check
    if (ctrlCheck && board.wouldBeInCheck(this, newPos)) {
        return false;
    }

    // Check if the piece can jump over others or if the path to the new position is clear
    return canJumpOverOthers || board.isPathClear(position, newPos);
}

void Board::moveSuccessful(std::shared_ptr<ChessPiece> piece, std::shared_ptr<ChessPiece> targetPiece, const Position& from, const Position& to) {
    // Fill the lastMove structure with details of the move
    lastMove.movedPiece = piece;
    lastMove.fromPos = from;
    lastMove.toPos = to;
    lastMove.capturedPiece = targetPiece;
    lastMove.prevHalfMoveClock = halfMoveClock;
    lastMove.prevFullMoveNumber = fullMoveNumber;

    // Reset halfMoveClock if a pawn moves or a capture occurs; otherwise, increment it
    if (dynamic_cast<Pawn*>(piece.get()) != nullptr || targetPiece != nullptr) {
        halfMoveClock = 0;
    } else {
        halfMoveClock += 1;
    }

    // Increment fullMoveNumber after black's turn
    if (currentTurn->getColor() == "black") {
        fullMoveNumber += 1;
    }

    // Switch turns
    switchTurn();
}

bool ChessPiece::canThreat(const Board& board, const Position& newPos, bool ctrlCheck) const {
    // Simplistically, canThreat mirrors canMove if no specific threat rules apply
    return canMove(board, newPos, ctrlCheck);
}

bool ChessPiece::canCapture(const Board& board, const Position& newPos, bool ctrlCheck) const {
    // A piece can capture if it can move to the new position and there is an opponent's piece
    if (canMove(board, newPos, ctrlCheck)) {
        ChessPiece* targetPiece = board.getCell(newPos);
        return targetPiece && targetPiece->getPlayer() != this->getPlayer();
    }
    return false;
}

void ChessPiece::move(const Position& newPos) {
    position = newPos;
    moved = true;
}

bool ChessPiece::hasMoved() {
   return moved;
}

Player ChessPiece::getPlayer() const {
    return player;
}

Position ChessPiece::getPosition() const {
    return position;
}

std::string ChessPiece::toString() const {
    // Simple conversion to string representation
    return "( " + player.getName() + " " + name + " at " + position.toString() + " )";
}
