# My CV in markdown

To build,

    nox -s build-cv copy-to-docs build-docs

Articles are in *bibtex* format in `cv/refs/articles.bib`, which was taken
from google scholar.

To fetch the latest list of articles from Google Scholar,

    nox -s fetch-articles
