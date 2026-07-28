def iter_results(
    context,
):

    if hasattr(
        context,
        "results",
    ):
        yield from context.results
        return

    for child in context.rows:
        yield from list(iter_results(child))

def running_tally(context):
    passed = sum(
        1
        for result in iter_results(context)
        if result.passed
    )

    failed = sum(
        1
        for result in iter_results(context)
        if not result.passed
        and not result.skipped
    )

    skipped = sum(
        1
        for result in iter_results(context)
        if result.skipped
    )

    return passed, failed, skipped

def timings_tally(context):
    return sum(
                r.duration_ms
                for r in iter_results(context)
            )

def slowest_query(
    context,
):

    return max(
        iter_results(
            context
        ),
        key=lambda r:
            r.duration_ms,
        default=None,
    )

def pass_rate(context):
    result_lst = list(iter_results(context))
    passed = sum(
        1
        for result in result_lst
        if result.passed
    )
    return int(passed / len(result_lst))