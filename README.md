# jetpunk-score-scraper

Scrapes jetpunk.com for your daily quiz scores.

To install, clone this repo and install with `pipx` via

```bash
pipx install .
```

After running `pipx ensurepath` if necessary (you will be notified of this), the command-line utility `scrape-jetpunk` will be available. Running the command

```bash
scrape-jetpunk <username>
```

will (after entering your password at the prompt) save your scores to `scores.csv`.

Some customisation options are available. Run `scrape-jetpunk --help` for a list of available options.

## Authors

Christian Chapman-Bird
