#include "Board.h"
#include "ChessPiece.h"
#include "Position.h"
// Include specific chess piece headers if necessary

Board::Board(Player& player1, Player& player2) 
    : currentTurn(&player1), players{player1, player2}, halfMoveClock(0), fullMoveNumber(1) {
}

void Board::addPiece(std::shared_ptr<ChessPiece> piece) {
    pieces.push_back(piece);
    piece->getPlayer().addPiece(piece);
}

void Board::removePiece(std::shared_ptr<ChessPiece> piece) {
    auto it = std::find(pieces.begin(), pieces.end(), piece);
    if (it != pieces.end()) {
        pieces.erase(it);
    }

    piece->getPlayer().removePiece(piece);
}

ChessPiece* Board::getCell(Position pos) const {
    for (const auto& piece : pieces) {
        if (piece->getPosition() == pos) {
            return piece.get();
        }
    }
    return nullptr;
}

bool Board::movePiece(std::shared_ptr<ChessPiece> piece, const Position& to, const std::string& additionalInput) {
    if (piece->getPlayer() != currentTurn) {
        return false;
    }

    Position from = piece->getPosition();
    ChessPiece* targetPiece = getCell(to);

    // Check for castle move (for King)
    if (auto king = dynamic_cast<King*>(piece.get()); king && std::abs(to.x - from.x) == 2) {
        Position rookPos = (to.x < from.x) ? Position{0, from.y} : Position{7, from.y};
        ChessPiece* rook = getCell(rookPos);
        if (rook && king->canCastle(rook, *this)) {
            king->castle(rook);
            // Assuming moveSuccessful updates necessary state
            moveSuccessful(piece, targetPiece, from, to);
            return true;
        }
    }

    // Check for en passant (for Pawn)
    if (auto pawn = dynamic_cast<Pawn*>(piece.get()); pawn && pawn->canEnpassant(to, *this)) {
        pawn->enpassant(to, *this);
        moveSuccessful(piece, targetPiece, from, to);
        return true;
    }

    // Normal Move
    if (!piece->canMove(*this, to, true)) {
        return false;
    }

    // Move the piece and handle captures
    if (targetPiece && piece->canCapture(*this, to, true)) {
        // Assuming removePiece handles removal from the board's and player's piece lists
        removePiece(targetPiece);
    }

    piece->move(to);

    // Pawn Promotion Logic
    if (auto pawn = dynamic_cast<Pawn*>(piece.get()); pawn && (to.y == 0 || to.y == 7)) {
        // Assuming promotePawn handles the promotion logic
        if (!promotePawn(piece, additionalInput)) {
            return false; // Promotion failed or was invalid
        }
    }

    moveSuccessful(piece, targetPiece, from, to);
    return true;
}

void Board::switchTurn() {
    // Switch the current turn between the two players
    currentTurn = (currentTurn == &players[0]) ? &players[1] : &players[0];
}

