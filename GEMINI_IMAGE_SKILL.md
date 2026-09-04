# Free image generation (Gemini) — installed skill

Adds `gemini-image-gen`, a Claude Code skill that generates images through
Google's Gemini API free tier (`gemini-2.5-flash-image`, "Nano Banana"). Free
to set up (no credit card for the API key); the free *usage* tier has a
daily rate limit rather than a spend cap.

Unrelated to the SQL portfolio in this repo — added on request as a free
alternative after the paid Arcads pack was installed and then removed.

## First-time setup

1. Get a free key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey).
2. Copy `.env.example` to `.env` and paste the key into `GEMINI_API_KEY`.
   `.env` is gitignored — it stays local.
3. Ask Claude Code to generate an image, e.g. "Generate an image of a cozy
   reading nook, watercolor style."

## What's installed

- `skills/gemini-image-gen/SKILL.md` — canonical source (workflow, setup,
  free-tier caveats).
- `skills/gemini-image-gen/scripts/generate_image.py` — stdlib-only Python
  script that calls the API and saves the image locally.
- `.claude/skills/gemini-image-gen/` — the copy Claude Code actually reads
  (kept in sync with `skills/gemini-image-gen/`; re-copy manually after
  editing the canonical source since there's no sync hook installed).

## Known caveat

The ~500 images/day free-tier number quoted in the skill docs comes from
third-party sources, not verified directly against Google's own docs
(`ai.google.dev` wasn't reachable when this was set up). Check
[ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing)
for the current limit.
