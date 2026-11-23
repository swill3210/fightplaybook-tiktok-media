#!/usr/bin/env python3
"""Write YouTube Analytics (read only) into the Obsidian vault as new dated notes.

Never overwrites: if a note with the target name exists, a numbered copy is written instead.
No credentials are written into the vault.

usage: python3 vault_sync.py --token <token_yt_readonly.json> --vault <vault dir> [--days 28]
"""
import argparse, datetime as dt, os, sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

ap = argparse.ArgumentParser()
ap.add_argument("--token", required=True)
ap.add_argument("--vault", required=True)
ap.add_argument("--days", type=int, default=28)
ap.add_argument("--subdir", default="Claude Production", help="Claude only writes inside this folder of the vault")
a = ap.parse_args()

creds = Credentials.from_authorized_user_file(a.token)
if not set(creds.scopes or []) <= {"https://www.googleapis.com/auth/yt-analytics.readonly", "https://www.googleapis.com/auth/youtube.readonly"}:
    sys.exit("token is not read only; refusing")
ya = build("youtubeAnalytics", "v2", credentials=creds, cache_discovery=False)
yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
today = dt.date.today()
end = today.isoformat()
start = (today - dt.timedelta(days=a.days)).isoformat()

def q(metrics, dims=None, filters=None, sort=None, maxr=None, s=start):
    p = dict(ids="channel==MINE", startDate=s, endDate=end, metrics=metrics)
    for k, v in (("dimensions", dims), ("filters", filters), ("sort", sort), ("maxResults", maxr)):
        if v: p[k] = v
    r = ya.reports().query(**p).execute()
    cols = [h["name"] for h in r.get("columnHeaders", [])]
    return [dict(zip(cols, row)) for row in r.get("rows", [])]

def titles_for(ids):
    out = {}
    try:
        for i in range(0, len(ids), 50):
            for v in yt.videos().list(part="snippet", id=",".join(ids[i:i + 50])).execute().get("items", []):
                out[v["id"]] = v["snippet"]["title"]
        return out, True
    except HttpError:
        return out, False

def write_new(rel, text):
    path = os.path.join(a.vault, a.subdir, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    base, ext = os.path.splitext(path)
    n = 2
    while os.path.exists(path):
        path = f"{base} ({n}){ext}"; n += 1
    with open(path, "x") as f:
        f.write(text)
    print("wrote", os.path.relpath(path, a.vault))

mmss = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
M = "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,subscribersLost"
tot = q(M)
types = q("views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained", dims="creatorContentType")
traffic = q("views", dims="insightTrafficSourceType", sort="-views")
shorts = q(M, dims="video", filters="creatorContentType==shorts", sort="-views", maxr=15)
longs = q(M, dims="video", filters="creatorContentType==videoOnDemand", sort="-views", maxr=25)
names, have_titles = titles_for([r["video"] for r in shorts + longs])
name = lambda v: names.get(v, "(title needs YouTube Data API v3)")

T = tot[0] if tot else {}
lines = [
    "---", "type: analytics-report", f"date: {end}", f"window_days: {a.days}", "source: YouTube Analytics API v2 (read only), verified numbers", "---",
    f"# Channel report {end} (last {a.days} days)", "",
    "| Metric | Value |", "| --- | --- |",
    f"| Views | {T.get('views', 0):,} |",
    f"| Watch hours | {T.get('estimatedMinutesWatched', 0) / 60:.1f} |",
    f"| Average view duration | {mmss(T.get('averageViewDuration', 0))} |",
    f"| Average % viewed | {T.get('averageViewPercentage', 0):.1f}% |",
    f"| Subscribers | +{T.get('subscribersGained', 0)} / -{T.get('subscribersLost', 0)} |", "",
    "## Shorts vs long form", "", "| Type | Views | Watch h | AVD | % viewed | Subs gained |", "| --- | --- | --- | --- | --- | --- |",
]
for r in types:
    lines.append(f"| {r['creatorContentType']} | {r['views']:,} | {r['estimatedMinutesWatched'] / 60:.1f} | {mmss(r['averageViewDuration'])} | {r['averageViewPercentage']:.1f}% | {r['subscribersGained']} |")
lines += ["", "## Traffic sources", "", "| Source | Views |", "| --- | --- |"] + [f"| {r['insightTrafficSourceType']} | {r['views']:,} |" for r in traffic[:10]]
for label, rows in (("Long form videos", longs), ("Top Shorts", shorts)):
    lines += ["", f"## {label}", "", "| Video | Title | Views | Watch h | AVD | % viewed | Subs |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for r in rows:
        lines.append(f"| [{r['video']}](https://youtu.be/{r['video']}) | {name(r['video'])} | {r['views']:,} | {r['estimatedMinutesWatched'] / 60:.1f} | {mmss(r['averageViewDuration'])} | {r['averageViewPercentage']:.1f}% | +{r['subscribersGained']} |")
if not have_titles:
    lines += ["", "> Titles missing: enable YouTube Data API v3 on the Google Cloud project, then rerun."]
write_new(f"05 Analytics/Reports/{end} Channel Report.md", "\n".join(lines) + "\n")

# retention curves for every long form video with data
rl = ["---", "type: retention", f"date: {end}", "source: YouTube Analytics API v2, audienceWatchRatio by elapsedVideoTimeRatio, organic traffic", "---",
      f"# Long form retention {end}", "",
      "Share of the starting audience still watching at each point of the video (1.00 = everyone who started).", "",
      "| Video | Title | 5% | 10% | 20% | 30% | 50% | 75% | 95% | Lost by 10% |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
for r in longs:
    v = r["video"]
    try:
        rows = q("audienceWatchRatio", dims="elapsedVideoTimeRatio", filters=f"video=={v};audienceType==ORGANIC", s="2026-01-01")
    except HttpError:
        continue
    if len(rows) < 20:
        continue
    pts = {round(x["elapsedVideoTimeRatio"], 2): x["audienceWatchRatio"] for x in rows}
    g = lambda p: pts.get(p, float("nan"))
    rl.append(f"| [{v}](https://youtu.be/{v}) | {name(v)} | " + " | ".join(f"{g(p):.2f}" for p in (0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 0.95)) + f" | {1 - g(0.1):.0%} |")
write_new(f"05 Analytics/Retention/{end} Long Form Retention.md", "\n".join(rl) + "\n")
