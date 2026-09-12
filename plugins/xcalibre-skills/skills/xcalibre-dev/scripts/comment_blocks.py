#!/usr/bin/env python3
"""Dump a file's comment BLOCKS with their line ranges and the first code line each precedes,
so comments can be rewritten by range without reading the whole file into context.

A BLOCK IS EVERY COMMENT LINE UP TO THE NEXT LINE OF CODE. A blank line does NOT end one and
does NOT reset the count: three lines means three comment lines before the code they describe,
however they are spaced. Only code ends a block.

    python3 comment_blocks.py <file> [comment-prefix]     # default prefix '#'
    python3 comment_blocks.py <file> --apply <edits.json> # rewrite by range
    python3 comment_blocks.py <file> --over [n]           # only blocks over n comment lines (3)

edits.json: {"<start-line>": [<end-line>, ["new line", ...]], ...}  (1-indexed, inclusive;
an empty list deletes the block). Ranges are applied high-to-low so earlier ones stay valid.
"""
import json
import sys


def spans(lines, prefix="#"):
    """(start, end, ncomment) per block, 1-indexed inclusive, blanks spanned; a leading shebang is not a comment."""
    out = []
    i = 1 if lines and lines[0].startswith("#!") else 0
    while i < len(lines):
        if lines[i].strip().startswith(prefix):
            j = i
            k = i
            n = 0
            while k < len(lines):
                s = lines[k].strip()
                if s.startswith(prefix):
                    j = k
                    n += 1
                elif s:
                    break
                k += 1
            out.append((i + 1, j + 1, n))
            i = j + 1
        else:
            i += 1
    return out


def blocks(path, prefix="#", over=None):
    lines = open(path).read().split("\n")
    for a, b, n in spans(lines, prefix):
        if over is not None and n <= over:
            continue
        code = next((lines[k].strip()[:100] for k in range(b, min(b + 4, len(lines)))
                     if lines[k].strip()), "")
        print(f"--- {a}-{b}  ({n} comment lines)  >>> {code}")
        print("\n".join(lines[a - 1:b]))


def apply(path, table):
    lines = open(path).read().split("\n")
    for start in sorted(table, key=lambda k: -int(k)):
        end, new = table[start]
        lines[int(start) - 1:end] = new
    open(path, "w").write("\n".join(lines))


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "--apply":
        apply(sys.argv[1], json.load(open(sys.argv[3])))
    elif len(sys.argv) > 2 and sys.argv[2] == "--over":
        blocks(sys.argv[1], "#", int(sys.argv[3]) if len(sys.argv) > 3 else 3)
    else:
        blocks(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "#")
