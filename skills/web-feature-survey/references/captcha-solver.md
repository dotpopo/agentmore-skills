# Slider / Jigsaw Captcha Auto-Solve (AJ-Captcha, battle-tested)

Applies to: anji-plus AJ-Captcha and variants with "decoy outlines" (multiple white puzzle outlines on the background, only one is the real gap).

## Why blind dragging / eyeballing screenshots fails

- Screenshots are scaled (raw background 310×155, displayed 360×155); eyeball error easily exceeds tolerance (±5 raw pixels).
- With decoy outlines, the "best-looking" one is probably fake — on a real project the first true gap had residual 17.1 vs 25.0/36.1 for decoys, visually indistinguishable.

## Algorithm (success rate ~100%)

1. **Extract raw images from the DOM**, not screenshots: two base64 images —
   - background `img.backImg` (e.g. 310×155)
   - puzzle strip `img.bock-backImg` (e.g. 47×155, transparent background containing the puzzle piece)
2. **Puzzle mask**: take the puzzle bbox via alpha>128 (46×46 on the real project), then erode 2–4 px to remove the white border.
3. **Candidate locating**: find white (RGB>215) connected components in the background; candidates are those whose bbox size ≈ puzzle size.
4. **Darkening fit decides the truth**: true-gap pixels ≈ puzzle content × constant k (k via least squares).
   For each candidate compute `mean|bg_region − k·piece|`; smallest residual wins.
   Decoy outlines are just painted strokes unrelated to the piece — clearly larger residual.
5. **Coordinate mapping**:
   - scale = display width / raw width (360/310)
   - strip left = bg.left + gap.x × scale
   - **handle "center follows mouse"**: element left = mouse.x − halfWidth (20 px on the project). Don't forget this!
6. **Human-like drag**: after mouse down, move in 6–8 segments (±1–2 px vertical jitter), overshoot slightly then settle, then mouse up.
7. **Measured mapping**: mid-drag (before release) read the strip position once to confirm the displacement ratio between strip and handle (1:1 on the project), then correct the target accordingly.

## Failure handling

- Failure auto-rotates the image: just re-extract and recompute (script the whole flow; a single retry costs < 10 s).
- Captcha images expire (a few minutes) — drag soon after analysis.
- Some sites wrap the captcha in an iframe / dialog; switch frames accordingly.

## Dependencies

Python: Pillow, numpy. Core idea: connected-component candidates + darkening-fit residual ranking + drag with measured 1:1 mapping.
