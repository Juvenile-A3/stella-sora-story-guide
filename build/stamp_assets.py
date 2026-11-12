"""Version local entry-page dependencies and media by content before publishing."""
import hashlib
from pathlib import Path
import re

SITE = Path(__file__).resolve().parents[1]
LOCAL_ASSET = re.compile(r'(?P<quote>["\'])(?P<path>[\w./%-]+\.(?:js|css|mp4|mp3|srt|jpg|png|webp|txt))(?:\?v=[\w.-]+)?(?P=quote)')


def stamp(entry, hashes):
    def version(match):
        asset = SITE / match["path"]
        if not asset.is_file() or SITE not in asset.resolve().parents:
            return match[0]
        if asset not in hashes:
            hashes[asset] = hashlib.sha256(asset.read_bytes()).hexdigest()[:12]
        return f'{match["quote"]}{match["path"]}?v={hashes[asset]}{match["quote"]}'

    original = entry.read_bytes().decode("utf-8")
    updated = LOCAL_ASSET.sub(version, original)
    if updated != original:
        entry.write_bytes(updated.encode("utf-8"))


if __name__ == "__main__":
    digests = {}
    for filename in ("index.html", "intro.html"):
        stamp(SITE / filename, digests)
