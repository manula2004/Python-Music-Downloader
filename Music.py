import urllib.request
from urllib.parse import urljoin
import os
import subprocess
import json
from pathlib import Path
import re
from concurrent.futures import ThreadPoolExecutor

# ---------------- CONFIG ----------------
BASE_URL = "http://www.infolanka.com/miyuru_gee/"
ARTIST_LIST_URL = urljoin(BASE_URL, "art/art.html")
WORKING_DIR = "."
MAX_WORKERS = 8

# ---------------- HTTP ----------------
def fetch_html(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req) as r:
        return r.read().decode(errors="ignore")

# ---------------- ARTISTS ----------------
def get_artists():
    print("Loading artist list...")
    html = fetch_html(ARTIST_LIST_URL)
    # regex to match <a href="xxx.html">Artist Name</a>
    matches = re.findall(
        r'href="([^"]+\.html)".*?>([^<]+)</a>',
        html, re.IGNORECASE
    )
    artists = []
    for file, name in matches:
        name = name.strip()
        if name and file.endswith(".html"):
            artists.append((name, file))
    return artists

def choose_artist():
    artists = get_artists()
    print(f"\nFound {len(artists)} artists:\n")
    for i, (name, _) in enumerate(artists):
        print(f"{i+1}. {name}")
    choice = int(input("\nChoose artist number: ")) - 1
    name, file = artists[choice]
    url = urljoin(BASE_URL + "art/", file)
    print(f"\nSelected: {name}\n")
    return url

# ---------------- AUDIO LINKS ----------------
def get_audio_links(html):
    return re.findall(
        r'href="([^"]+\.(?:ram|ra))"',
        html, re.IGNORECASE
    )

# ---------------- HELPERS ----------------
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def get_metadata(file_path):
    try:
        result = subprocess.run(
            ["ffprobe","-v","quiet","-print_format","json","-show_format", str(file_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        data = json.loads(result.stdout)
        tags = data.get("format", {}).get("tags", {})
        title = tags.get("title")
        artist = tags.get("artist")
        return artist, title
    except:
        return None, None

def download_file(url, name):
    path = os.path.join(WORKING_DIR, name)
    try:
        urllib.request.urlretrieve(url, path)
        print("Downloaded:", name)
        return path
    except:
        print("Failed:", name)
        return None

def process_ram(path):
    try:
        with open(path) as f:
            url = f.read().strip()
        name = url.split("/")[-1]
        return url, name
    except:
        return None, None

def rename_audio(file):
    artist, title = get_metadata(file)
    if not artist or not title:
        return
    new = f"{sanitize_filename(artist)} - {sanitize_filename(title)}.ra"
    new_path = file.with_name(new)
    if not new_path.exists():
        file.rename(new_path)
        print("Renamed:", new)

# ---------------- MAIN ----------------
def main():
    print("Starting audio file processor...\n")
    page_url = choose_artist()
    html = fetch_html(page_url)
    links = get_audio_links(html)
    print(f"Found {len(links)} files\n")
    
    # Download initial .ra / .ram files
    with ThreadPoolExecutor(MAX_WORKERS) as ex:
        futures = []
        for l in links:
            url = urljoin(BASE_URL + "art/", l)
            name = url.split("/")[-1]
            futures.append(ex.submit(download_file, url, name))
        files = [f.result() for f in futures if f.result()]

    # Process .ram files
    ram = [f for f in files if f.endswith(".ram")]
    if ram:
        with ThreadPoolExecutor(MAX_WORKERS) as ex:
            tasks = [ex.submit(process_ram, r) for r in ram]
            ra_list = [t.result() for t in tasks if t.result()[0]]
        with ThreadPoolExecutor(MAX_WORKERS) as ex:
            for url, name in ra_list:
                ex.submit(download_file, url, name)

    # Rename downloaded .ra files
    print("\nRenaming files...\n")
    for f in Path(WORKING_DIR).glob("*.ra"):
        rename_audio(f)

    # Cleanup .ram files
    for f in Path(WORKING_DIR).glob("*.ram"):
        f.unlink()

    print("\nDone!")

if __name__ == "__main__":
    main()