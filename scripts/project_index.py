"""Search featured projects or render their accessible Markdown index, offline."""
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_projects(path: Path) -> list[dict]:
    projects = json.loads(path.read_text(encoding="utf-8"))["projects"]
    seen = set()
    for project in projects:
        repo = project.get("repo", "")
        if not isinstance(repo, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+", repo):
            raise ValueError("Project repository names must be nonempty GitHub names")
        if repo.casefold() in seen:
            raise ValueError(f"Duplicate project: {repo}")
        seen.add(repo.casefold())
        if not isinstance(project.get("description"), str):
            raise ValueError(f"Missing description for {repo}")
        tags = project.get("technologies", [])
        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            raise ValueError(f"Invalid technologies for {repo}")
    return projects


def search_projects(projects: list[dict], query: str) -> list[dict]:
    terms = query.casefold().split()
    return [project for project in projects if all(
        term in " ".join([project["repo"], project["description"],
                          *project.get("technologies", [])]).casefold()
        for term in terms
    )]


def markdown(projects: list[dict]) -> str:
    def cell(value):
        return html.escape(str(value)).replace("|", "&#124;").replace("\n", " ").replace("\r", " ")

    lines = ["# Featured project index", "",
             "Generated from `assets/projects.json`; descriptions reflect implemented behavior.",
             "", "| Project | What it does | Technologies |", "| --- | --- | --- |"]
    for project in projects:
        repo = project["repo"]
        lines.append(f"| [{cell(repo)}](https://github.com/pralav-25/{repo}) | "
                     f"{cell(project['description'])} | "
                     f"{cell(', '.join(project.get('technologies', [])))} |")
    if not projects:
        lines.extend(["", "No matching projects."])
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--projects", type=Path, default=ROOT / "assets/projects.json")
    parser.add_argument("--search", default="", help="Match all words across names, descriptions and technologies")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", type=Path, help="Write to a file instead of stdout")
    parser.add_argument("--check", action="store_true", help="Fail if the output file needs regeneration")
    args = parser.parse_args(argv)
    if args.check and not args.output:
        parser.error("--check requires --output")
    try:
        projects = search_projects(load_projects(args.projects), args.search)
        result = (json.dumps(projects, ensure_ascii=False, indent=2) + "\n"
                  if args.format == "json" else markdown(projects))
        if args.check:
            if not args.output.exists() or args.output.read_text(encoding="utf-8") != result:
                print(f"Project index is stale: {args.output}")
                return 1
        elif args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(result, encoding="utf-8")
        else:
            print(result, end="")
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
