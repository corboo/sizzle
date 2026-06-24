# Hume Octave TTS — IPAI Character Voices

## Overview

Hume Octave is the first TTS system built on LLM intelligence. Unlike conventional TTS that applies fixed prosody rules, Octave *understands* the text it speaks — emotionally and semantically. It knows when to whisper secrets, when to shout in triumph, and when to calmly state facts.

## IPAI Character Roster

When using Sizzle/IPAI productions, prefer these character voices over generic TTS. Each has a distinct personality that Octave delivers authentically:

| Character | Slug | Best For |
|-----------|------|----------|
| **Nigel Thistledown** | `nigel_thistledown` | Nature, gardening, relaxation, gentle education |
| **Claire Delish** | `claire_delish` | Cooking, nutrition, recipes, food culture |
| **Olly Bennett** | `olly_bennett` | Fitness, sports, motivation, action |
| **VV Steele** | `vv_steele` | Fashion, style, culture, entertainment |
| **Pennie Power** | `pennie_power` | Finance, business, investing, economics |
| **Roxie Rush** | `roxie_rush` | General narration, storytelling, news, drama |

## Prompting Guidance

### Voice Selection
- Match the character to the content topic. A gardening video should use Nigel. A finance explainer should use Pennie.
- For general/neutral content where no character fits, use **Roxie Rush** — she's the versatile narrator.
- Never use a character voice for content that contradicts their personality (e.g., don't use Nigel for a fast-paced tech demo).

### Text Preparation
- Octave reads punctuation for pacing. Use em-dashes for pauses, ellipses for trailing thoughts.
- Short sentences = punchy delivery. Long flowing sentences = smoother, calmer delivery.
- Octave handles emphasis naturally from context — you rarely need ALL CAPS or special markers.
- For dramatic reveals: put the key word at the end of a sentence after a dash.

### Speed
- Default (1.0) works for most content
- Slow (0.85) for meditative/relaxation content (Nigel nature walks)
- Fast (1.1) for energetic content (Olly fitness, Roxie news)

## Technical Details

- **Model:** Octave 2 (preview)
- **Latency:** ~100ms (not including network)
- **Format:** MP3
- **API:** `POST https://api.hume.ai/v0/tts/file`
- **Auth:** `X-Hume-Api-Key` header
- **Supports:** English, Spanish, Japanese, Korean, French, Portuguese, Italian, German, Russian, Hindi, Arabic
