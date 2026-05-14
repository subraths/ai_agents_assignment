from typing import Optional


def turn_on(device: str, room: Optional[str] = None) -> str:
    if room:
        return f"[MOCK] Turned ON {device} in {room}."
    return f"[MOCK] Turned ON {device}."


def turn_off(device: str, room: Optional[str] = None) -> str:
    if room:
        return f"[MOCK] Turned OFF {device} in {room}."
    return f"[MOCK] Turned OFF {device}."


def set_value(device: str, value: str, room: Optional[str] = None) -> str:
    if room:
        return f"[MOCK] Set {device} in {room} to {value}."
    return f"[MOCK] Set {device} to {value}."
