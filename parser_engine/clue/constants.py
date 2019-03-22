from enum import IntEnum


class ClueStatus(IntEnum):
    PENDING = 0
    RUNNING = 1
    SUCCESS = 200
    FAILED = 500
