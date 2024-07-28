#include "Position.h"
#include <stdexcept>

PositionDelta::PositionDelta(int x, int y) : x(x), y(y) {}

Position::Position(int x, int y) : x(x), y(y) {}

Position::Position(const std::string& posStr) {
    if (posStr.length() != 2 || posStr[0] < 'a' || posStr[0] > 'h' || posStr[1] < '1' || posStr[1] > '8') {
        throw std::invalid_argument("Invalid position string.");
    }
    x = posStr[0] - 'a';
    y = posStr[1] - '1';
}

// Converts the position back to a string representation
std::string Position::toString() const {
    return std::string(1, 'a' + x) + std::to_string(y + 1);
}

// Operator overloads
PositionDelta Position::operator+(const Position& other) const {
    return PositionDelta(x + other.x, y + other.y);
}

PositionDelta Position::operator-(const Position& other) const {
    return PositionDelta(x - other.x, y - other.y);
}

bool Position::operator==(const Position& other) const {
    return x == other.x && y == other.y;
}
