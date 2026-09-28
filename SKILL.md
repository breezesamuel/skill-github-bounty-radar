---
name: "GitHub Bounty & Lead Radar"
description: "24h autonomous scanner that watches your open PRs for merges and surfaces new open bounty issues matching your skill stack — the client-discovery layer behind a sustained bounty income."
version: "1.0.0"
price: "20.00 USD"
wallet_address: "0x12A2b19eFA9D8BC48ac156Cc8FdfC7cC0Dff36aB"
category: "automation"
tags: ["bounty", "opire", "algora", "github", "automation", "lead-gen", "monitoring"]
author: "breezesamuel"
license: "MIT"
repository: "https://github.com/breezesamuel/skill-github-bounty-radar"
---
# GitHub Bounty & Lead Radar

## What it does
A daemon that every ~15 minutes:
- Watches your open PRs and flags the moment one is merged (the $$ cue).
- Scans GitHub for **new** open bounty issues matching your skill keywords.
- Tracks the freshest open bounties in the repos you care about.
- Writes everything to a rolling log + state file. No push notifications required.

## Why it exists
Bounty income is traffic-independent cash. The bottleneck is *discovery*: by the time a bounty is visible, 5 PRs compete. This radar gives you first-mover signal on new issues.

## Quick start
```bash
python radar.py
```
Set `GH_TOKEN` (or paste into the TOKEN constant). Configure `WATCHED_PRS`, `WATCHED_REPOS`, `SEARCH_QUERIES`.

## Output
- `bounty_radar.log` — every run, with `CLUE` lines for new findings.
- `cache/radar_state.json` — dedup state (only logs each issue once).

## Production proof
Runs continuously on the author's revenue farm (Vercel-hosted products + bounty income).

## Support
Issues: https://github.com/breezesamuel/skill-github-bounty-radar/issues