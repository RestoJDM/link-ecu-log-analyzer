from pathlib import Path
import re
import struct
import math

DS3 = b"ds3"
UTF16_ASCII = re.compile(rb"(?:(?:[\x20-\x7e]\x00){2,})")


def _utf16_strings(buf):
    out = []
    for match in UTF16_ASCII.finditer(buf):
        try:
            value = match.group().decode("utf-16le").rstrip("\x00")
            out.append((match.start(), value))
        except UnicodeDecodeError:
            pass
    return out


def _channel_meta(header):
    strings = _utf16_strings(header)

    # Observed PCLink ds3 metadata layout.
    name = next((s for pos, s in strings if pos == 215), None)
    unit = next((s for pos, s in strings if pos == 415), None)

    # Fallbacks for possible format revisions.
    if name is None:
        candidates = [(p, s) for p, s in strings if 180 <= p < 400]
        if candidates:
            name = candidates[0][1]

    if unit is None:
        candidates = [(p, s) for p, s in strings if 400 <= p < 620]
        if candidates:
            unit = candidates[0][1]

    return name, unit


def _float_pairs(payload):
    usable = len(payload) - (len(payload) % 8)
    payload = payload[:usable]

    times = []
    values = []

    for t, v in struct.iter_unpack("<ff", payload):
        if math.isfinite(t) and math.isfinite(v):
            times.append(float(t))
            values.append(float(v))

    return times, values


def load_llgx(path):
    """
    Returns a list of channel dictionaries:

    {
        "name": str | None,
        "unit": str | None,
        "occurrence": int,
        "time": [...],
        "value": [...]
    }
    """
    raw = Path(path).read_bytes()

    positions = []
    start = 0
    while True:
        pos = raw.find(DS3, start)
        if pos < 0:
            break
        positions.append(pos)
        start = pos + len(DS3)

    if not positions:
        raise ValueError("No ds3 channels found. File may not be a supported Link .llgx log.")

    channels = []
    occurrence_count = {}

    for i, marker_pos in enumerate(positions):
        block_start = marker_pos - 4

        if block_start < 0:
            continue

        block_size = struct.unpack_from("<I", raw, block_start)[0]

        # Typical ds3 block size observed in current PCLink logs is 645 bytes,
        # but use the value stored in the file rather than hard-coding it.
        if block_size < 32 or block_start + block_size > len(raw):
            continue

        header = raw[block_start:block_start + block_size]
        name, unit = _channel_meta(header)

        data_start = block_start + block_size
        if i + 1 < len(positions):
            data_end = positions[i + 1] - 4
        else:
            data_end = len(raw)

        if data_end < data_start:
            continue

        times, values = _float_pairs(raw[data_start:data_end])

        key = name or "<unnamed>"
        occurrence = occurrence_count.get(key, 0)
        occurrence_count[key] = occurrence + 1

        channels.append({
            "name": name,
            "unit": unit,
            "occurrence": occurrence,
            "time": times,
            "value": values,
        })

    return channels


def find_channels(channels, name):
    """Exact-name lookup returning all occurrences."""
    return [c for c in channels if c["name"] == name]


def find_channel_contains(channels, text):
    """Case-insensitive fallback lookup."""
    text = text.lower()
    return [
        c for c in channels
        if c["name"] and text in c["name"].lower()
    ]


def channel_names(channels):
    return [
        (c["name"], c["unit"], c["occurrence"], len(c["value"]))
        for c in channels
    ]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Inspect Link ECU .llgx channels")
    parser.add_argument("file")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()

    channels = load_llgx(args.file)

    if args.list:
        for name, unit, occurrence, samples in channel_names(channels):
            print(f"{name!r}\t{unit!r}\tocc={occurrence}\tsamples={samples}")
    else:
        print(f"Parsed {len(channels)} channel streams.")