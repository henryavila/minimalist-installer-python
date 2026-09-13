"""Questionary prompts must show the active/selected row like Atomic/clack."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from minimalist_installer.tui.app import Choice, create_questionary_prompts
from minimalist_installer.tui.prompt_style import (
    CHECKBOX_INSTRUCTION,
    SELECT_INSTRUCTION,
    build_prompt_style,
    prompt_pointer,
    prompt_qmark,
)


def _style_attrs(style) -> dict[str, str]:
    """Map prompt_toolkit Style class names to their style strings."""

    return {cls: attrs for cls, attrs in style.style_rules}


def test_prompt_style_highlights_active_and_selected_rows() -> None:
    """Clack-like contrast: active row cyan, checked green, pointer visible."""

    style = build_prompt_style(color=True)
    attrs = _style_attrs(style)

    assert "highlighted" in attrs
    assert "cyan" in attrs["highlighted"] or "bold" in attrs["highlighted"]
    assert attrs["highlighted"].strip() != ""

    assert "pointer" in attrs
    assert attrs["pointer"].strip() != ""
    assert "cyan" in attrs["pointer"] or "bold" in attrs["pointer"]

    assert "selected" in attrs
    assert attrs["selected"].strip() != ""
    assert "green" in attrs["selected"] or "bold" in attrs["selected"]

    assert "instruction" in attrs
    assert attrs["instruction"].strip() != ""


def test_prompt_glyphs_follow_unicode_capability() -> None:
    assert prompt_pointer(unicode_ok=True) == "❯"
    assert prompt_pointer(unicode_ok=False) == ">"
    assert prompt_qmark(unicode_ok=True) == "◆"
    assert prompt_qmark(unicode_ok=False) == "*"


def test_select_passes_style_pointer_instruction_and_choice_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Select must wire visible chrome; default must match a Choice value."""

    fake_question = MagicMock()
    fake_question.ask.return_value = "user"
    select_mock = MagicMock(return_value=fake_question)
    monkeypatch.setattr(
        "questionary.select",
        select_mock,
        raising=False,
    )
    import questionary

    monkeypatch.setattr(questionary, "select", select_mock)

    prompts = create_questionary_prompts()
    result = prompts.select(
        "Where?",
        [Choice("user", "User"), Choice("project", "Project")],
        default="user",
    )

    assert result == "user"
    assert select_mock.call_count == 1
    kwargs = select_mock.call_args.kwargs
    assert kwargs["pointer"] in {"❯", ">"}
    assert kwargs["qmark"] in {"◆", "*"}
    assert kwargs["instruction"] == SELECT_INSTRUCTION
    assert kwargs["style"] is not None
    attrs = _style_attrs(kwargs["style"])
    assert attrs["highlighted"].strip() != ""
    # default must be the Choice value that exists (string or Choice with that value)
    default = kwargs["default"]
    if hasattr(default, "value"):
        assert default.value == "user"
    else:
        assert default == "user"


def test_checkbox_passes_style_pointer_and_instruction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_question = MagicMock()
    fake_question.ask.return_value = ["codex"]
    checkbox_mock = MagicMock(return_value=fake_question)
    import questionary

    monkeypatch.setattr(questionary, "checkbox", checkbox_mock)

    prompts = create_questionary_prompts()
    result = prompts.checkbox(
        "Hosts?",
        [Choice("codex", "Codex", checked=True), Choice("cursor", "Cursor")],
    )

    assert result == ["codex"]
    kwargs = checkbox_mock.call_args.kwargs
    assert kwargs["pointer"] in {"❯", ">"}
    assert kwargs["qmark"] in {"◆", "*"}
    assert kwargs["instruction"] == CHECKBOX_INSTRUCTION
    assert kwargs["style"] is not None
    attrs = _style_attrs(kwargs["style"])
    assert attrs["selected"].strip() != ""
    assert attrs["pointer"].strip() != ""
