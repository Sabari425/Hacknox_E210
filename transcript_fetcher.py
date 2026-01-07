import os
import io
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/documents.readonly"
]

TRANSCRIPT_FILE_ID = "PASTE_GOOGLE_DOC_FILE_ID"

def authenticate():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def download_transcript(creds):
    service = build("drive", "v3", credentials=creds)

    request = service.files().export_media(
        fileId=TRANSCRIPT_FILE_ID,
        mimeType="text/plain"
    )

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print("Downloading transcript...")

    with open("meeting_transcript.txt", "wb") as f:
        f.write(fh.getvalue())

    print("Saved as meeting_transcript.txt")


if __name__ == "__main__":
    creds = authenticate()
    download_transcript(creds)
