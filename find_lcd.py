#!/usr/bin/env python3
"""Filter the segment LCD reference list by size, drive and temperature.

Examples:
    python find_lcd.py --min-width 40 --max-width 60 --voltage 3.0
    python find_lcd.py --type VA --negative --duty 1/4
    python find_lcd.py --temp-min -30 --app thermostat --csv > picks.csv
"""
import argparse
import csv
import os
import sys

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "segment-lcd-references.csv")


def num(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def fmt(value):
    n = num(value)
    if n is None:
        return "?"
    return ("%.1f" % n).rstrip("0").rstrip(".") if n != int(n) else str(int(n))


def temp(value):
    n = num(value)
    if n is None:
        return "?"
    return "%+d" % n if n else "0"


def build_parser():
    p = argparse.ArgumentParser(description="Filter segment LCD references by size, drive and temperature.")
    p.add_argument("--min-width", type=float, help="minimum viewing-area width in mm")
    p.add_argument("--max-width", type=float, help="maximum viewing-area width in mm")
    p.add_argument("--min-height", type=float, help="minimum viewing-area height in mm")
    p.add_argument("--max-height", type=float, help="maximum viewing-area height in mm")
    p.add_argument("--voltage", type=float, help="LCD operating voltage in V (matches within 0.2 V)")
    p.add_argument("--duty", help="1/4, 1/8, static ...")
    p.add_argument("--type", help="TN, HTN, STN, FSTN, DFSTN or VA")
    pol = p.add_mutually_exclusive_group()
    pol.add_argument("--positive", action="store_true", help="positive mode only (dark segments on a light background)")
    pol.add_argument("--negative", action="store_true", help="negative mode only (light segments on a dark background)")
    p.add_argument("--temp-min", type=float, help="rated to operate at this temperature or colder, in °C")
    p.add_argument("--temp-max", type=float, help="rated to operate at this temperature or hotter, in °C")
    p.add_argument("--connection", help="Metal pins, Zebra, FPC or Heat seal")
    p.add_argument("--app", help="text to look for in the application column")
    p.add_argument("--csv", action="store_true", help="write matching rows as CSV instead of a list")
    p.add_argument("--data", default=DATA, help=argparse.SUPPRESS)
    return p


def matches(r, a):
    w, h = num(r["viewing_area_w_mm"]), num(r["viewing_area_h_mm"])
    tmin, tmax = num(r["operating_temp_min_c"]), num(r["operating_temp_max_c"])
    v = num(r["lcd_voltage_v"])
    checks = [
        a.min_width is None or (w is not None and w >= a.min_width),
        a.max_width is None or (w is not None and w <= a.max_width),
        a.min_height is None or (h is not None and h >= a.min_height),
        a.max_height is None or (h is not None and h <= a.max_height),
        a.voltage is None or (v is not None and abs(v - a.voltage) <= 0.2),
        a.duty is None or r["duty"].lower() == a.duty.lower(),
        a.type is None or r["lcd_type"].upper() == a.type.upper(),
        not a.positive or r["polarity"] == "positive",
        not a.negative or r["polarity"] == "negative",
        a.temp_min is None or (tmin is not None and tmin <= a.temp_min),
        a.temp_max is None or (tmax is not None and tmax >= a.temp_max),
        a.connection is None or r["connection"].lower() == a.connection.lower(),
        a.app is None or a.app.lower() in r["application"].lower(),
    ]
    return all(checks)


def line(r):
    drive = r["duty"] + (" duty, " + r["bias"] + " bias" if r["bias"] else "")
    t = "%s to %s °C" % (temp(r["operating_temp_min_c"]), temp(r["operating_temp_max_c"]))
    v = num(r["lcd_voltage_v"])
    return "%-8s %-5s %-8s %6s x %-5s mm  %s V  %-19s %-14s %s" % (
        r["model"], r["lcd_type"], r["polarity"], fmt(r["viewing_area_w_mm"]), fmt(r["viewing_area_h_mm"]),
        "%.1f" % v if v is not None else "?", drive, t, r["url"])


def main(argv=None):
    a = build_parser().parse_args(argv)
    with open(a.data, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    found = [r for r in rows if matches(r, a)]
    if a.csv:
        out = csv.DictWriter(sys.stdout, fieldnames=list(rows[0].keys()) if rows else [])
        out.writeheader()
        out.writerows(found)
    else:
        for r in found:
            print(line(r))
    print("%d of %d references" % (len(found), len(rows)), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
