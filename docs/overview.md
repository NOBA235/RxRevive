# Overview

RxRevive-agent is a researcher-supervised workspace for exploring drug repositioning hypotheses. A planning agent can propose a workflow for review; research, prediction, and data agents then gather evidence, run supported analyses, and prepare a report.

## Capabilities

- **Planning and oversight:** break a research question into steps and review a plan before longer runs.
- **Evidence gathering:** search biomedical literature and protocol documents, resolve disease identifiers, and build disease-focused knowledge graphs from supported public sources.
- **Predictive modeling:** run the included CPSign ADMET models for supported compound properties.
- **Data analysis:** inspect uploaded files, combine and rank candidate tables, calculate statistics, and generate figures.
- **Traceable work:** retain plans, conversations, and generated files in the local persistence directory.
- **Reusable planning:** optionally save successful plans as precedent for later tasks.

## Local deployment

The application runs locally and stores conversations and artifacts under `persistence/`. Requests to language-model and data providers use the credentials and services configured for the installation. See [Local setup](local.md) for installation instructions.

## Project lineage

RxRevive-agent is a customized fork of [Repuragent](https://github.com/pharmbio/repuragent). The upstream project and scientific resources are credited in [Acknowledgments](acknowledgement.md).
