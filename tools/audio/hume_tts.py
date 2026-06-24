"""
Hume Octave TTS — IPAI Character Voices

The first TTS system built on LLM intelligence. Understands emotional context
and adapts delivery (pitch, tempo, emphasis) to match each word's intent.

IPAI Characters:
  - Nigel Thistledown (gardener/nature guide)
  - Claire Delish (chef/nutrition coach)
  - Olly Bennett (fitness coach)
  - VV Steele (style/fashion advisor)
  - Pennie Power (financial coach)
  - Roxie Rush (narrator/host)
"""

import os
import httpx
from pathlib import Path
from tools.base_tool import BaseTool, ToolResult, ToolRuntime, ToolStability, ToolTier, ToolStatus


HUME_API_KEY = os.getenv("HUME_API_KEY", "")

# IPAI Character Voice Registry
IPAI_VOICES = {
    "nigel_thistledown": {
        "id": "3bfd1fc0-a7d2-49ed-8325-4a28891f55ad",
        "name": "Nigel Thistledown",
        "description": "Gentle gardener & nature guide. Warm, patient, slightly British.",
        "best_for": ["nature", "gardening", "relaxation", "educational"],
    },
    "claire_delish": {
        "id": "09eccfe9-8068-42c3-8f0a-e91f5d50d160",
        "name": "Claire Delish",
        "description": "Warm chef & nutrition coach. Enthusiastic about food, encouraging.",
        "best_for": ["cooking", "nutrition", "health", "recipes"],
    },
    "olly_bennett": {
        "id": "de25054e-a18d-41d7-93f3-d9fb6fb63078",
        "name": "Olly Bennett",
        "description": "Energetic fitness coach. Motivating, upbeat, action-oriented.",
        "best_for": ["fitness", "sports", "motivation", "health"],
    },
    "vv_steele": {
        "id": "d513161a-3be9-4eaa-9612-711f77268b63",
        "name": "VV Steele",
        "description": "Stylish fashion advisor. Confident, trendy, opinionated.",
        "best_for": ["fashion", "style", "culture", "entertainment"],
    },
    "pennie_power": {
        "id": "240fb214-35c0-4c46-ad08-ac16fe48499b",
        "name": "Pennie Power",
        "description": "Sharp financial coach. Clear, direct, no-nonsense.",
        "best_for": ["finance", "business", "investing", "economics"],
    },
    "roxie_rush": {
        "id": "33e57cc2-1727-465b-ab0f-8ac4bca82e9b",
        "name": "Roxie Rush",
        "description": "Dynamic narrator. Dramatic timing, engaging, versatile.",
        "best_for": ["narration", "storytelling", "news", "general"],
    },
}


class HumeTTS(BaseTool):
    """Hume Octave TTS with IPAI character voices."""

    name = "hume_tts"
    version = "1.0.0"
    tier = ToolTier.VOICE
    capability = "tts"
    provider = "hume"
    stability = ToolStability.PRODUCTION

    dependencies = []
    install_instructions = (
        "Set HUME_API_KEY in .env\n"
        "Get one at https://platform.hume.ai"
    )

    agent_skills = [".agents/skills/tts/hume-octave.md"]

    capabilities = [
        "text_to_speech",
        "character_voices",
        "emotional_delivery",
        "voice_design",
    ]

    input_schema = {
        "type": "object",
        "required": ["text", "output_path"],
        "properties": {
            "text": {"type": "string", "description": "Text to speak"},
            "output_path": {"type": "string", "description": "Where to save the audio file"},
            "voice": {
                "type": "string",
                "description": "Voice ID or IPAI character slug (e.g. 'nigel_thistledown')",
                "default": "roxie_rush",
            },
            "speed": {
                "type": "number",
                "description": "Speech speed multiplier",
                "default": 1.0,
            },
        },
    }

    def check_available(self) -> bool:
        return bool(HUME_API_KEY)

    def get_status_reason(self) -> str:
        if not HUME_API_KEY:
            return "HUME_API_KEY not set"
        return ""

    async def execute(self, text: str, output_path: str, voice: str = "roxie_rush", speed: float = 1.0) -> dict:
        """Generate speech using Hume Octave TTS."""
        if not HUME_API_KEY:
            raise RuntimeError("HUME_API_KEY not configured")

        # Resolve IPAI character slug to voice ID
        voice_id = voice
        voice_name = voice
        if voice in IPAI_VOICES:
            voice_id = IPAI_VOICES[voice]["id"]
            voice_name = IPAI_VOICES[voice]["name"]

        # Build request
        payload = {
            "utterances": [
                {
                    "text": text,
                    "voice": {"id": voice_id},
                    "speed": speed,
                }
            ],
            "format": {"type": "mp3"},
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                "https://api.hume.ai/v0/tts/file",
                headers={
                    "X-Hume-Api-Key": HUME_API_KEY,
                    "Content-Type": "application/json",
                },
                json=payload,
            )

        if response.status_code != 200:
            raise RuntimeError(f"Hume TTS failed ({response.status_code}): {response.text[:200]}")

        # Write audio file
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(response.content)

        return {
            "output_path": str(out),
            "voice": voice_name,
            "voice_id": voice_id,
            "size_bytes": len(response.content),
            "provider": "hume_octave",
        }

    def get_info(self) -> dict:
        return {
            "name": self.name,
            "provider": "Hume AI (Octave)",
            "voices": {k: v["name"] for k, v in IPAI_VOICES.items()},
            "capabilities": self.capabilities,
            "available": self.check_available(),
        }
