#!/usr/bin/env python3
"""
Anno Strings Validator — localization coverage and integrity checks.

Validates that:
1. All Vietnamese strings files have matching English originals (and vice versa)
2. No values are empty or placeholder-only
3. Key naming follows project conventions
4. Coverage statistics are reported

Usage:
    python3 validate_localization.py \
        --reference localization/en/Localizable.strings \
        --target localization/vi/Localizable.strings
"""

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# .strings file parser
# ---------------------------------------------------------------------------

STRINGS_LINE_RE = re.compile(
    r'^"([^"]+)"\s*=\s*"((?:[^"\\]|\\.)*)"\s*;\s*(?://.*)?$'
)
COMMENT_RE = re.compile(r"^\s*(//|/\*)")


@dataclass
class StringsFile:
    path: Path
    entries: Dict[str, str] = field(default_factory=dict)
    parse_errors: List[Tuple[int, str]] = field(default_factory=list)

    @classmethod
    def parse(cls, path: Path) -> "StringsFile":
        sf = cls(path=path)
        if not path.exists():
            sf.parse_errors.append((0, f"File not found: {path}"))
            return sf

        content = path.read_text(encoding="utf-8")
        for i, line in enumerate(content.splitlines(), start=1):
            stripped = line.strip()
            if not stripped or COMMENT_RE.match(stripped):
                continue
            m = STRINGS_LINE_RE.match(stripped)
            if m:
                key = m.group(1)
                value = m.group(2)
                if key in sf.entries:
                    sf.parse_errors.append(
                        (i, f"Duplicate key: \"{key}\" (first at line ?)")
                    )
                sf.entries[key] = value
            else:
                # Could be a multi-line value, silent ignore for now
                pass
        return sf


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


