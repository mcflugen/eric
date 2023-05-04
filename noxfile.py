import os
import pathlib
import shutil
import tempfile
from urllib import request

import nox


@nox.session(name="build-refs")
def build_refs(session: nox.Session) -> None:
    article_pattern = "(article-journal|chapter)"

    session.install("click", "pandoc", "pyyaml")

    with session.chdir("cv/refs"):
        with open("_articles.yaml", "w") as fp:
            session.run(
                "pandoc",
                "articles.bib",
                "-s",
                "-f",
                "biblatex",
                "-t",
                "markdown",
                stdout=fp,
            )

        with open("_journal-articles.yaml", "w") as fp:
            session.run(
                "python",
                "filter_by_type.py",
                f"--type={article_pattern}",
                "_articles.yaml",
                stdout=fp,
                stderr=None,
            )
        with open("_other.yaml", "w") as fp:
            session.run(
                "python",
                "filter_by_type.py",
                "_articles.yaml",
                f"--type=(?!{article_pattern})",
                stdout=fp,
                stderr=None,
            )


@nox.session(name="build-cv")
def build_cv(session: nox.Session) -> None:
    path_to_cv = pathlib.Path("cv/_cv.pdf")

    session.install("pandoc")

    build_refs(session)

    with session.chdir(path_to_cv.parent):
        session.run(
            "pandoc",
            "cv.md",
            "--from=markdown",
            "--citeproc",
            "--lua-filter=multiple-bibliographies.lua",
            "-o",
            path_to_cv.name,
        )
    session.log(f"👉 {path_to_cv!s} 👈")


@nox.session(name="fetch-articles")
def fetch_articles(session: nox.Session) -> None:
    path_to_articles = pathlib.Path("cv/refs/articles.bib")

    url = (
        "https://scholar.googleusercontent.com/"
        "citations?view_op=export_citations&"
        "user=-5-z-Q0AAAAJ&citsig=ACseELIAAAAAZFVeoa3YBX2eweKyqxRBCdcHf00&hl=en"
    )

    with request.urlopen(url) as response:
        with open(path_to_articles, "w") as fp:
            fp.write(response.read().decode("utf-8", errors="backslashreplace"))

    session.log(f"👉 {path_to_articles!s} 👈")
