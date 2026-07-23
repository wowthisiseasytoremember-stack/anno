#!/usr/bin/env python3
"""
Pseudo-localization tool for Anno iOS .strings files.

Transforms English strings by:
  - Adding ~30% length expansion with padding characters
  - Applying Vietnamese-style diacritics to vowels
  - Wrapping output in [~~~ ~~~] brackets to visually flag unlocalized strings

Usage:
    python3 pseudo_localize.py --input Localizable.strings
    python3 pseudo_localize.py --input en.lproj/Localizable.strings --output pseudo.lproj/Localizable.strings --expansion 40
"""

import argparse
import os
import random
import re
import sys


# Vietnamese-style diacritic mappings for vowels
DIACRITIC_MAP = {
    "a": ["á", "à", "ả", "ã", "ạ"],
    "e": ["é", "è", "ẻ", "ẽ", "ẹ"],
    "i": ["í", "ì", "ỉ", "ĩ", "ị"],
    "o": ["ó", "ò", "ỏ", "õ", "ọ"],
    "u": ["ú", "ù", "ủ", "ũ", "ụ"],
    "A": ["Á", "À", "Ả", "Ã", "Ạ"],
    "E": ["É", "È", "Ẻ", "Ẽ", "Ẹ"],
    "I": ["Í", "Ì", "Ỉ", "Ĩ", "Ị"],
    "O": ["Ó", "Ò", "Ỏ", "Õ", "Ọ"],
    "U": ["Ú", "Ù", "Ủ", "Ũ", "Ụ"],
}

PADDING_CHAR = "."

# Regex to match iOS .strings line:  "key" = "value";
STRINGS_LINE_RE = re.compile(r'^("(?:[^"\\]|\\.)*")\s*=\s*("(?:[^"\\]|\\.)*");')

# Regex to match format specifiers like %@, %d, %f, %lld, %2$@, etc.
FORMAT_SPEC_RE = re.compile(r"%(\d+\$)?[-+#0-9]*(\.[0-9]+)?[hlLz]*[%@dcfFeEgGxXsuS]")

# Regex to match escape sequences like \n, \", \t, \\, etc.
ESCAPE_SEQ_RE = re.compile(r"\\([\\\"'nrt0abfve])")


def add_diacritics(text: str) -> str:
    """Apply random Vietnamese-style diacritics to vowels in the text."""
    result = []
    for char in text:
        variants = DIACRITIC_MAP.get(char)
        if variants:
            result.append(random.choice(variants))
        else:
            result.append(char)
    return "".join(result)


def pseudo_localize_value(value: str, expansion_pct: int) -> str:
    """
    Pseudo-localize a single string value.
    - Preserves format specifiers (%@, %d, etc.) and escape sequences (\n, \", etc.)
    - Applies diacritics to the rest
    - Pads to achieve ~expansion_pct length increase
    - Wraps in [~~~ ~~~]
    """
    # Split the value into segments: literal text vs format specifiers vs escape sequences
    segments = []
    pos = 0

    while pos < len(value):
        # Check for format specifier
        fmt_match = FORMAT_SPEC_RE.match(value, pos)
        if fmt_match:
            if segments and not isinstance(segments[-1], str):
                # Unlikely, but merge adjacent non-literal segments
                pass
            segments.append(("fmt", fmt_match.group(0)))
            pos = fmt_match.end()
            continue

        # Check for escape sequence
        esc_match = ESCAPE_SEQ_RE.match(value, pos)
        if esc_match:
            segments.append(("esc", esc_match.group(0)))
            pos = esc_match.end()
            continue

        # Regular character — accumulate into a literal segment
        if not segments or segments[-1][0] != "lit":
            segments.append(("lit", ""))
        segments[-1] = ("lit", segments[-1][1] + value[pos])
        pos += 1

    # Build pseudo-localized version segment by segment
    pseudo_parts = []
    for seg_type, seg_value in segments:
        if seg_type == "lit":
            # Apply diacritics to literal text
            pseudo_parts.append(add_diacritics(seg_value))
        else:
            # Preserve format specifiers and escape sequences exactly
            pseudo_parts.append(seg_value)

    localized = "".join(pseudo_parts)

    # Calculate padding needed for ~expansion_pct increase
    original_len = len(value)
    target_len = int(original_len * (1 + expansion_pct / 100.0))

    # But the bracket wrapping adds ~7 chars ([~~~ ~~~]), subtract that
    bracket_overhead = 7  # "[~~~" + "~~~]"
    padding_needed = max(0, target_len - original_len - bracket_overhead)

    # Distribute padding: ~half before, half after (inside the brackets)
    pad_left = padding_needed // 2
    pad_right = padding_needed - pad_left

    padded = PADDING_CHAR * pad_left + localized + PADDING_CHAR * pad_right

    return f"[~~~{padded}~~~]"


