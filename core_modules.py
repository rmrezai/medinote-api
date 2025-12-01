def call_opencds(labs):
    return [{
        "summary": "Hyperkalemia",
        "detail": "Recommend checking creatinine before starting ACEi.",
        "suggestions": [{"label": "Order BMP"}, {"label": "Hold lisinopril"}]
    }]

class MediNoteCDSWrapper:
    def __init__(self, labs, vitals=None, meds=None):
        self.labs = labs or {}
        self.vitals = vitals or {}
        self.meds = meds or []

    def enrich_cdscard(self, card):
        summary = card.get("summary", "")
        detail = card.get("detail", "")
        suggestions = card.get("suggestions", [])
        enriched = [f"- {detail}"]
        if "hyperkalemia" in summary.lower():
            if self.labs.get("Cr", 0) > 1.5:
                enriched.append("- Elevated Cr suggests renal impairment.")
            if any("lisinopril" in m.lower() for m in self.meds):
                enriched.append("- Lisinopril present — consider holding.")
        for s in suggestions:
            enriched.append(f"- Suggestion: {s.get('label')}")
        return f"3. {summary}\n" + "\n".join(enriched)

    def enrich_all(self, cards):
        return [self.enrich_cdscard(c) for c in cards]

def medinote_ap_handler(payload):
    labs = payload.get("labs", {})
    vitals = payload.get("vitals", {})
    meds = payload.get("meds", [])
    cds_cards = call_opencds(labs)
    wrapper = MediNoteCDSWrapper(labs, vitals, meds)
    enriched_aps = wrapper.enrich_all(cds_cards)
    return {"ap_entries": enriched_aps}
