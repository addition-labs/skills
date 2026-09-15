#!/usr/bin/env python3
"""Pull Search Console performance rows through the API for two comparison windows (v2.0.0, 2026-09-15).

Writes a NEW run directory <out>/<property-slug>/<end-date>/ with:
  current.csv, previous.csv          query x page x device rows (unrounded ctr and position)
  current_pages.csv, previous_pages.csv   page-only rows, for page-level comparison
  manifest.json                      property, search type, dimensions, filters, windows, reporting
                                     timezone, row counts, completion status
Pagination collects the rows the API exposes; it does not recover anonymized queries or guarantee a
complete query table. Exhaustion means "no further rows returned for this request".
Network: Google OAuth authorization/token services and the Search Console API (read-only scope).
"""
import argparse, csv, datetime as dt, json, sys, traceback
from pathlib import Path
try:
    from zoneinfo import ZoneInfo
except ImportError:  # Python < 3.9
    ZoneInfo = None
try:
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
except ImportError:
    sys.exit("Missing dependencies. In the virtual environment from Setup: pip install google-api-python-client google-auth-oauthlib")

VERSION = "2.0.0"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
PAGE = 25000          # documented maximum rows per request
SEARCH_TYPE = "web"
REPORTING_TZ = "America/Los_Angeles"   # Search Console reports in Pacific time


def creds(secret: Path, token: Path):
    c = Credentials.from_authorized_user_file(token, SCOPES) if token.is_file() else None
    if not c or not c.valid:
        if c and c.expired and c.refresh_token:
            c.refresh(Request())
        else:
            if not secret.is_file():
                sys.exit(f"OAuth client file not found: {secret}. See SKILL.md Setup.")
            c = InstalledAppFlow.from_client_secrets_file(str(secret), SCOPES).run_local_server(port=0)
        token.parent.mkdir(parents=True, exist_ok=True)
        token.write_text(c.to_json())
    return c


def pull(svc, site, start, end, dimensions):
    rows, start_row = [], 0
    while True:
        body = {"startDate": start.isoformat(), "endDate": end.isoformat(), "dimensions": dimensions,
                "type": SEARCH_TYPE, "rowLimit": PAGE, "startRow": start_row}
        r = svc.searchanalytics().query(siteUrl=site, body=body).execute()
        batch = r.get("rows", [])
        for b in batch:
            row = dict(zip(dimensions, b["keys"]))
            row.update(clicks=b["clicks"], impressions=b["impressions"], ctr=b["ctr"], position=b["position"])
            rows.append(row)
        print(f"  {'/'.join(dimensions)} {start}..{end}: +{len(batch)} rows (total {len(rows)})", flush=True)
        if len(batch) < PAGE:
            print("  no further rows returned for this request", flush=True)
            return rows
        start_row += PAGE


def write_csv(path, fields, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--site", required=True, help='exact property, e.g. "sc-domain:example.com" or "https://www.example.com/"')
    ap.add_argument("--client-secret", type=Path, required=True, help="path to the downloaded Desktop OAuth client JSON")
    ap.add_argument("--token", type=Path, default=None, help="where the cached token is created or updated (default: token.json beside the client file)")
    ap.add_argument("--out", type=Path, required=True, help="root directory for pull runs; the run directory is created under it")
    ap.add_argument("--days", type=int, default=28, help="window length in days (> 0)")
    ap.add_argument("--lag", type=int, default=3, help="days subtracted from the reporting date for finalization (>= 0)")
    ap.add_argument("--end", default=None, help="explicit end date YYYY-MM-DD for the current window (overrides --lag)")
    a = ap.parse_args()
    if a.days <= 0:
        ap.error("--days must be greater than 0")
    if a.lag < 0:
        ap.error("--lag must be 0 or more")
    secret = a.client_secret.expanduser().resolve()
    token = (a.token.expanduser().resolve() if a.token else secret.parent / "token.json")
    if a.end:
        try:
            end = dt.date.fromisoformat(a.end)
        except ValueError:
            ap.error("--end must be YYYY-MM-DD")
    else:
        today = dt.datetime.now(ZoneInfo(REPORTING_TZ)).date() if ZoneInfo else dt.date.today()
        end = today - dt.timedelta(days=a.lag)
    cur_start = end - dt.timedelta(days=a.days - 1)
    prev_end = cur_start - dt.timedelta(days=1)
    prev_start = prev_end - dt.timedelta(days=a.days - 1)
    slug = a.site.replace("sc-domain:", "").replace("https://", "").replace("http://", "").strip("/").replace("/", "_")
    out = a.out.expanduser().resolve() / slug / end.isoformat()
    if out.exists():
        ap.error(f"run directory already exists: {out}. Every pull writes to a new directory.")
    out.mkdir(parents=True, exist_ok=False)

    manifest = dict(version=VERSION, property=a.site, search_type=SEARCH_TYPE, filters=[], reporting_timezone=REPORTING_TZ,
                    windows=dict(current=dict(start=cur_start.isoformat(), end=end.isoformat()),
                                 previous=dict(start=prev_start.isoformat(), end=prev_end.isoformat())),
                    files={}, completed=False, status="incomplete", error=None,
                    note="Pagination collects the rows the API exposes; it does not recover anonymized queries or guarantee a complete query table.")
    def save():
        (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    save()
    try:
        svc = build("searchconsole", "v1", credentials=creds(secret, token))
        plan = [("current", cur_start, end, ["query", "page", "device"], "current.csv"),
                ("previous", prev_start, prev_end, ["query", "page", "device"], "previous.csv"),
                ("current", cur_start, end, ["page"], "current_pages.csv"),
                ("previous", prev_start, prev_end, ["page"], "previous_pages.csv")]
        for window, s, e, dims, name in plan:
            rows = pull(svc, a.site, s, e, dims)
            write_csv(out / name, dims + ["clicks", "impressions", "ctr", "position"], rows)
            manifest["files"][name] = dict(window=window, dimensions=dims, rows=len(rows))
            save()
            print(f"{name}: {len(rows)} rows ({s} to {e})")
    except SystemExit:
        raise
    except Exception as exc:  # auth, quota, network: keep the run as incomplete evidence, never analyze it
        manifest["error"] = f"{type(exc).__name__}: {exc}"
        save()
        (out / "error.txt").write_text(traceback.format_exc())
        sys.exit(f"INCOMPLETE RUN {out}: {manifest['error']}. Recovery: check the OAuth consent, property access and API quota, then run again into a new directory.")
    manifest["completed"] = True; manifest["status"] = "complete"; save()
    print("OUT", out)


if __name__ == "__main__":
    main()
