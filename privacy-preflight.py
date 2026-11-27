#!/usr/bin/env python3
"""Read-only preflight for the free journal. Run in the operator's Google Cloud Shell."""
import json
import subprocess
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

PROJECT = "bride-journal"
BASE = "b330215cf5b4c416b508db572a1ffd8824508af8"
ROOT = Path(__file__).resolve().parent
def normalized(text):
    return text.lstrip("\ufeff").replace("\r\n", "\n").strip()
def main():
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"], text=True).strip()
    def read(resource, payload=None):
        req = Request(resource, headers={"Authorization": "Bearer " + token,
                      "Content-Type": "application/json", "x-goog-user-project": PROJECT},
                      data=json.dumps(payload).encode() if payload else None)
        with urlopen(req, timeout=25) as response:
            return json.load(response)
    api = "https://firebaserules.googleapis.com/v1/"
    release = read(api + "projects/" + PROJECT + "/releases/cloud.firestore")
    active = read(api + release["rulesetName"])
    files = active["source"]["files"]
    baseline = subprocess.check_output(["git", "show", BASE + ":firestore.rules"], cwd=ROOT, text=True)
    match = len(files) == 1 and normalized(files[0]["content"]) == normalized(baseline)
    print("project:", PROJECT)
    print("active Firestore rules match reviewed baseline:", "YES" if match else "NO")
    admin = read("https://identitytoolkit.googleapis.com/v1/projects/" + PROJECT + "/accounts:lookup",
                 {"email": ["matatmail@gmail.com"]})
    verified = any(u.get("emailVerified") and not u.get("disabled") for u in admin.get("users", []))
    print("admin email verified and enabled:", "YES" if verified else "NO")
    return 0 if match and verified else 2
if __name__ == "__main__":
    try:
        sys.exit(main())
    except HTTPError as error:
        sys.exit("Read-only check could not finish: HTTP " + str(error.code) + ". No changes made.")
