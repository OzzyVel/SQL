---
name: gemini-image-gen
description: Generate images for free using the Gemini API's free tier (gemini-2.5-flash-image, "Nano Banana"). Use when the user asks to create, generate, or make an image, picture, graphic, or illustration and wants a free / no-cost option, or explicitly mentions Gemini, Nano Banana, or Google AI Studio for image generation.
---

# Gemini free-tier image generation

Generates images via Google's Gemini API using a **free** Google AI Studio
API key — no credit card required to obtain the key. This is genuinely free
to set up; the free *usage* tier has a daily rate limit (see below) rather
than a spend cap.

## Setup (one-time)

1. Get a free API key at **https://aistudio.google.com/apikey** (Google
   account only, no credit card).
2. Copy `.env.example` to `.env` in the repo root (if not already done) and
   paste the key in:
   ```
   GEMINI_API_KEY=your_key_here
   ```
   `.env` is gitignored — never commit it, never paste the key in chat.

## Generating an image

```bash
python3 skills/gemini-image-gen/scripts/generate_image.py "your prompt here"
```

Options:
- `--count N` — generate N variations (default 1). Each is a separate API
  call and counts separately against the daily free quota.
- `--out DIR` — output directory (default `outputs/gemini-images/`).
- `--model NAME` — override the model (default `gemini-2.5-flash-image`).

The script is stdlib-only Python (no `pip install` needed) and saves each
generated image locally, printing the saved path(s).

## Free-tier limits (confirm current numbers yourself)

Multiple third-party sources report the free tier as roughly **500
images/day at 1024×1024** for `gemini-2.5-flash-image`, but this was **not**
verified against Google's own docs (their domains aren't reachable from
this environment) and free-tier limits change. **Check
https://ai.google.dev/gemini-api/docs/pricing** for the current numbers
before relying on a specific quota. If a generation call fails with a `429`
error, that's the rate limit — the script will tell you and point at the
same page.

## Workflow

1. Ensure `.env` has `GEMINI_API_KEY` (see Setup). If missing, tell the user
   how to get one — do not ask them to paste the key in chat unless they
   insist; if they do, write it to `.env` and confirm without repeating it.
2. Write one clear, specific prompt (style, subject, composition, mood —
   avoid keyword-soup). For marketing/ad-style images, describe the exact
   scene, lighting, and any on-image text explicitly (Gemini can render
   text in-image but short, simple text works best).
3. Ask how many variations the user wants (default 1) — each is a separate
   billed-against-quota call.
4. Run `scripts/generate_image.py` with the prompt.
5. **Inspect the output** for defects (distorted faces/hands, garbled
   requested text, artifacts). If something looks wrong, regenerate with a
   revised prompt that explicitly corrects the issue. Cap at 2 retries per
   originally requested image.
6. Show the user the saved file path(s) (use `SendUserFile` — or the
   equivalent in whatever harness this is running in — to actually surface
   the image, not just the path as text).

## Notes

- No presigned uploads, no reference-image asset pipeline, no project
  folders — this is a much thinner tool than a paid creative platform. It's
  best for quick single images, not multi-step ad campaigns (storyboards,
  video, character consistency across many shots).
- The API can also accept an input image (for edits / image-to-image) via
  an additional `inlineData` part in the request — not implemented in
  `generate_image.py` yet since the initial ask was text-to-image. Extend
  the script if that's needed.
