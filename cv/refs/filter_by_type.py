import re
import sys

import click
import yaml


EXCLUDE = frozenset(
    (
        "kettneragu",
        "masellistratodynamics",
        "nudurupatiprinting",
        "overeemsinking",
        "syvitskichapter",
        "syvitskidelivering",
        "xingcsdms",
    )
)


@click.command()
@click.option("--type", help="type to filter")
@click.argument("file", type=click.File())
def filter_by_type(file, type):
    docs = list(yaml.safe_load_all(file))

    filtered = [_filter_doc(doc, type) for doc in docs if doc]

    print(yaml.dump_all(filtered, explicit_start=True, explicit_end=True))

    all_types = {
        t for types in [_gather_types(doc) for doc in docs if doc] for t in types
    }
    included_types = {
        t for types in [_gather_types(doc) for doc in filtered if doc] for t in types
    }
    excluded_types = all_types - included_types

    print(f"included: {sorted(included_types)!r}", file=sys.stderr)
    print(f"excluded: {sorted(excluded_types)!r}", file=sys.stderr)


def _gather_types(doc):
    return [ref["type"] for ref in doc["references"] if "type" in ref]


def _filter_doc(doc, type_):
    filtered_doc = {k: v for k, v in doc.items() if k != "references"}

    references = []
    for reference in doc["references"]:
        if reference["id"] in EXCLUDE:
            continue
        try:
            reference_type = reference["type"]
        except KeyError:
            pass
        else:
            if re.match(type_, reference_type):
                references.append(reference)

    filtered_doc["references"] = references
    return filtered_doc


if __name__ == "__main__":
    filter_by_type()
