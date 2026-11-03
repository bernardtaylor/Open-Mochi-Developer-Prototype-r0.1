#!/usr/bin/env python3
"""Optional reproducible r0 play-test against a running local gateway.

Creates a redacted report containing no hostname, IP, Bluetooth MAC,
GPS coordinate, board serial or credentials. Only intended for loopback URL.
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def request(url, command):
    data = json.dumps({"command": command}).encode()
    r = Request(url + "/api/command", data=data, headers={"Content-Type": "application/json"})
    try:
        with urlopen(r, timeout=5) as result:
            return result.status, json.loads(result.read())
    except HTTPError as error:
        return error.code, json.loads(error.read())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8765")
    parser.add_argument("--output", default="playtest-report.json")
    args = parser.parse_args()
    if args.url not in ("http://127.0.0.1:8765", "http://localhost:8765"):
        parser.error("r0 playtest only supports the default loopback server")
    steps = [
        ("I", 200, "ID:0.2,"),
        ("Q", 200, "ST:"),
        ("E:happy", 200, "OK:E:happy"),
        ("V:42.5", 200, "OK:V"),
        ("S:1", 200, "OK:S"),
        ("P:1", 200, "OK:P"),
        ("P:0", 200, "OK:P"),
        ("Q", 200, "ST:happy,42.5"),
        ("E:bad", 422, ""),
        ("V:-1", 422, ""),
        ("E:neutral", 200, "OK:E:neutral"),
        ("V:0", 200, "OK:V"),
    ]
    results = []
    for cmd, expected_code, expected_prefix in steps:
        try:
            status, body = request(args.url, cmd)
            reply = body.get("reply", "")
            passed = status == expected_code and (not expected_prefix or reply.startswith(expected_prefix))
            results.append({"command": cmd, "passed": passed, "http_status": status, "reply": reply[:40]})
        except (URLError, OSError, ValueError) as error:
            results.append({"command": cmd, "passed": False, "error": type(error).__name__})
    passed = sum(row["passed"] for row in results)
    report = {"project": "open-mochi", "protocol": "MOCHI/1", "version": "0.2.0",
              "timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "python_major_minor": f"{sys.version_info.major}.{sys.version_info.minor}",
              "passed": passed, "total": len(steps), "tests": results,
              "privacy": "This report omits GPS, usernames, MAC, hostname, serials and tokens."}
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"{passed}/{len(steps)} checks passed; wrote {args.output}")
    sys.exit(0 if passed == len(steps) else 1)


if __name__ == "__main__":
    main()
