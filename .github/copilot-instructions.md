# Copilot Instructions for AST250 Stellar Populations Project

## Project Overview
This is an educational research project exploring stellar populations and the initial mass function (IMF) as part of UC Berkeley's AST250 course. A core focus is investigating how generative AI can be integrated into scientific workflows. The project combines Jupyter notebooks for computational work with research documentation.

## Key Project Areas

### Stellar Populations & IMF Research
- **Domain**: Astrophysics - studying star formation histories and the Initial Mass Function (IMF)
- **Key papers** referenced in README: Conroy (2013), Walcher+ (2011), Tolstoy+ (2009), Gallart+ (2005)
- **Core problem**: Understanding stellar populations through spectral energy distribution (SED) fitting and color-magnitude diagrams
- **IMF work**: [Stellar_IMF_exercise_Jan22/exercise.ipynb](Stellar_IMF_exercise_Jan22/exercise.ipynb) contains practical exercises on IMF sampling

### AI in Science Methodology
- **Research focus**: Documenting how AI tools (Claude, Gemini, ChatGPT) integrate into scientific workflows
- **Context**: Tracking decisions, challenges, and outcomes in [research_notebook.md](research_notebook.md)
- **Key insight from notebook**: When using AI, conversational threading (multi-turn context) works better than isolated prompts; AI is most helpful when given the full research context

## Critical Developer Workflows

### Working with Jupyter Notebooks
- Primary computational environment: Jupyter notebooks (`.ipynb` files)
- Extension setup: The project uses Markdown All in One and Markdown Preview Enhanced for documentation
- **Workflow pattern**: Notebooks are used for exercises and computational exploration; results documented in the research notebook

### Research Documentation
- Research progress tracked in [research_notebook.md](research_notebook.md) as a living document
- Structure: Dated entries documenting experiments, tool setup, and discoveries
- Keep detailed context about *why* decisions were made, not just *what* was tried

### Common Development Tasks
1. **Running exercises**: Use Jupyter notebooks for interactive computation
2. **Literature review**: Reference papers in [01_jan20_2026/](01_jan20_2026/) and [02_jan22_2026/](02_jan22_2026/) directories
3. **Documentation**: Update research_notebook.md with findings and methodology
4. **Model fitting**: Project relies on MCMC and astropy.modeling (see README references)

## Project-Specific Conventions

### Documentation Style
- Use markdown for all text documentation
- Include dated entries for research progress with clear context
- Reference specific papers/resources by name and link when discussing domain concepts
- Explain the "why" behind experimental choices for future readers (human and AI)

### File Organization
- PDFs and course materials in date-stamped folders
- Jupyter notebooks in subdirectories organized by exercise/topic
- Research tracking in root-level markdown files
- Images directory for screenshots/figures

### Dependencies & Tools
- **Python environment**: Astropy (modeling), MCMC libraries
- **Documentation**: Markdown + VS Code extensions (Markdown All in One, Markdown Preview Enhanced)
- **AI integration**: GitHub Copilot (via Berkeley @astro.berkeley.edu email), Gemini, Claude
- **Constraint**: GitHub Copilot requires Berkeley astro email setup (contact EECS/department admin)

## AI Agent Guidance

When assisting with this project:
1. **Understand the domain first**: Read referenced astrophysics papers to grasp stellar population concepts
2. **Respect the research workflow**: Treat research_notebook.md as the source of truth for project state; update it when significant decisions are made
3. **Jupyter-first approach**: Notebooks are primary computational environment; prioritize clean, documented code cells
4. **Context matters**: When generating code or analysis, provide full context about assumptions and data sources (mirrors the conversational threading principle discovered in the research)
5. **Reference existing patterns**: The exercise notebook shows the expected structure for IMF/population modeling work
