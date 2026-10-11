# RxRevive-agent

**Drug repositioning research workspace**

RxRevive-agent helps researchers explore new therapeutic hypotheses for existing compounds. It combines a human-reviewed research plan with biomedical literature search, disease-specific knowledge graphs, compound property predictions, analysis of uploaded files, and a traceable final report. It is a research support tool; its outputs require expert review.

## What it can do

- Propose a multi-step workflow and pause for review before longer tasks.
- Search biomedical literature and protocol documents, then build disease-focused knowledge graphs from supported public sources.
- Run available ADMET predictions and analyze uploaded tables with generated figures.
- Keep task conversations, plans, and artifacts in the local persistence directory.
- Reuse saved plans when the user enables that option.

## Run locally

Requirements: Python 3.11-3.13 and an API key for the configured language model provider.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Add your provider key to .env
python main.py
```

Open http://localhost:7860. Set `LOCAL_CONSTRAINED_MODE=true` in `.env` for the resource-limited local profile described in [CONSTRAINED_MODE.md](CONSTRAINED_MODE.md).

For container deployment, use `docker compose up --build`. Persistent data stays under `persistence/`.

## Project map

- `app/` - interface, conversations, run lifecycle, downloads
- `core/` - agent graph, prompts, and tools
- `backend/` - database, document retrieval, execution support, and data clients
- `persistence/` - local conversations, uploads, indexes, and results
- `models/` - included predictive model artifacts
- `docs/` - operating and technical guides

## Project lineage and acknowledgments

RxRevive-agent is a customized fork of [Repuragent](https://github.com/pharmbio/repuragent), the open-source drug-repurposing agent project. The workflow and scientific capabilities build on that project; this rebrand does not claim the upstream work as original. See [acknowledgments](docs/acknowledgement.md) for scientific tools, datasets, and protocol sources, and preserve applicable upstream license terms when redistributing this code.

The upstream project describes its research in this preprint:

```bibtex
@article{huynh2026,
  title   = {Human-supervised Agentic AI for Hypothesis Generation and Experimental Assistance in Drug Repurposing},
  author  = {Huynh, Dinh Long and Asp, Elin and Ballante, Flavio and Carreras Puigvert, Jordi and DeGrave, Alisa and Karki, Reagon and Nader, Kristen and Ostling, Paivi and Pokharel, Bishab and Rietdijk, Jonne and Schlotawa, Lars and Schmidt, Lina and Seal, Srijit and Seashore-Ludlow, Brinton and Aittokallio, Tero and Spjuth, Ola},
  journal = {bioRxiv},
  year    = {2026},
  doi     = {10.64898/2026.04.20.719538},
  url     = {https://www.biorxiv.org/content/10.64898/2026.04.20.719538v2}
}
```
