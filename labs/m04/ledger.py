"""Two ledgers. One of them ignores withdrawals."""

from __future__ import annotations


def buggy(events: list[tuple[str, int]]) -> int:
    balance = 0
    for kind, amount in events:
        if kind == "deposit" and amount >= 0:
            balance += amount
    return balance


def fixed(events: list[tuple[str, int]]) -> int:
    balance = 0
    for kind, amount in events:
        if amount < 0:
            raise ValueError("amount must be non-negative")
        if kind == "deposit":
            balance += amount
        elif kind == "withdraw":
            if amount > balance:
                continue
            balance -= amount
        else:
            raise ValueError(f"unknown event {kind}")
    return balance