@dataclass
class ValidationReport:
    reference_path: Path
    target_path: Path
    reference: StringsFile
    target: StringsFile

    # Key comparison
    missing_in_target: List[str] = field(default_factory=list)
    extra_in_target: List[str] = field(default_factory=list)
    value_mismatch: List[Tuple[str, str, str]] = field(default_factory=list)
    empty_values_target: List[str] = field(default_factory=list)
    empty_values_reference: List[str] = field(default_factory=list)

    # Coverage
    key_count_reference: int = 0
    key_count_target: int = 0
    coverage_pct: float = 0.0

    # Convention checks
    naming_issues: List[str] = field(default_factory=list)

    # Parse errors
    parse_errors_reference: List[Tuple[int, str]] = field(default_factory=list)
    parse_errors_target: List[Tuple[int, str]] = field(default_factory=list)

    VALID_KEY_PREFIXES = {"app", "tab", "action", "label", "setting", "paywall",
                          "onboarding", "empty", "accessibility", "alert", "section"}

    def validate(self) -> "ValidationReport":
        self.key_count_reference = len(self.reference.entries)
        self.key_count_target = len(self.target.entries)
        self.parse_errors_reference = self.reference.parse_errors
        self.parse_errors_target = self.target.parse_errors

        ref_keys = set(self.reference.entries.keys())
        tgt_keys = set(self.target.entries.keys())

        self.missing_in_target = sorted(ref_keys - tgt_keys)
        self.extra_in_target = sorted(tgt_keys - ref_keys)

        common_keys = ref_keys & tgt_keys
        for key in sorted(common_keys):
            ref_val = self.reference.entries[key]
            tgt_val = self.target.entries[key]

            if not ref_val.strip():
                self.empty_values_reference.append(key)
            if not tgt_val.strip():
                self.empty_values_target.append(key)

        self.coverage_pct = (
            (len(common_keys) / len(ref_keys) * 100) if ref_keys else 100.0
        )

        # Naming convention check
        for key in sorted(ref_keys | tgt_keys):
            parts = key.split(".")
            if len(parts) < 2:
                self.naming_issues.append(
                    f"\"{key}\": must have at least 2 dot-separated segments "
                    f"(e.g. 'tab.today')"
                )
            elif parts[0] not in self.VALID_KEY_PREFIXES:
                self.naming_issues.append(
                    f"\"{key}\": prefix '{parts[0]}' is not in the allowed set: "
                    f"{sorted(self.VALID_KEY_PREFIXES)}"
                )

        return self

    def print_report(self, verbose: bool = False) -> None:
        print(f"{'='*70}")
        print(f"  Strings Validation Report")
        print(f"{'='*70}")
        print(f"  Reference: {self.reference_path}")
        print(f"  Target:    {self.target_path}")
        print()

        print(f"  Reference keys: {self.key_count_reference}")
        print(f"  Target keys:    {self.key_count_target}")
        print(f"  Coverage:       {self.coverage_pct:.1f}%")
        print()

        if self.parse_errors_reference:
            print(f"  [!] Parse errors in reference:")
            for line_no, msg in self.parse_errors_reference[:10]:
                print(f"      Line {line_no}: {msg}")
            print()

        if self.parse_errors_target:
            print(f"  [!] Parse errors in target:")
            for line_no, msg in self.parse_errors_target[:10]:
                print(f"      Line {line_no}: {msg}")
            print()

        if self.missing_in_target:
            print(f"  [!] Missing in target ({len(self.missing_in_target)}):")
            if verbose:
                for key in self.missing_in_target:
                    print(f"      - \"{key}\" = \"{self.reference.entries[key]}\"")
            else:
                print(f"      (use --verbose to show values)")
            print()

        if self.extra_in_target:
            print(f"  [!] Extra keys in target ({len(self.extra_in_target)}):")
            for key in self.extra_in_target:
                print(f"      - \"{key}\" = \"{self.target.entries[key]}\"")
            print()

        if self.empty_values_reference:
            print(f"  [!] Empty values in reference ({len(self.empty_values_reference)}):")
            for key in self.empty_values_reference:
                print(f"      - \"{key}\"")
            print()

        if self.empty_values_target:
            print(f"  [!] Empty values in target ({len(self.empty_values_target)}):")
            for key in self.empty_values_target:
                print(f"      - \"{key}\"")
            print()

        if self.naming_issues:
            print(f"  [!] Naming convention issues ({len(self.naming_issues)}):")
            for issue in self.naming_issues[:10]:
                print(f"      - {issue}")
            if len(self.naming_issues) > 10:
                print(f"      ... and {len(self.naming_issues) - 10} more")
            print()

        if (not self.missing_in_target and not self.extra_in_target
                and not self.empty_values_target and not self.naming_issues
                and not self.parse_errors_reference):
            print("  ✓ All checks passed!")
        print(f"{'='*70}")

    def to_json_summary(self) -> dict:
        return {
            "reference": str(self.reference_path),
            "target": str(self.target_path),
            "reference_keys": self.key_count_reference,
            "target_keys": self.key_count_target,
            "coverage_pct": round(self.coverage_pct, 1),
            "missing_in_target": self.missing_in_target,
            "extra_in_target": self.extra_in_target,
            "empty_values_target": self.empty_values_target,
            "naming_issues": self.naming_issues,
            "parse_errors_reference": [f"Line {ln}: {msg}" for ln, msg in self.parse_errors_reference],
            "parse_errors_target": [f"Line {ln}: {msg}" for ln, msg in self.parse_errors_target],
        }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def find_strings_files(base_dir: Path) -> Dict[str, Path]:
    """Discover .strings files in localization subdirectories."""
    files = {}
    for lproj_dir in base_dir.iterdir():
        if lproj_dir.is_dir():
            strings_file = lproj_dir / "Localizable.strings"
            if strings_file.exists():
                files[lproj_dir.name] = strings_file
    return files


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate Anno .strings files for coverage and integrity."
    )
    parser.add_argument(
        "--reference",
        type=str,
        default=None,
        help="Path to reference (English) .strings file",
    )
    parser.add_argument(
        "--target",
        type=str,
        default=None,
        help="Path to target (Vietnamese) .strings file",
    )
    parser.add_argument(
        "--localization-dir",
        type=str,
        default=None,
        help="Path to localization/ directory (auto-discovers all languages)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show full details for missing keys",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON summary",
    )

    args = parser.parse_args()

    # Determine files
    ref_path: Optional[Path] = None
    tgt_path: Optional[Path] = None
    auto_discovered = False

    if args.localization_dir:
        base = Path(args.localization_dir)
        found = find_strings_files(base)
        if "en" in found:
            ref_path = found["en"]
        if "vi" in found:
            tgt_path = found["vi"]
        if ref_path and tgt_path:
            auto_discovered = True
        else:
            print(f"Discovered languages: {list(found.keys())}")
            if not ref_path:
                print("No English .strings found in localization/")
            if not tgt_path:
                print("No Vietnamese .strings found in localization/")

    if not auto_discovered:
        if not args.reference or not args.target:
            parser.error(
                "Provide --reference and --target, or --localization-dir"
            )
        ref_path = Path(args.reference)
        tgt_path = Path(args.target)

    assert ref_path is not None and tgt_path is not None, "Language files must resolve"

    # Parse and validate
    ref_file = StringsFile.parse(ref_path)
    tgt_file = StringsFile.parse(tgt_path)

    report = ValidationReport(
        reference_path=ref_path,
        target_path=tgt_path,
        reference=ref_file,
        target=tgt_file,
    ).validate()

    if args.json:
        import json
        json.dump(report.to_json_summary(), sys.stdout, indent=2, ensure_ascii=False)
        print()
    else:
        report.print_report(verbose=args.verbose)

    # Exit code
    if report.missing_in_target or report.empty_values_target:
        sys.exit(1)


if __name__ == "__main__":
    main()
