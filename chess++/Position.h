#ifndef POSITION_H
#define POSITION_H

#include <string>

class PositionDelta {
public:
    int x, y;

    // Constructors
    PositionDelta(int x = 0, int y = 0);
};

class Position {
public:
    int x, y;

    // Constructors
    Position(int x = 0, int y = 0);
    Position(const std::string& posStr);

    // Convert to string representation
    std::string toString() const;

    // Operator overloads
    PositionDelta operator+(const Position& other) const;
    PositionDelta operator-(const Position& other) const;
    bool operator==(const Position& other) const;
};

#endif // POSITION_H
