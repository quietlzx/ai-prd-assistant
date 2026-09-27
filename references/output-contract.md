# Output Contract

## Markdown

Produce one complete Markdown document that includes:

- run metadata
- revision history
- Brief and validation summaries
- full PRD
- quantitative targets
- AI risk list
- human review record
- centralized pending-decision appendix
- required disclaimers

## HTML

Produce one self-contained HTML file:

- inline CSS
- no external scripts, styles, fonts, or network resources
- escaped user and document content
- stable heading anchors and numbering
- printable layout
- responsive layout for mobile and desktop
- complete risk table and pending-decision appendix
- no hidden or removable disclaimer

## Consistency Checks

The Markdown and HTML outputs must agree on:

- `run_id`
- product and PRD versions
- Gate status
- `review_state`
- risk IDs
- pending-decision IDs
- disclaimer text

Report assembly must stop if these values differ.
