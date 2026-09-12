# Maintaining this profile

Featured card descriptions live in `assets/projects.json`. The scheduled
[asset workflow](../.github/workflows/radar.yml) refreshes API-backed statistics;
project descriptions remain editorial and should describe implemented behavior.
Run `python -m unittest discover -s tests -v` before changing the SVG generators.

The profile uses local light and dark SVG banners in `assets/profile-banner-*.svg`.
Keep their accessible titles and the README image description in sync when editing
the visible text. Profile claims should link to implemented behavior and public
evidence; the native GitHub achievement panel remains the source for earned badges.

If the optional GraphQL contribution request times out or returns incomplete data,
the generator omits its contribution tiles and still renders the available REST
statistics and project cards. It does not turn unavailable counts into zero.

## Preview profile cards

From the repository root, render a preview without replacing the committed assets:

```bash
python scripts/cards.py --user pralav-25 --projects assets/projects.json --out /tmp/pralav-profile-cards
```

Open both `card-stats-dark.svg` and `card-stats-light.svg` in the output directory
to check text and contrast. Public repository statistics work without a token;
contribution and streak tiles require `GITHUB_TOKEN`. Keep the featured-work
table and `assets/projects.json` descriptions consistent when updating a project.
