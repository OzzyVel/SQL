#!/usr/bin/env python3
"""Generate images via the free tier of the Gemini API
(gemini-2.5-flash-image, codenamed "Nano Banana").

Stdlib-only -- no pip install needed.

Usage:
    python3 generate_image.py "a cozy reading nook, watercolor style"
    python3 generate_image.py "product hero shot, studio lighting" --count 3
    python3 generate_image.py "..." --model gemini-2.5-flash-image --out outputs/gemini-images

Requires GEMINI_API_KEY in the environment or in a .env file in the
current directory (GEMINI_API_KEY=your_key_here). Get a free key at
https://aistudio.google.com/apikey -- no credit card required.
"""
import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
DEFAULT_MODEL = "gemini-2.5-flash-image"


def load_dotenv(path=".env"):
    """Minimal .env loader -- avoids a python-dotenv dependency."""
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip("'").strip('"')
            os.environ.setdefault(key, value)


def generate_one(prompt, model, api_key, out_dir, index):
    url = f"{API_BASE}/{model}:generateContent"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        hint = ""
        if e.code == 429:
            hint = (
                "\nThis looks like a free-tier rate limit. Check your current "
                "quota at https://aistudio.google.com/apikey or "
                "https://ai.google.dev/gemini-api/docs/pricing."
            )
        raise SystemExit(f"Gemini API error {e.code}: {body}{hint}")
    except urllib.error.URLError as e:
        raise SystemExit(f"Network error calling Gemini API: {e}")

    candidates = data.get("candidates", [])
    if not candidates:
        raise SystemExit(f"No candidates returned. Full response: {json.dumps(data)[:800]}")

    parts = candidates[0].get("content", {}).get("parts", [])
    saved = []
    img_n = 0
    for part in parts:
        inline = part.get("inlineData") or part.get("inline_data")
        if not inline:
            continue
        img_n += 1
        mime = inline.get("mimeType") or inline.get("mime_type") or "image/png"
        ext = "png" if "png" in mime else "jpg"
        raw = base64.b64decode(inline["data"])
        out_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        fname = out_dir / f"gemini-{ts}-{index}-{img_n}.{ext}"
        fname.write_bytes(raw)
        saved.append(str(fname))

    if not saved:
        text = "".join(p.get("text", "") for p in parts)
        raise SystemExit(
            "Model responded with text instead of an image (often means the "
            f"prompt was refused or needs rephrasing): {text[:500]}"
        )
    return saved


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prompt", help="Text description of the image to generate")
    ap.add_argument("--model", default=os.environ.get("GEMINI_IMAGE_MODEL", DEFAULT_MODEL))
    ap.add_argument("--out", default="outputs/gemini-images", help="Output directory")
    ap.add_argument("--count", type=int, default=1, help="Number of variations to generate")
    args = ap.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        sys.exit(
            "GEMINI_API_KEY not set. Get a free key (no credit card) at "
            "https://aistudio.google.com/apikey and save it in .env as:\n"
            "  GEMINI_API_KEY=your_key_here"
        )

    out_dir = Path(args.out)
    all_saved = []
    for i in range(1, args.count + 1):
        saved = generate_one(args.prompt, args.model, api_key, out_dir, i)
        all_saved.extend(saved)
        for path in saved:
            print(f"Saved: {path}")

    print(f"\nDone -- {len(all_saved)} image(s) saved to {out_dir}/")


if __name__ == "__main__":
    main()