def parse_strings_line(line: str) -> tuple[str | None, str | None, str | None]:
    """
    Parse a single line of a .strings file.
    Returns (full_match, key_str, value_str). If not a strings line, returns (None, None, None).
    """
    match = STRINGS_LINE_RE.match(line)
    if not match:
        return None, None, None
    return match.group(0), match.group(1), match.group(2)


def process_file(input_path: str, output_path: str, expansion_pct: int) -> dict:
    """Process a .strings file and write the pseudo-localized output."""
    stats = {
        "keys_processed": 0,
        "total_original_len": 0,
        "total_pseudo_len": 0,
    }

    with open(input_path, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    out_lines = []

    for line in lines:
        _, key_str, value_str = parse_strings_line(line.rstrip("\n").rstrip("\r"))
        if key_str is None or value_str is None:
            out_lines.append(line.rstrip("\n").rstrip("\r"))
            continue

        # Extract the actual value without surrounding quotes
        inner_value = value_str[1:-1]  # strip quotes

        # Pseudo-localize
        pseudo_value = pseudo_localize_value(inner_value, expansion_pct)

        # Reconstruct line: "key" = "pseudo_value";
        pseudo_line = f'{key_str} = "{pseudo_value}";'
        out_lines.append(pseudo_line)

        stats["keys_processed"] += 1
        stats["total_original_len"] += len(inner_value)
        stats["total_pseudo_len"] += len(pseudo_value)

    # Write output
    with open(output_path, "w", encoding="utf-8") as outfile:
        for line in out_lines:
            outfile.write(line + "\n")

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Pseudo-localize iOS .strings files for Anno localization testing.\n"
                    "Expands English strings by ~30%, adds Vietnamese-style diacritics,\n"
                    "and wraps in [~~~ ~~~] brackets to visually flag unlocalized strings.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input .strings file",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Path to the output pseudo .strings file (default: input path with .pseudo suffix)",
    )
    parser.add_argument(
        "--expansion",
        type=int,
        default=30,
        help="Percentage to expand strings by (default: 30)",
    )
    args = parser.parse_args()

    # Validate input file
    if not os.path.isfile(args.input):
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Determine output path
    if args.output is None:
        output_path = args.input + ".pseudo"
    else:
        output_path = args.output

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Seed RNG for reproducibility (same seed = same pseudo-loc output)
    random.seed(42)

    # Process the file
    stats = process_file(args.input, output_path, args.expansion)

    # Calculate averages
    avg_original = stats["total_original_len"] / stats["keys_processed"] if stats["keys_processed"] > 0 else 0
    avg_pseudo = stats["total_pseudo_len"] / stats["keys_processed"] if stats["keys_processed"] > 0 else 0

    # Print summary
    print(f"Pseudo-localization complete!")
    print(f"  Input:  {args.input}")
    print(f"  Output: {output_path}")
    print(f"  Keys processed:      {stats['keys_processed']}")
    print(f"  Avg length before:   {avg_original:.1f} chars")
    print(f"  Avg length after:    {avg_pseudo:.1f} chars")
    print(f"  Expansion target:    {args.expansion}%")


if __name__ == "__main__":
    main()
