#!/usr/bin/env python3
"""Read-only YouTube Analytics pull for The Fight Playbook.

Runs on Sean's own computer. The OAuth client file and the saved token stay in
the private folder next to this script (never committed: see .gitignore).

Scopes are read-only:
  https://www.googleapis.com/auth/yt-analytics.readonly   (Studio analytics)
  https://www.googleapis.com/auth/youtube.readonly        (channel name, video titles)

usage:
  python3 yt_analytics.py --secrets client_secret.json [--days 28] [--out report.json]
"""
import argparse, datetime as dt, json, os, stat, sys

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
except ImportError:
    sys.exit("Missing packages. Run:\n  python3 -m pip install --user google-auth-oauthlib google-api-python-client")

SCOPES = [
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/youtube.readonly",
]

ap = argparse.ArgumentParser()
ap.add_argument("--secrets", required=True, help="OAuth Desktop client JSON from Google Cloud")
ap.add_argument("--token", default=None, help="where to cache the token (default: next to the secrets file)")
ap.add_argument("--days", type=int, default=28)
ap.add_argument("--out", default=None, help="optional JSON output path")
a = ap.parse_args()

token_path = a.token or os.path.join(os.path.dirname(os.path.abspath(a.secrets)), "token_yt_readonly.json")

creds = None
if os.path.exists(token_path):
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(a.secrets, SCOPES)
        # opens the browser on this computer; Google redirects back to a localhost port
        creds = flow.run_local_server(port=0, prompt="consent", open_browser=True)
    with open(token_path, "w") as f:
        f.write(creds.to_json())
    os.chmod(token_path, stat.S_IRUSR | stat.S_IWUSR)  # owner read/write only

granted = set(creds.scopes or [])
if not granted <= set(SCOPES):
    sys.exit(f"Refusing to continue: token has scopes beyond read-only: {granted - set(SCOPES)}")

yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
ya = build("youtubeAnalytics", "v2", credentials=creds, cache_discovery=False)

from googleapiclient.errors import HttpError
try:
    ch = yt.channels().list(part="snippet,statistics,contentDetails", mine=True).execute()["items"][0]
except HttpError as e:
    print(f"(YouTube Data API unavailable, channel name and titles skipped: {e.reason})")
    ch = {"id": "MINE", "snippet": {"title": "(enable YouTube Data API v3 for the name)"}, "statistics": {}}
cid = ch["id"]
end = dt.date.today()
start_window = end - dt.timedelta(days=a.days)
lifetime_start = dt.date(2005, 2, 14)

def report(start, metrics, dims=None, sort=None, maxr=None, filters=None):
    q = dict(ids="channel==MINE", startDate=start.isoformat(), endDate=end.isoformat(), metrics=metrics)
    if dims: q["dimensions"] = dims
    if sort: q["sort"] = sort
    if maxr: q["maxResults"] = maxr
    if filters: q["filters"] = filters
    r = ya.reports().query(**q).execute()
    cols = [h["name"] for h in r.get("columnHeaders", [])]
    return [dict(zip(cols, row)) for row in r.get("rows", [])]

M = "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,subscribersLost,likes,comments"
life = report(lifetime_start, M)
win = report(start_window, M)
top = report(start_window, M, dims="video", sort="-views", maxr=15)
by_type = report(start_window, "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage", dims="creatorContentType")
traffic = report(start_window, "views,estimatedMinutesWatched", dims="insightTrafficSourceType", sort="-views")

ids = [r["video"] for r in top]
titles = {}
if ids and cid != "MINE":
    for v in yt.videos().list(part="snippet,contentDetails", id=",".join(ids)).execute()["items"]:
        titles[v["id"]] = (v["snippet"]["title"], v["snippet"]["publishedAt"][:10], v["contentDetails"]["duration"])

def hours(m): return f"{(m or 0) / 60:.1f}"
L = life[0] if life else {}
print(f"Channel: {ch['snippet']['title']}  ({cid})")
print(f"Subscribers (public count): {ch['statistics'].get('subscriberCount')}")
print(f"Lifetime views: {L.get('views')}   watch hours: {hours(L.get('estimatedMinutesWatched'))}")
if win:
    W = win[0]
    print(f"Last {a.days} days: views {W['views']}, watch hours {hours(W['estimatedMinutesWatched'])}, "
          f"AVD {W['averageViewDuration']}s, avg viewed {W['averageViewPercentage']:.1f}%, "
          f"subs +{W['subscribersGained']}/-{W['subscribersLost']}")
print("\nShorts vs long form (window):")
for r in by_type:
    print(f"  {r['creatorContentType']:<14} views {r['views']:<7} watch h {hours(r['estimatedMinutesWatched']):<6} AVD {r['averageViewDuration']}s  viewed {r['averageViewPercentage']:.1f}%")
print("\nTop videos (window):")
for r in top:
    t, pub, dur = titles.get(r["video"], ("?", "?", "?"))
    print(f"  {r['views']:>6} views  {hours(r['estimatedMinutesWatched']):>5} h  AVD {r['averageViewDuration']:>4}s  {r['averageViewPercentage']:5.1f}%  {pub}  {dur:<9} {t}")
print("\nTraffic sources (window):")
for r in traffic[:8]:
    print(f"  {r['insightTrafficSourceType']:<22} {r['views']} views")

if a.out:
    json.dump(dict(channel=dict(id=cid, title=ch["snippet"]["title"], stats=ch["statistics"]),
                   lifetime=life, window_days=a.days, window=win, by_type=by_type,
                   top_videos=[dict(r, title=titles.get(r["video"], ("",))[0]) for r in top], traffic=traffic),
              open(a.out, "w"), indent=1)
    print(f"\nSaved {a.out}")
