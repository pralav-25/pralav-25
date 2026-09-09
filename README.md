# Hi, I'm Pralav Singh

I'm seeking **data science / ML internships**. My current focus is reproducible
model evaluation, numerical data monitoring, and Python tools that make results
inspectable. I also build the APIs and interfaces around these workflows.

[Portfolio](https://pralav-singh-portfolio.vercel.app) ·
[Email](mailto:singhpralav07@gmail.com) · Based in India

## Start with ShiftWatch

[**ShiftWatch**](https://github.com/pralav-25/shiftwatch) compares a dummy baseline,
logistic regression, and a random forest on UCI Wine with training-only
cross-validation. It evaluates a separate holdout, then examines synthetic feature
shifts and missingness with a Python drift library and an interactive dashboard.

- [Executed analysis notebook](https://github.com/pralav-25/shiftwatch/blob/main/notebooks/wine-monitoring-analysis.ipynb): training-data exploration, fold scores, holdout errors, and drift interpretation.
- [Interactive results](https://pralav-25.github.io/shiftwatch/): inspect prediction metrics, feature distributions, and data-quality alerts.
- [Methodology and limitations](https://github.com/pralav-25/shiftwatch/blob/main/docs/methodology.md): preprocessing isolation, multiple testing, and what the monitor cannot establish.
- [Tests and reproduction](https://github.com/pralav-25/shiftwatch/actions/workflows/ci.yml): numerical checks, CLI behavior, report reproduction, and notebook execution.

The shifted scenarios are synthetic and the dataset is small. This is an
educational workbench; its scores are not claims of production performance.

## Supporting engineering projects

| Project | Evidence to inspect | Links |
|---|---|---|
| **StructIQ** | FastAPI infrastructure-maintenance app with private workspaces, photo reports, audit history, and SQLite/PostgreSQL persistence. | [Source and setup](https://github.com/pralav-25/StructIQ) · [API tests](https://github.com/pralav-25/StructIQ/tree/main/tests) |
| **Interleave** | Six deterministic concurrency experiments with shareable replays, private investigations, and local AI trace assistance. | [Source and architecture](https://github.com/pralav-25/interleave) · [Live workbench](https://interleave-pralav.vercel.app) |
| **Developer portfolio** | Project walkthroughs and working interfaces built with TypeScript and React. | [Source](https://github.com/pralav-25/pralav-25.github.io) · [Portfolio](https://pralav-singh-portfolio.vercel.app) |

## Tools used in these projects

- **Data and ML:** Python, NumPy, pandas, SciPy, scikit-learn, Matplotlib, Jupyter
- **Backend and persistence:** FastAPI, SQLAlchemy, PostgreSQL, SQLite
- **Interfaces:** TypeScript, React, HTML, CSS, Tailwind CSS
- **Validation and delivery:** pytest, Ruff, Git, GitHub Actions

I also edit short-form and sports video in DaVinci Resolve. My current internship
search is focused on data science and machine learning.

## GitHub activity

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-stats-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/card-stats-light.svg">
    <img src="assets/card-stats-dark.svg" width="480" alt="Pralav Singh's GitHub activity summary">
  </picture>
</p>

## Contact

- Email: [singhpralav07@gmail.com](mailto:singhpralav07@gmail.com)
- Video work: [@ig_sinisterrrr](https://www.instagram.com/ig_sinisterrrr/)
- GitHub: [@pralav-25](https://github.com/pralav-25)

## Maintaining this profile

Featured card descriptions live in `assets/projects.json`. The scheduled
[asset workflow](.github/workflows/radar.yml) refreshes API-backed statistics;
project descriptions remain editorial and should describe implemented behavior.
Run `python -m unittest discover -s tests -v` before changing the SVG generators.

### Preview profile cards

From the repository root, render a preview without replacing the committed assets:

```bash
python scripts/cards.py --user pralav-25 --projects assets/projects.json --out /tmp/pralav-profile-cards
```

Open both `card-stats-dark.svg` and `card-stats-light.svg` in the output directory
to check text and contrast. Public repository statistics work without a token;
contribution and streak tiles require `GITHUB_TOKEN`. Keep the featured-work
table and `assets/projects.json` descriptions consistent when updating a project.
