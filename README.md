# skill-github-bounty-radar

24h autonomous GitHub bounty & client-lead radar.

- `SKILL.md` — SkillShop manifest ($20, USDC on Base)
- `radar.py` — the production scanner (single file, zero deps)

Run: `python radar.py` (wrap in cron / a powershell loop / a supervisor for 24h coverage).

Configure `WATCHED_PRS`, `WATCHED_REPOS`, `SEARCH_QUERIES`, `TOKEN`.