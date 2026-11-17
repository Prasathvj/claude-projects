#!/usr/bin/env python3
"""Upload a reviewed video folder to YouTube as PRIVATE (optionally scheduled).

    python upload.py output/why-you-procrastinate                 # long + short, private
    python upload.py output/foo --only short
    python upload.py output/foo --publish-at 2026-12-01T14:30:00Z # goes public at that time

One-time setup: create an OAuth "Desktop app" client in Google Cloud Console with the
YouTube Data API v3 enabled, and save it as client_secret.json next to this file.
"""
import argparse
import json
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

ROOT = Path(__file__).resolve().parent
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def youtube():
    token = ROOT / "token.json"
    creds = Credentials.from_authorized_user_file(str(token), SCOPES) if token.exists() else None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = InstalledAppFlow.from_client_secrets_file(str(ROOT / "client_secret.json"), SCOPES) \
                .run_local_server(port=0)
        token.write_text(creds.to_json())
    return build("youtube", "v3", credentials=creds)


def upload(yt, file, title, description, tags, publish_at):
    status = dict(privacyStatus="private", selfDeclaredMadeForKids=False)
    if publish_at:
        status["publishAt"] = publish_at
    body = dict(snippet=dict(title=title[:100], description=description, tags=tags, categoryId="27"),
                status=status)
    req = yt.videos().insert(part="snippet,status", body=body,
                             media_body=MediaFileUpload(str(file), chunksize=-1, resumable=True))
    video_id = req.execute()["id"]
    print(f"uploaded {file.name}: https://youtu.be/{video_id}")
    return video_id


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--only", choices=["long", "short"])
    ap.add_argument("--publish-at", help="ISO time (UTC) to make the video public")
    args = ap.parse_args()

    folder = Path(args.folder)
    meta = json.loads((folder / "metadata.json").read_text())
    yt = youtube()

    if "long" in meta and args.only != "short":
        vid = upload(yt, folder / meta["long"]["file"], meta["title"], meta["description"], meta["tags"],
                     args.publish_at)
        try:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(
                str(folder / meta["long"]["thumbnail"]))).execute()
        except Exception as e:  # custom thumbnails need a phone-verified channel
            print(f"thumbnail not set: {e}")
    if "short" in meta and args.only != "long":
        s = meta["short"]
        upload(yt, folder / s["file"], s["title"], s["description"], meta["tags"], args.publish_at)


if __name__ == "__main__":
    main()
