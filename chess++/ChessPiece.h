#ifndef CHESSPIECE_H
#define CHESSPIECE_H

#include <string>
#include <vector>
#include "Position.h" // Assume Position struct is defined elsewhere
#include "Board.h"    // Assume Board class is defined elsewhere with appropriate methods

class Board; // Forward declaration

class ChessPiece {
protected:
    Position position;
    Player player;
    std::vector<PositionDelta> possibleRegularMoves; // These might be set in the constructor of derived classes
    std::vector<PositionDelta> possibleCaptureMoves; // These might be set in the constructor of derived classes
    bool canJumpOverOthers;
    bool multipleMove;
    bool moved=false;
    std::string name;

public:
    ChessPiece(const Player& player, const Position& pos);

    // Methods to check piece movement capabilities
    virtual bool canMove(const Board& board, const Position& newPos, bool ctrlCheck = true) const = 0;
    bool canThreat(const Board& board, const Position& newPos, bool ctrlCheck = true) const;
    bool canCapture(const Board& board, const Position& newPos, bool ctrlCheck = true) const;

    void move(const Position& newPos);
    bool hasMoved();

    std::string toString() const;

    Player getPlayer() const;
    Position getPosition() const;

    virtual ~ChessPiece() = default;
};

#endif // CHESSPIECE_H
