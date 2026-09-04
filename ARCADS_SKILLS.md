# Arcads AI Video — installed skills

This repo includes the [Arcads AI Video skill pack](https://github.com/krusemediallc/arcads-claude-code)
for Claude Code, installed on `2026-09-04`. It's unrelated to the SQL portfolio
in this repo — it was added on request to make the Arcads creative-generation
skills available in this workspace.

## What's installed

Six ready-to-use Claude Code skills live under `.claude/skills/`:

| Skill | What it does |
|---|---|
| `arcads-external-api` | Core skill — Arcads API reference, video-model prompting (Seedance 2.0, Sora 2, Veo 3.1, Kling 3.0, Grok Video, OmniHuman), analyze-video / clone-ad workflows. |
| `chatgpt-image-ad` | Static Meta image-ad creatives via gpt-image-2 (typography / UI-mimicry templates). |
| `nano-banana-image-ad` | Static Meta image-ad creatives via Nano Banana 2/Pro/Edit (photoreal / lifestyle templates). |
| `image-ad-clone` | Reverse-engineers an existing ad image into a reusable template entry. |
| `generate-youtube-thumbnail` | 5 CTR-tested YouTube thumbnail formulas. |
| `meta-ad-builder` | Publishes a finished creative as a **paused** Meta ad via the Meta Marketing API. |

Their canonical source (and supporting prompt libraries / guides referenced by
the skills above) lives under `skills/` and `shared/skills/` — that's where to
edit if you customize a skill; re-run `./scripts/sync-skill.sh` afterward to
refresh the copies under `.claude/skills/`.

## Not installed

This is a **skills-only** install. Deliberately left out, because they change
session behavior repo-wide rather than just adding on-demand skills:

- The upstream root `CLAUDE.md` (auto-loaded Arcads session rules).
- The `.claude/settings.json` `SessionStart` hook (auto skill-sync + banner on every session).
- The `.cursor/` integration.
- The original repo's sample reference photos and API call log (119 MB of
  demo AI-influencer images + another user's usage log) — not relevant here.

## First-time setup (only needed if you actually use these skills)

1. Copy `.env.example` to `.env` and fill in your Arcads API key
   (`app.arcads.ai/settings/api`). `.env` is gitignored.
2. Optionally copy `MASTER_CONTEXT.template.md` to `MASTER_CONTEXT.md` for
   persistent workspace context (default product, credit costs, brand voice).
   Also gitignored.
3. Drop reference images into `references/influencers/`, `references/products/`,
   or `references/aesthetics/` as needed — that folder is gitignored too.
4. Ask Claude Code to use a skill, e.g. "Generate a UGC selfie of [product]"
   or "Make me a Forbes editorial-style image ad."

See `AGENTS.md` for a fuller walkthrough (written for any AI coding assistant,
not just Claude Code).
