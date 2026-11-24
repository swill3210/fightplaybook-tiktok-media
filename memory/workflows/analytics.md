---
type: knowledge
area: analytics
updated: 2026-11-24
---
# Analytics access check and missing data policy

## Access check (run before any analysis or topic decision)
1. Token present: `/root/.config/fightplaybook/token_yt_readonly.json` exists in the session (it does not survive a new container).
2. Scopes are read only: exactly `yt-analytics.readonly` and `youtube.readonly`. Anything else: stop and do not use the token.
3. Live call works: `python3 production/analytics/yt_analytics.py --secrets client_secret.json --days 28` returns the channel totals without an HTTP error.
4. Identity: the video IDs returned include known Fight Playbook uploads (for example `ZxX74dpPbu0`, `QDmUFEn6JoA`). If not, the wrong channel was authorised: stop.
5. Freshness: record the end date of the data in every report. YouTube Analytics lags about 48 hours.
6. Write the result of the check at the top of every analysis note: PASS (live), PARTIAL (which metrics missing) or FAIL (why).

## What the read only API can and cannot give
| Metric | Source | Notes |
| --- | --- | --- |
| Views, watch time, average view duration, percent viewed, subscribers, likes, comments, traffic sources, demographics, devices | YouTube Analytics API v2 | Available live |
| Audience retention curve per video | YouTube Analytics API v2 (`audienceWatchRatio` by `elapsedVideoTimeRatio`) | Available; small videos may return too few points |
| Thumbnail impressions and impressions CTR | NOT in the Analytics API. Only YouTube Studio, or the YouTube Reporting API bulk reach reports (a job must be created, first data after about 24 to 48 hours) | Missing unless Sean exports from Studio or a Reporting job exists |
| A/B thumbnail test results | Studio only | Missing unless Sean shares a screenshot or export |
| Competitor analytics | Never available | Use public view counts, upload dates and transcripts only, labelled as public data |

## How to handle missing analytics
1. Never invent or estimate a number and present it as data. Label every figure: VERIFIED (API, date), STUDIO EXPORT (date), PUBLIC (competitor page, date) or ESTIMATE (method).
2. If the token is missing or expired: ask Sean for a one time browser sign in (same OAuth client, read only). Until then, use the newest saved report in `Claude Production/05 Analytics/Reports` and state its date.
3. If a metric is missing (CTR, impressions, A/B): say it is missing in the report, use the newest Studio snapshot if one exists (Nov 13 snapshot in the handoff repo: long form CTR 2.4 to 4.0 percent, Shorts shelf CTR 10.5 percent), and ask Sean for a Studio export when the decision depends on it.
4. If retention is missing for a video (too few views): do not infer it from other videos; mark it "not enough data".
5. Decisions made with missing data are labelled "provisional" and revisited when the data arrives.
