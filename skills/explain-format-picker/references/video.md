# Explainer Videos (v2: two tiers)

Style target: 3Blue1Brown — intuition first, symbols second; one idea per frame; the continuous change of the frame itself is the argument. Never impersonate the original author, never copy brand assets, never imitate their voice.

## Tier 0 — video as a page (default)

A video is a diagram that changes on a schedule. Before encoding any MP4, build a **step player page** — the pattern popularized by [answer-me-with-html](https://github.com/QingYunA/answer-me-with-html):

- One self-contained HTML file: the diagram (SVG/Canvas/CSS) plus a player bar (play/pause, prev/next, progress, speed).
- The draft's narration lines become **beats**; each beat reveals or moves one thing in the diagram (a node lights up, an arrow draws, a state flips). The "camera" follows the current beat's node.
- Beats start automatically and advance on a timer; captions show the current line; clicking a chapter jumps to it.
- No ffmpeg, no encoding, works offline, text stays selectable, and every beat is exactly as precise as the draft it came from.
- Voiceover: use the host's TTS if the user asked for sound; otherwise ship captions (default). Captions come from the draft lines — do not re-write them at render time.

This tier satisfies most "explain it as a video" requests. Reply with the page path and one sentence.

## Tier 1 — rendered video (explicit request only)

Build MP4/WebM when the user asks for a **video file** explicitly:

- Inspect the environment before committing: Manim for visuals; ffmpeg (or equivalent) for compositing; a licensed TTS for voice. Missing tools → say what's missing, fall back to Tier 0 plus a storyboard, and call the storyboard a storyboard — never a video.
- Render beats from the same draft; spot-check 1–2 frames for overflow, overlap, contrast.
- Deliver the file + a text summary (core conclusion, key parameters, applicability limits).

## Draft rules (both tiers)

- Structure: core question → intuition → dynamic mechanism → key conclusion → applicability limits.
- One beat = one or two narration lines; each beat changes exactly one thing; the picture serves the narration ("two quantities grow together" ⇒ two quantities grow together).
- Duration by beat count, not ambition: 8–15 beats for a short topic; 16:9 (9:16 only for phone-first).
- An object keeps the same name, color, symbol throughout; text minimal; every change explains a relationship; after a key transformation, pause.
- Math and data must be exact — controlled rendering, never generative imagery. Label simulated data `illustrative`.

## When NOT to make a video

- One diagram plus a few sentences already explains it.
- The user is casually asking and shows no willingness to spend minutes watching.
- The content is precise reference material (commands, parameter tables) — video is harder to search.

In these cases deliver text and a diagram first, then offer a video in one sentence.
