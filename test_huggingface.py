from huggingface_hub import HfApi, ModelCard
import json
from datetime import datetime

hf_api = HfApi()

# ── DETECTION CATEGORIES (same logic as your HTML analyzer tool) ──────────────
CATEGORIES = [
    {
        "name": "Explicit content signals",
        "weight": 4,
        "terms": ["nsfw", "adult content", "explicit", "uncensored", "18+",
                  "erotic", "nude", "nudity", "naked", "lewd", "hentai", "porn"]
    },
    {
        "name": "Euphemistic framing",
        "weight": 3,
        "terms": ["all-purpose", "greater variety", "all possibilities",
                  "no restrictions", "unlimited", "unrestricted",
                  "anything goes", "you can more"]
    },
    {
        "name": "Legal distancing",
        "weight": 2,
        "terms": ["exempt", "not responsible", "sole responsibility",
                  "declare myself exempt", "violations resulting",
                  "right to sell", "creator is responsible"]
    },
    {
        "name": "Bypass/capability signals",
        "weight": 2,
        "terms": ["lora", "fine-tuned", "no trigger needed", "prompt adherence",
                  "realistic girls", "ethnic training", "merge model",
                  "training with nsfw", "nsfw conducted"]
    },
    {
        "name": "Suspicious tags",
        "weight": 1,
        "terms": ["nsfw", "adult", "uncensored", "explicit", "anime",
                  "stable-diffusion", "lora", "realistic"]
    },
]

def score_text(text):
    """Score a block of text using the analyzer categories. Returns score 0-100."""
    if not text:
        return 0, []

    text_lower = text.lower()
    total_weight = 0
    flagged = []

    for cat in CATEGORIES:
        hits = [t for t in cat["terms"] if t in text_lower]
        if hits:
            total_weight += len(hits) * cat["weight"]
            flagged.append({
                "category": cat["name"],
                "hits": hits,
                "points": len(hits) * cat["weight"]
            })

    score = min(round((total_weight / 30) * 100), 100)
    return score, flagged


def risk_label(score):
    if score < 20:   return "LOW"
    if score < 45:   return "MODERATE"
    if score < 70:   return "ELEVATED"
    return "HIGH"


# ── SEARCH TERMS — these target the suspicious side of HuggingFace ───────────
SEARCH_QUERIES = [
    "uncensored",
    "nsfw",
    "lora realistic",
]

print("=" * 65)
print("  HUGGING FACE → ANALYZER PIPELINE  |  Platform Safety Research")
print(f"  Run at: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 65)

results = []

for query in SEARCH_QUERIES:
    print(f"\n>>> SEARCHING: '{query}'")
    print("-" * 65)

    models = hf_api.list_models(
        search=query,
        sort="downloads",
        limit=5
    )

    for model in models:
        # Build text to analyze: combine tags + description
        tag_text = " ".join(model.tags) if model.tags else ""

        try:
            card = ModelCard.load(model.id)
            description = card.text[:1000]
        except Exception:
            description = ""

        full_text = tag_text + " " + description
        score, flagged = score_text(full_text)
        label = risk_label(score)

        # Print result
        print(f"\n  MODEL:     {model.id}")
        print(f"  DOWNLOADS: {model.downloads:,}" if model.downloads else "  DOWNLOADS: N/A")
        print(f"  RISK:      {score}/100 — {label}")

        if flagged:
            for f in flagged:
                print(f"  [{f['category']}] → {f['hits']} ({f['points']} pts)")

        # Save to results list
        results.append({
            "query": query,
            "model_id": model.id,
            "downloads": model.downloads,
            "likes": model.likes,
            "tags": model.tags,
            "risk_score": score,
            "risk_label": label,
            "flagged_categories": flagged,
            "description_preview": description[:300]
        })

# ── SAVE RESULTS TO JSON (this is your research data) ────────────────────────
output_file = f"scan_results_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
with open(output_file, "w") as f:
    json.dump(results, f, indent=2)

print("\n" + "=" * 65)
print(f"  SCAN COMPLETE — {len(results)} models analyzed")
print(f"  HIGH risk:     {sum(1 for r in results if r['risk_label'] == 'HIGH')}")
print(f"  ELEVATED risk: {sum(1 for r in results if r['risk_label'] == 'ELEVATED')}")
print(f"  MODERATE risk: {sum(1 for r in results if r['risk_label'] == 'MODERATE')}")
print(f"  LOW risk:      {sum(1 for r in results if r['risk_label'] == 'LOW')}")
print(f"\n  Results saved to: {output_file}")
print("=" * 65)