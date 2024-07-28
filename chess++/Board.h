#ifndef BOARD_H
#define BOARD_H

#include <vector>
#include <memory>
#include <string>
// Assume all necessary piece and position includes are handled elsewhere
#include "Player.h"
#include "ChessPiece.h" // Base class for chess pieces
// Forward declarations for piece types
class Pawn;
class Rook;
class Knight;
class Bishop;
class Queen;
class King;

class MoveDetails {
public:
   std::shared_ptr<ChessPiece> movedPiece;
   Position fromPos;
   Position toPos;
   std::shared_ptr<ChessPiece> capturedPiece; // Use nullptr if no piece was captured
   int prevHalfMoveClock;
   int prevFullMoveNumber;
};

class Board {
public:
   Board(Player& player1, Player& player2);
   void addPiece(std::shared_ptr<ChessPiece> piece);
   void removePiece(std::shared_ptr<ChessPiece> piece);
   ChessPiece* getCell(Position pos) const;
   bool movePiece(std::shared_ptr<ChessPiece> piece, const Position& to, const std::string& additionalInput = "");
   void Board::moveSuccessful(std::shared_ptr<ChessPiece> piece, std::shared_ptr<ChessPiece> targetPiece, const Position& from, const Position& to);
   bool promotePawn(std::shared_ptr<ChessPiece> pawn, const std::string& promotionChoice);
   bool wouldBeInCheck(const ChessPiece* piece, const Position& pos) const;
   bool isCheck(const Player& player) const;
   bool isCheckmate(const Player& player) const;
   bool isGameOver() const;
   bool isDraw() const;
   bool isStalemate(const Player& player) const;
   void switchTurn();
   bool isPathClear(const Position& from, const Position& to) const;
   bool isUnderAttack(Position pos, const Player& player) const;
   std::string getCastlingAvailability() const;
   void setCastlingAvailability(const std::string& castling);
   std::string getEnPassantTarget() const;
   MoveDetails getLastMove() const;
   std::string boardToString() const;
   std::string boardToFEN() const;
   static Board boardFromFEN(const std::string& fen);

private:
   std::vector<std::shared_ptr<ChessPiece>> pieces;
   Player* currentTurn;
   std::vector<Player> players;
   MoveDetails lastMove;
   int halfMoveClock;
   int fullMoveNumber;
};

#endif // BOARD_H
