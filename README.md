# NSFW AI Model Detection Pipeline
**Undergraduate Research — RAND Lab, UC Santa Cruz**
*Advisor: Professor Ram Sundara Raman*

## Overview
This repository contains a metadata scraping and risk-scoring pipeline built as part of ongoing research into AI platform safety and non-consensual intimate imagery (NCII). The pipeline connects to Hugging Face's public API, collects model metadata and full model card descriptions, scores them across six weighted detection categories, and outputs structured JSON results for analysis.

This work extends a spring quarter project that involved manually analyzing NSFW model pages on CivitAI and building a standalone HTML-based detection tool. This quarter the goal was to automate that process at scale.

## Files
- `test_huggingface.py` — initial API scraper pulling model metadata (names, tags, downloads, descriptions)
- `hf_pipeline.py` — full pipeline combining API scraping + automated risk scoring + JSON output
- `scan_results_20260901_1610.json` — sample output from scanning 15 models across 3 search queries

## Detection Categories
The scoring system flags model pages across 6 weighted categories:

| Category | Weight | Example Terms |
|---|---|---|
| Explicit content signals | 4x | nsfw, nude, uncensored |
| Euphemistic framing | 3x | all-purpose, all possibilities |
| Legal distancing | 2x | exempt, right to sell |
| Bypass/capability signals | 2x | lora, no trigger needed |
| Suspicious tags | 1x | nsfw, adult, anime |

Each model receives a risk score from 0–100.

## Key Findings
- 15 models analyzed across 3 search queries ("uncensored," "nsfw," "lora realistic")
- Multi-category clustering is a stronger signal than single keyword hits
- Identified false positive problem: "uncensored" flagged unrelated chatbot models
- Safety tools (e.g. Falconsai/nsfw_image_detection) scored similarly to suspicious models — showing context matters beyond keywords

## Next Steps
- Expand to CivitAI scraping pipeline
- Set up cron job for continuous automated monitoring
- Move toward embedding-based similarity scoring to catch euphemistic evasions

## Research Context
This project is related to lab research on AI-enabled NSFW services on mainstream platforms. See: *"From Underground to Mainstream Marketplaces: Measuring AI-Enabled NSFW Deepfakes on Fiverr"* — Dawoud, Cuevas, Raman (USEC 2026).
