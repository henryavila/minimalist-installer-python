"""Clack-inspired Questionary styles so the active row is always visible.

Questionary's DEFAULT_STYLE leaves ``pointer``, ``selected``, and
``highlighted`` empty, so select/checkbox look flat on many terminals.
Atomic Skills uses @clack/prompts (cyan active, green checked); mirror that
contrast here without depending on Node.
"""

from __future__ import annotations

from typing import Any

from .theme import detect_unicode_ok

SELECT_INSTRUCTION = "(↑↓ move, enter confirm)"
CHECKBOX_INSTRUCTION = "(↑↓ move, space toggle, enter confirm)"


def prompt_pointer(*, unicode_ok: bool | None = None) -> str:
    ok = detect_unicode_ok() if unicode_ok is None else unicode_ok
    return "❯" if ok else ">"


def prompt_qmark(*, unicode_ok: bool | None = None) -> str:
    ok = detect_unicode_ok() if unicode_ok is None else unicode_ok
    return "◆" if ok else "*"


def build_prompt_style(*, color: bool = True) -> Any:
    """High-contrast style matching Atomic/clack select and checkbox chrome."""

    from questionary import Style

    if not color:
        return Style(
            [
                ("qmark", "bold"),
                ("question", "bold"),
                ("answer", "bold"),
                ("pointer", "bold"),
                ("highlighted", "bold underline"),
                ("selected", "bold"),
                ("instruction", "italic"),
                ("text", ""),
                ("separator", "italic"),
                ("disabled", "italic"),
            ]
        )
    return Style(
        [
            ("qmark", "fg:#00d4ff bold"),
            ("question", "bold"),
            ("answer", "fg:#00c853 bold"),
            ("pointer", "fg:#00d4ff bold"),
            ("highlighted", "fg:#00d4ff bold"),
            ("selected", "fg:#00c853 bold"),
            ("instruction", "fg:#808080 italic"),
            ("text", ""),
            ("separator", "fg:#808080"),
            ("disabled", "fg:#808080 italic"),
        ]
    )


__all__ = [
    "CHECKBOX_INSTRUCTION",
    "SELECT_INSTRUCTION",
    "build_prompt_style",
    "prompt_pointer",
    "prompt_qmark",
]
