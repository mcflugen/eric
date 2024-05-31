import os
import pathlib

from dateutil.relativedelta import relativedelta
from datetime import date


project = "Eric Hutton"
copyright = "2024, Eric Hutton"
author = "Eric Hutton"

alive = relativedelta(date.today(), date(1973, 3, 14))
version = f"{alive.years}.{alive.months}.{alive.days}"
release = version

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx_copybutton",
    "sphinx_inline_tabs",
]

# Add any paths that contain templates here, relative to this directory.
# templates_path = ["_templates"]

language = "en"
pygments_style = "sphinx"
todo_include_todos = False
html_static_path = ["_static"]
html_theme = "furo"
html_static_path = ["_static"]

html_theme_options = {
    "light_logo": "eric-logo-light.png",
    "dark_logo": "eric-logo-dark.png",
    "source_repository": "https://github.com/mcflugen/cv/",
    "source_branch": "main",
    "source_directory": "docs/source",
    "footer_icons": [
        {
            "name": "power",
            "url": "https://csdms.colorado.edu",
            "html": """
               <svg stroke="currentColor" fill="currentColor" stroke-width="0" version="1.1" viewBox="0 0 16 16" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M6 0l-6 8h6l-4 8 14-10h-8l6-6z"></path></svg>
               <b><i>Powered by CSDMS</i></b>
            """,
            "class": "",
        },
    ],
}

myst_enable_extensions = ["colon_fence"]
