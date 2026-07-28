from pathlib import Path


from ..report_models import (
    FileArtifact, ReporterRole, ReportContext
)

from ....models import OutputFormat
from ....module_loader import load
from ..report_registry import reporter

@reporter(
    formats=[
        OutputFormat.HTML,
    ],
    role=ReporterRole.RENDERER,
)
class HtmlRenderer:

    def render(
        self,
        report_context: ReportContext,
    ) -> FileArtifact:

        templates = (
            Path.cwd() / "templates"
        )

        load("jinja")
        from jinja2 import (
            Environment,
            FileSystemLoader,
        )

        self.environment = (
            Environment(
                loader=FileSystemLoader(
                    templates
                )
            )
        )

        template = (
            self.environment
            .get_template(
                "report.html.j2"
            )
        )
        
        summary = report_context.report_data.summary

        html = template.render(
            summary=summary.to_dict(),
            failures=[
                x.to_dict()
                for x in report_context.report_data.failures
            ],
            performance=[
                x.to_dict()
                for x in report_context.report_data.performance
            ],
        )

        report_context.artifact =  FileArtifact(
            content=html,
            output_file="index.html"
        )