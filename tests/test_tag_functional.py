"""Functional test of 'dtool tag' CLI command."""

from click.testing import CliRunner

from . import tmp_dataset_fixture  # NOQA


def test_tag_basic(tmp_dataset_fixture):  # NOQA

    from dtool_tag.cli import tag

    runner = CliRunner()

    result = runner.invoke(tag, [
        "set",
        tmp_dataset_fixture.uri,
        "e.coli",
    ])
    assert result.exit_code == 0

    result = runner.invoke(tag, [
        "ls",
        tmp_dataset_fixture.uri,
    ])
    assert result.exit_code == 0

    expected = "e.coli"
    actual = result.output.strip()
    assert actual == expected


def test_tag_invalid_name(tmp_dataset_fixture):  # NOQA

    from dtool_tag.cli import tag

    runner = CliRunner()

    # Spaces, slashes, etc are not allowed.
    result = runner.invoke(tag, [
        "set",
        tmp_dataset_fixture.uri,
        "project name",
    ])
    assert result.exit_code == 400

    expected_lines = [
        "Invalid tag 'project name'",
        "Tag must be 80 characters or less",
        "Tags may only contain the characters: 0-9 a-z A-Z - _ .",
        "Example: first-class",
    ]
    for line in expected_lines:
        assert result.output.find(line) != -1


def test_delete_command(tmp_dataset_fixture):  # NOQA

    from dtool_tag.cli import tag

    runner = CliRunner()

    # Add two tags.
    result = runner.invoke(tag, [
        "set",
        tmp_dataset_fixture.uri,
        "e.coli",
    ])
    assert result.exit_code == 0

    result = runner.invoke(tag, [
        "set",
        tmp_dataset_fixture.uri,
        "genome",
    ])
    assert result.exit_code == 0

    # Make sure that both tags are present.
    result = runner.invoke(tag, [
        "ls",
        tmp_dataset_fixture.uri,
    ])
    assert result.exit_code == 0

    expected_lines = ["e.coli", "genome"]
    for line in expected_lines:
        assert result.output.find(line) != -1


    # Delete one tag.
    result = runner.invoke(tag, [
        "delete",
        tmp_dataset_fixture.uri,
        "e.coli",
    ])
    assert result.exit_code == 0

    result = runner.invoke(tag, [
        "ls",
        tmp_dataset_fixture.uri,
    ])
    assert result.exit_code == 0

    expected = "genome"
    actual = result.output.strip()
    assert actual == expected


    # Delete the remaining tag.
    result = runner.invoke(tag, [
        "delete",
        tmp_dataset_fixture.uri,
        "genome",
    ])
    assert result.exit_code == 0

    result = runner.invoke(tag, [
        "ls",
        tmp_dataset_fixture.uri,
    ])
    assert result.exit_code == 0

    expected = ""
    actual = result.output.strip()
    assert actual == expected
