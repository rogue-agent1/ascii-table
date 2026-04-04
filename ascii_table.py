#!/usr/bin/env python3
"""ascii_table - ASCII/Unicode reference and encoding toolkit.

Lookup characters, code points, encoding conversions. Zero dependencies.
"""

import argparse
import sys
import unicodedata


def cmd_lookup(args):
    for ch in args.text:
        cp = ord(ch)
        try:
            name = unicodedata.name(ch)
        except ValueError:
            name = "(unknown)"
        cat = unicodedata.category(ch)
        print(f"  '{ch}'  U+{cp:04X}  {cp:>5d}  0x{cp:02X}  0b{cp:08b}  {cat}  {name}")


def cmd_range(args):
    start = int(args.start, 0) if args.start.startswith("0") else int(args.start)
    end = int(args.end, 0) if args.end.startswith("0") else int(args.end)
    cols = args.cols or 16
    for i in range(start, end + 1, cols):
        hex_part = f"U+{i:04X}: "
        chars = ""
        for j in range(cols):
            cp = i + j
            if cp > end:
                break
            ch = chr(cp)
            if unicodedata.category(ch).startswith("C"):
                chars += " .  "
            else:
                chars += f" {ch}  "
        print(f"  {hex_part}{chars}")


def cmd_ascii(args):
    print("  Dec  Hex  Oct  Char  Name")
    print("  " + "-" * 50)
    names = {0: "NUL", 1: "SOH", 2: "STX", 3: "ETX", 4: "EOT", 5: "ENQ", 6: "ACK",
             7: "BEL", 8: "BS", 9: "TAB", 10: "LF", 11: "VT", 12: "FF", 13: "CR",
             14: "SO", 15: "SI", 16: "DLE", 17: "DC1", 18: "DC2", 19: "DC3", 20: "DC4",
             21: "NAK", 22: "SYN", 23: "ETB", 24: "CAN", 25: "EM", 26: "SUB", 27: "ESC",
             28: "FS", 29: "GS", 30: "RS", 31: "US", 32: "SP", 127: "DEL"}
    for i in range(128):
        ch = names.get(i, chr(i))
        display = ch if i > 32 and i < 127 else f"({ch})"
        print(f"  {i:>3d}  0x{i:02X}  {i:03o}  {display:<6}")


def cmd_encode(args):
    text = args.text
    for enc in (args.encoding or "utf-8").split(","):
        enc = enc.strip()
        try:
            raw = text.encode(enc)
            hex_str = " ".join(f"{b:02X}" for b in raw)
            print(f"  {enc}: {hex_str} ({len(raw)} bytes)")
        except (UnicodeEncodeError, LookupError) as e:
            print(f"  {enc}: ERROR - {e}")


def cmd_decode(args):
    hex_str = args.hex.replace(" ", "").replace("0x", "")
    raw = bytes.fromhex(hex_str)
    for enc in (args.encoding or "utf-8").split(","):
        enc = enc.strip()
        try:
            text = raw.decode(enc)
            print(f"  {enc}: {text!r}")
        except (UnicodeDecodeError, LookupError) as e:
            print(f"  {enc}: ERROR - {e}")


def cmd_search(args):
    query = args.query.upper()
    count = 0
    for cp in range(0x10FFFF + 1):
        try:
            ch = chr(cp)
            name = unicodedata.name(ch)
            if query in name:
                print(f"  U+{cp:04X}  {ch}  {name}")
                count += 1
                if count >= (args.limit or 50):
                    break
        except ValueError:
            continue
    print(f"\n{count} results", file=sys.stderr)


def cmd_stats(args):
    text = args.text if args.text else sys.stdin.read()
    total = len(text)
    unique = len(set(text))
    categories = {}
    scripts = {}
    for ch in text:
        cat = unicodedata.category(ch)
        categories[cat] = categories.get(cat, 0) + 1
        try:
            scr = unicodedata.name(ch).split()[0]
            scripts[scr] = scripts.get(scr, 0) + 1
        except ValueError:
            pass
    utf8_bytes = len(text.encode("utf-8"))
    print(f"  Characters: {total}")
    print(f"  Unique: {unique}")
    print(f"  UTF-8 bytes: {utf8_bytes}")
    print(f"  Categories:")
    for cat, cnt in sorted(categories.items(), key=lambda x: -x[1])[:10]:
        print(f"    {cat}: {cnt}")


def main():
    p = argparse.ArgumentParser(description="ASCII/Unicode toolkit")
    sub = p.add_subparsers(dest="cmd")

    lp = sub.add_parser("lookup", help="Lookup character details")
    lp.add_argument("text")

    rp = sub.add_parser("range", help="Show code point range")
    rp.add_argument("start")
    rp.add_argument("end")
    rp.add_argument("-c", "--cols", type=int, default=16)

    sub.add_parser("ascii", help="Full ASCII table")

    ep = sub.add_parser("encode", help="Encode text to bytes")
    ep.add_argument("text")
    ep.add_argument("-e", "--encoding", default="utf-8")

    dp = sub.add_parser("decode", help="Decode hex bytes to text")
    dp.add_argument("hex")
    dp.add_argument("-e", "--encoding", default="utf-8")

    sp = sub.add_parser("search", help="Search Unicode by name")
    sp.add_argument("query")
    sp.add_argument("-n", "--limit", type=int, default=50)

    stp = sub.add_parser("stats", help="Text Unicode statistics")
    stp.add_argument("text", nargs="?")

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        sys.exit(1)
    {"lookup": cmd_lookup, "range": cmd_range, "ascii": cmd_ascii, "encode": cmd_encode,
     "decode": cmd_decode, "search": cmd_search, "stats": cmd_stats}[args.cmd](args)


if __name__ == "__main__":
    main()
