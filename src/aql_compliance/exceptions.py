class ComplianceError(Exception):
    """
    Base compliance framework exception.
    """

    pass


class RetryableError(
    ComplianceError
):
    """
    Query output failed validation.
    """

    pass

class ValidationError(
    ComplianceError
):
    """
    Query output failed validation.
    """

    pass


class FailFastQuery(
    ComplianceError
):
    """
    Stop suite immediately on first query failure.
    """

    pass


class ManifestError(
    ComplianceError
):
    """
    Manifest loading/parsing error.
    """

    pass


class FixtureError(
    ComplianceError
):
    """
    Fixture loading error.
    """

    pass