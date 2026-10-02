# Diagrams and Interactive Pages

## Diagrams

Pick a form that directly expresses the structure of the problem. Never draw for decoration.

| Content | Preferred form |
|---|---|
| Taxonomy and hierarchy | Tree diagram, structure diagram |
| Operations, branching, state transitions | Flowchart, state diagram |
| System interactions and message order | Architecture diagram, sequence diagram |
| Comparing attributes or options | Comparison table, comparison matrix |
| Differences in magnitude | Bar chart |
| Continuous numeric trends | Line chart |
| Correlation and distribution | Scatter plot, distribution plot |
| Spatial layout and part relationships | Annotated schematic |
| Changes across key stages | Step-by-step diagram, before/after comparison |

- Flows, relationships, and architecture: use declarative diagramming such as Mermaid. Quantitative charts: HTML/CSS/JS with a charting library, following the host's output rules.
- One diagram, one point. Labels must be legible. Data charts must show units, categories, and necessary data ranges.
- When precise formulas or lots of text are needed, use charts with controlled layout; do not hand all the text to an image generator.
- Give every diagram one line of "what to look at here". Never make the user hunt for the point.
- No real data, no "trend". Simulated data for teaching must be labeled.

## Interactive pages

Build a page only when interaction genuinely helps understanding.

| Item | Requirement |
|---|---|
| Delivery | A single-file HTML that opens directly, or a runnable artifact the host supports |
| Dependencies | Inline CSS, JS, and SVG preferred. Offline artifacts must not secretly depend on CDNs, remote fonts, or online APIs |
| Core interaction | Sliders, toggles, dragging, step switching, or parameter inputs built around the main difficulty |
| Feedback | Results update immediately after each action, and the user can see why the result changed |
| Initial state | Default parameters already demonstrate the key pattern — not a blank state |
| Recoverable | Provide reset. Time animations need pause and step controls |
| Accessibility | Keyboard operable, clear labels, sufficient contrast, respects "reduce motion" preference |
| Correctness | Distinguish real computation, simplified models, and visual illustration; mark important assumptions |
| Self-contained | The page itself carries a one-line conclusion and usage hint; readable without external text |

A "beautiful layout" with no interaction benefit is not an explanation page. If the environment supports rendering or testing, check key interactions, boundary inputs, and mobile layout; never claim you tested what you didn't.
