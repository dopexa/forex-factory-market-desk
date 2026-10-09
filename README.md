# Market desk — GitHub Pages

This folder is the root of the GitHub repository for the site. It contains a static dashboard and a GitHub Actions workflow that refreshes the news feed and publishes the site to GitHub Pages.

## Live headlines

The workflow reads headline metadata from Google News RSS searches focused on FX, currencies, central banks, and commodities. It publishes the headline, publisher, publication time, and link to the original story in `news.json`. The site refreshes from that file every five minutes and links out to publishers; it does not republish article text.

GitHub Pages cannot run server-side application code. GitHub Actions creates the static JSON file before each Pages deployment instead. GitHub scheduled workflows have a five-minute minimum interval, but GitHub may delay scheduled runs during high load, so headline updates are periodic rather than guaranteed real-time.

Quotes, calendar values, positioning, and forum posts in this prototype are sample data.

## Publish

1. Create a GitHub repository and upload the contents of this folder to its default branch named `main`.
2. In the repository, open **Settings → Pages** and set the build and deployment source to **GitHub Actions**.
3. Open **Actions** and confirm that **Publish market desk to GitHub Pages** has completed. The live URL appears in the workflow deployment environment.

The workflow publishes on pushes to `main`, on manual dispatch, and on a five-minute schedule. The repository owner must authorize the first Pages deployment.
