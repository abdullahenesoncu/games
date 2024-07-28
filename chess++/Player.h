#ifndef PLAYER_H
#define PLAYER_H

#include <vector>
#include <string>
#include <memory>
// Forward declaration of ChessPiece to avoid circular dependency
class ChessPiece;

class Player {
private:
    std::string name;
    std::string color; // 'white' or 'black'
    std::vector<std::shared_ptr<ChessPiece>> pieces; // Pieces that belong to the player

public:
    // Constructor
    Player(const std::string& name, const std::string& color);

    // Add a piece to the player's collection
    void addPiece(const std::shared_ptr<ChessPiece>& piece);

    // Remove a piece from the player's collection
    void removePiece(const std::shared_ptr<ChessPiece>& piece);

    // Getters
    const std::string& getName() const;
    const std::string& getColor() const;
};

#endif // PLAYER_H
