#!/usr/bin/env python3
"""24h bounty/lead radar: PR-merge watch + new open-bounty scan + repo watch.
Docs: see SKILL.md. Runs forever under an outer loop (cron / powershell loop)."""
import json
import os
import urllib.request
import urllib.parse
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(BASE, "cache")
os.makedirs(CACHE, exist_ok=True)
LOG = os.path.join(BASE, "bounty_radar.log")
STATE = os.path.join(CACHE, "radar_state.json")

TOKEN = os.environ.get("GH_TOKEN") or "PASTE_YOUR_GITHUB_TOKEN"
WATCHED_PRS = [("owner/repo", 1)]  # (repo, pr_number)
WATCHED_REPOS = ["owner/repo"]  # repos to list open bounties
SEARCH_QUERIES = {
    "payments": "is:issue is:open (algora OR opire) (webhook OR payment OR stripe) created:>30d",
    "webstack": "is:issue is:open label:bounty (nextjs OR typescript OR prisma) created:>30d",
}


def now():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")


def log(m):
    line = "[%s] %s" % (now(), m)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


def get(url):
    r = urllib.request.Request(url, headers={"Authorization": "token " + TOKEN, "User-Agent": "radar"})
    with urllib.request.urlopen(r, timeout=30) as resp:
        return json.loads(resp.read().decode())


def load():
    try:
        with open(STATE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"seen": [], "last_pr": {}}


def save(st):
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, indent=2)


def watch_prs(st):
    for repo, num in WATCHED_PRS:
        try:
            pr = get("https://api.github.com/repos/%s/pulls/%s" % (repo, num))
            prev = st["last_pr"].get(str(num), {})
            if pr.get("merged") and not prev.get("merged"):
                log("!!! PR #%s (%s) MERGED" % (num, repo))
            st["last_pr"][str(num)] = {"merged": bool(pr.get("merged")), "state": pr.get("state")}
            log("PR #%s: %s merged=%s" % (num, repo, pr.get("merged")))
        except Exception as e:
            log("pr %s/%s ERR: %s" % (repo, num, e))


def scan_new(st):
    for key, q in SEARCH_QUERIES.items():
        try:
            d = get("https://api.github.com/search/issues?q=" + urllib.parse.quote(q) + "&sort=created&order=desc&per_page=8")
            for it in d.get("items", [])[:8]:
                iid = str(it["id"])
                if iid not in st["seen"]:
                    st["seen"].append(iid)
                    repo = it["repository_url"].replace("https://api.github.com/repos/", "")
                    log("CLUE %s #%s %s (%s) cmts=%s" % (
                        repo, it["number"], it["title"][:60], it["created_at"][:10], it["comments"]))
        except Exception as e:
            log("scan %s ERR: %s" % (key, e))
    st["seen"] = st["seen"][-400:]


def main():
    st = load()
    log("=== radar round ===")
    watch_prs(st)
    scan_new(st)
    save(st)
    log("=== round end ===")


if __name__ == "__main__":
    main()