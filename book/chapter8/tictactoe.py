from __future__ import annotations
from typing import List
from enum import Enum
from board import Piece, Board, Move


class TTTPiece(Piece, Enum):
    X = "X"
    O = "O"
    E = " "

    @property
    def opposite(self) -> TTTPiece:
        if self == TTTPiece.X:
            return TTTPiece.O
        elif self == TTTPiece.O:
            return TTTPiece.X
        else:
            return TTTPiece.E

    def __str__(self) -> str:
        return self.value


class TTTBoard(Board):

    def __init__(
            self,
            position: List[TTTPiece] = [TTTPiece.E] * 9,
            turn: TTTPiece = TTTPiece.X) -> None:
        self.position: List[TTTPiece] = position
        self._turn: TTTPiece = turn

    @property
    def turn(self) -> Piece:
        return self._turn

    def move(self, location: Move) -> Board:
        temp_position: List[TTTPiece] = self.position.copy()
        temp_position[location] = self._turn
        return TTTBoard(temp_position, self._turn.opposite)

    @property
    def legal_moves(self) -> List[Move]:
        return [Move(l) for l in range(len(self.position)) if self.position[l] == TTTPiece.E]

    @property
    def is_win(self) -> bool:
        def is_winning_line(line):
            [a, b, c] = [self.position[idx] for idx in line]
            return a == b and a == c and a != TTTPiece.E

        lines = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]
        return any([is_winning_line(line) for line in lines])

    def evaluate(self, player: Piece) -> float:
        if self.is_win and self.turn == player:
            return -1
        elif self.is_win and self.turn != player:
            return 1
        else:
            return 0

    def __repr__(self) -> str:
        def make_line(indexes) -> str:
            chars = [str(self.position[idx]) for idx in indexes]
            return "|".join(chars) + "\n"

        sep_line = "-----\n"
        lines = [
            make_line([0, 1, 2]),
            sep_line,
            make_line([3, 4, 5]),
            sep_line,
            make_line([6, 7, 8]),
        ]
        return "".join(lines)
