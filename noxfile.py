import pathlib
from urllib import request

import nox

ROOT = pathlib.Path(__file__).parent


@nox.session
def lint(session: nox.Session) -> None:
    """Look for lint."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", "--verbose")


@nox.session(name="build-refs")
def build_refs(session: nox.Session) -> None:
    article_pattern = "(article-journal|chapter)"

    session.install("-r", "requirements.in")

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
    session.install("pandoc")

    build_refs(session)

    args = [
        ("-o", "_cv.md", "-t", "markdown_strict"),
        ("-o", "_cv.pdf", "-t", "pdf"),
    ]
    with session.chdir(ROOT / "cv"):
        for arg in args:
            session.run(
                "pandoc",
                "cv.md",
                "--from=markdown",
                "--citeproc",
                "--lua-filter=multiple-bibliographies.lua",
                *arg,
            )
    # session.log(f"👉 {path_to_cv!s} 👈")


@nox.session(name="fetch-articles")
def fetch_articles(session: nox.Session) -> None:
    path_to_articles = pathlib.Path("cv/refs/articles.bib")

    url = (
        "https://scholar.googleusercontent.com/"
        "citations?view_op=export_citations&"
        "user=-5-z-Q0AAAAJ&citsig=AIIUsnMAAAAAZltb4AemAKbLeEl0ov-3aqs8-FE&hl=en"
    )

    with request.urlopen(url) as response:
        with open(path_to_articles, "w") as fp:
            fp.write(response.read().decode("utf-8", errors="backslashreplace"))

    session.log(f"👉 {path_to_articles!s} 👈")


@nox.session(name="build-docs")
def build_docs(session: nox.Session) -> None:
    """Build the docs."""
    session.install("-r", "docs/requirements.in")

    (ROOT / "build").mkdir(exist_ok=True)
    session.run(
        "sphinx-build",
        "-b",
        "html",
        "-W",
        "--keep-going",
        ROOT / "docs",
        ROOT / "build" / "html",
    )
    session.log(f"generated docs at {ROOT / 'build' / 'html'!s}")
