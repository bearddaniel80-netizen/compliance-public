import json
from .exceptions import ValidationError

def _validate_required_fields(
    rows: list[dict],
    required_fields: list[str],
) -> None:

    if not rows:
        raise ValidationError(
            "No rows returned"
        )

    first = rows[0]

    for field in required_fields:

        if field not in first:

            raise ValidationError(
                f"Missing field: {field}"
            )


def _validate_min_rows(
    rows: list[dict],
    min_rows: int,
) -> None:

    if len(rows) < min_rows:

        raise ValidationError(
            f"Expected at least "
            f"{min_rows} rows "
            f"but got {len(rows)}"
        )


def _validate_json(
    output: str,
):

    try:

        return json.loads(output)

    except json.JSONDecodeError as exc:

        raise ValidationError(
            f"Invalid JSON: {exc}"
        ) from exc


def _validate_not_empty(
    output: str,
) -> None:

    if output is None:

        raise ValidationError(
            "Output is None"
        )

    if not output.strip():

        raise ValidationError(
            "Output is empty"
        )


def _validate_show(
    output: str,
) -> None:

    _validate_not_empty(output)


def _validate_describe(
    output: str,
) -> None:

    _validate_not_empty(output)


def _validate_select(
    output: str,
    manifest,
) -> None:

    _validate_not_empty(output)

    rows = _validate_json(output)

    assertions = manifest.assertions

    if assertions.min_rows is not None:

        _validate_min_rows(
            rows,
            assertions.min_rows,
        )

    if assertions.required_fields:

        _validate_required_fields(
            rows,
            assertions.required_fields,
        )


def validate(
    query: str,
    output: str,
    manifest,
) -> None:

    normalized = query.text.strip().upper()

    if normalized.startswith("SHOW"):

        _validate_show(output)

        return

    if normalized.startswith("DESCRIBE"):

        _validate_describe(output)

        return

    if normalized.startswith("SELECT"):

        _validate_select(
            output,
            manifest,
        )

        return

    raise ValidationError(
        f"Unknown query type: {query}"
    )