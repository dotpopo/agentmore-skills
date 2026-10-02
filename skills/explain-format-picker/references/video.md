# Explainer Videos

Suited to abstract concepts, mechanisms that unfold over time, and content you only understand by watching it change. Style inspired by 3Blue1Brown: intuition first, symbols second; one idea per frame; the continuous change of the frame itself is the argument. Never impersonate the original author, never copy their brand assets, never imitate their voice.

## First establish what you can actually do

Inspect the environment before committing. Do not assume.

- **Visuals**: Manim is the usual choice. Without it, use whatever can generate animation frame by frame — e.g. scripts that draw SVG/Canvas frames, then compose.
- **Voiceover**: prefer built-in TTS. For local setups, use an actually available and licensed local TTS. Only consider an external voice service (e.g. ElevenLabs) when the user explicitly requests it, and never ask for plaintext API keys in the conversation.
- **Subtitles**: provided by default. If embedding fails, deliver an SRT file or a transcript.
- **Compositing**: ffmpeg or an equivalent.

When a key tool is missing, say exactly what is missing, then step down to delivering "script + storyboard + runnable render code" or short captioned clips. Storyboards and scripts are intermediate products, not the final video — never present them as one.

## Parameters

| Item | Default |
|---|---|
| Duration | Simple topics 60–90 s; complex topics 2–3 min; adjust to real capability |
| Aspect | 16:9; 9:16 when explicitly targeting vertical mobile video |
| Language | Match the user's language |
| Structure | Core question → build intuition → dynamic mechanism → key conclusion → applicability limits |

## Production workflow

1. **Write the narration first, not the code.** Narration in STE style: short sentences, one idea per sentence.
2. **Break into shots.** Each shot covers one or two narration lines; write down what appears and how it changes.
3. **Visuals serve the narration.** If the narration says "two quantities grow together", the frame must show two quantities growing together. Highlight whatever is being discussed; no filler material.
4. **Render and inspect.** Spot-check a few frames: text overflow, overlaps, sufficient contrast.
5. **Deliver.** Video file plus a short text summary (core conclusion, key parameters, applicability limits) for later reference.

## Visual principles

- One idea per frame; information appears progressively, never all at once.
- An object keeps the same name, color, and symbol throughout.
- Minimal text; if a shape can say it, don't write it.
- Every change has a purpose — motion, morphing, and highlights must be explaining some relationship.
- After a key transformation or formula appears, leave time to absorb it.
- Dark background, high contrast, large type.
- Math and data must be exact: use controlled rendering and compositing. Never entrust formula correctness to generative imagery.

## When NOT to make a video

- One diagram plus a few sentences already explains it.
- The user is casually asking and shows no willingness to spend minutes watching.
- The content is precise reference material (commands, parameter tables) — video is harder to search.

In these cases deliver text and a diagram first, then offer a video in one sentence.
