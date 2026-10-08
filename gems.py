#!/usr/bin/env python3
"""hidden-gems: unlocks the vault.

You are reading this before running it. Good. That is the whole lesson.

What it does: reads your username, your machine name and this folder, then
prints them back to you with some theatre. What it does not do: no network,
no file writes, no subprocess. tests/test_gems.py proves that on every run.
"""
import getpass
import os
import platform
import random
import sys
import time

WATERMARK = "hidden-gems-16d6937f70"
ROOT = os.path.dirname(os.path.abspath(__file__))

JOKES = [
    "Your systems are penetrated! Ouch.",
    "We have your IP address. It is 127.0.0.1. Keep it secret.",
    "Firewall breached. It is now just a wall.",
    "System compromised: your dignity.",
    "Your webcam light is on. Smile. (It is not. But you checked, didn't you?)",
    "Uploading your secrets to the cloud. The cloud said no thanks.",
    "Your password has been changed to 'ihavescrapedtoomuch'. (It has not.)",
    "Congratulations: you scraped 0 secrets and 1 lesson.",
    "sudo make me a sandwich. Permission denied. Same as your scraper.",
    "Mission failed. You will get 'em next time.",
]

COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def paint(code, text):
    return f"\033[{code}m{text}\033[0m" if COLOR else text


def red(text):
    return paint("1;31", text)


def green(text):
    return paint("32", text)


def dim(text):
    return paint("2", text)


def bar(label, seconds):
    """A progress bar that goes nowhere, slowly."""
    width = 24
    steps = 12
    frames = range(steps + 1) if sys.stdout.isatty() else [steps]
    for i in frames:
        filled = int(width * i / steps)
        line = f"  {label:<34} [{'#' * filled}{'.' * (width - filled)}] {int(100 * i / steps):3d}%"
        sys.stdout.write("\r" + line)
        sys.stdout.flush()
        if seconds:
            time.sleep(seconds / len(frames))
    sys.stdout.write("\n")


def loot(root):
    """Count what you took: files and lines in this folder, .git excluded."""
    files = lines = 0
    for here, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d != ".git"]
        for name in names:
            files += 1
            try:
                with open(os.path.join(here, name), "r", encoding="utf-8", errors="ignore") as fh:
                    lines += sum(1 for _ in fh)
            except OSError:
                pass
    return files, lines


def whoami():
    try:
        return getpass.getuser()
    except Exception:
        return "mystery guest"


def main(argv):
    pause = 0 if "--fast" in argv else 1.0
    files, lines = loot(ROOT)

    print()
    print(dim("  hidden-gems vault v1.0"))
    bar("Decrypting the vault", pause * 2)
    bar("Bypassing your antivirus", pause * 1.5)
    print()
    print(red("  !! INTRUSION DETECTED !!"))
    print(red("  Your systems are penetrated! Ouch."))
    print()
    print(f"  user       {whoami()}")
    print(f"  machine    {platform.node() or 'unknown'} ({platform.system() or 'unknown'})")
    print(f"  location   {os.getcwd()}")
    print(f"  loot       {files} files, {lines} lines, 0 secrets")
    print()
    bar("Uploading your browser history", pause * 2)
    print(f"  {random.choice(JOKES[1:])}")
    if pause:
        time.sleep(pause * 2)
    print()
    print(green("  Relax. Joke lang. Nothing left your machine."))
    print("  This file has no network code. Read it: it is shorter than your scraper.")
    print("  The only real gem here: never run code you scraped without reading it first.")
    print()
    print(dim("  Made with love by JTL Growth, https://jtlgrowth.com"))
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
