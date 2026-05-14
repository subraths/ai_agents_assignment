from typing import Optional, Dict, Tuple

# key: (device, room)
DEVICE_STATE: Dict[Tuple[str, Optional[str]], Dict[str, Optional[str]]] = {}


def _key(device: str, room: Optional[str]) -> Tuple[str, Optional[str]]:
    return (device.lower(), room.lower() if room else None)


def turn_on(device: str, room: Optional[str] = None) -> str:
    k = _key(device, room)
    DEVICE_STATE.setdefault(k, {"power": "OFF", "value": None})
    DEVICE_STATE[k]["power"] = "ON"
    return (
        f"[MOCK] Turned ON {device} in {room}."
        if room
        else f"[MOCK] Turned ON {device}."
    )


def turn_off(device: str, room: Optional[str] = None) -> str:
    k = _key(device, room)
    DEVICE_STATE.setdefault(k, {"power": "OFF", "value": None})
    DEVICE_STATE[k]["power"] = "OFF"
    return (
        f"[MOCK] Turned OFF {device} in {room}."
        if room
        else f"[MOCK] Turned OFF {device}."
    )


def set_value(device: str, value: str, room: Optional[str] = None) -> str:
    k = _key(device, room)
    DEVICE_STATE.setdefault(k, {"power": "OFF", "value": None})
    DEVICE_STATE[k]["value"] = value
    return (
        f"[MOCK] Set {device} in {room} to {value}."
        if room
        else f"[MOCK] Set {device} to {value}."
    )


def get_status(device: str, room: Optional[str] = None) -> str:
    k = _key(device, room)
    state = DEVICE_STATE.get(k)
    if not state:
        return (
            f"[MOCK] No state found for {device} in {room}."
            if room
            else f"[MOCK] No state found for {device}."
        )
    power = state.get("power", "UNKNOWN")
    value = state.get("value")
    if room:
        return f"[MOCK] {device} in {room}: power={power}, value={value}"
    return f"[MOCK] {device}: power={power}, value={value}"
