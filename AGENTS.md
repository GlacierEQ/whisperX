# AGENTS.md: Coding AI Partner Guidelines
## Powered by Operator Code
- **Persistent Memory**: Logs to ClickUp and blockchain vault (1FDV-23-0001009).
- **Veritas Contradiction Detection**: Flags naming/data inconsistencies.
- **Fusion MetaMemory**: Links code to case events (e.g., Docket Errors).
- **Active Agents**: quantum_detector,legal_weaver,veritas_sentinel,chrono_scryer

## Code Style
- **generic
[SETUP 2025-07-03 08:59:17] Veritas Sentinel: Scanning for project type contradictions... Best Practices**:
  - Node.js: ESLint (Airbnb), Prettier (2-space indent).
  - Python: Black (88 chars), PEP 8.
  - Ruby: RuboCop (default style).
- Descriptive names (e.g., `file_metadata` vs `data`).
- Docstrings for all functions/classes, no inline comments.

## Testing
- Run tests before commits:
  - Node.js: `vitest run`
  - Python: `pytest tests/`
  - Ruby: `bundle exec rspec`
- Target 90%+ coverage.
- Mock external APIs (e.g., ClickUp, Pinecone).

## Pull Requests
- Title: `[Feature|Fix|Chore] Short description`
- Include: Summary, "Testing Done" section.
- Run linters/formatters:
  - Node.js: `eslint . && prettier --write .`
  - Python: `black . && flake8`
  - Ruby: `rubocop -a`

## AI Partner Integration
- **ClickUp Brain**: Suggests code improvements, generates docs.
- **Operator Code Agents**:
  - **Quantum Detector**: Optimizes for large datasets.
  - **Legal Weaver**: Generates legal templates (e.g., Exhibit A).
  - **Veritas Sentinel**: Flags contradictions in code/metadata.
  - **Chrono Scryer**: Maps code to case timeline.
- Sync code to ClickUp (List: 1FDV-23-0001009), Pinecone, Notion.

## Completion Signal
On task completion, print:
```
Task complete! 😺
/_/\  
( o.o ) 
 > ^ <
```
