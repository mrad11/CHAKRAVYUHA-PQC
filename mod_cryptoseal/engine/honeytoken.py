"""
CHAKRAVYUHA PQC: Semantic Honeytoken & Dynamic Context Bait Injection
Ministry of Defence - Problem Statement 237

Inserts imperceptible, context-aware synthetic bait into non-critical text parameters.
Enables instant attribution if an insider re-types classified information on an un-watermarked notepad,
summarizes it on social media, or leaks it verbally over an unencrypted phone line.
"""

import re
from typing import Dict, Any, List, Optional


# Pre-calibrated tactical parameter variations
HONEYTOKEN_DICTIONARY = {
    "T_90_RESERVE_COUNT": {
        "Col. Rajesh Sharma": "48 main battle tanks",
        "Brig. Arvind Verma": "52 main battle tanks",
        "Maj. Priya Nair": "50 main battle tanks"
    },
    "SECURE_RADIO_FREQUENCY": {
        "Col. Rajesh Sharma": "142.85 MHz tactical band",
        "Brig. Arvind Verma": "142.90 MHz tactical band",
        "Maj. Priya Nair": "142.80 MHz tactical band"
    },
    "CONVOY_CALLSIGN": {
        "Col. Rajesh Sharma": "FALCON-EAGLE-ALPHA",
        "Brig. Arvind Verma": "FALCON-EAGLE-BRAVO",
        "Maj. Priya Nair": "FALCON-EAGLE-CHARLIE"
    },
    "FORWARD_DEPOT_GRID": {
        "Col. Rajesh Sharma": "Grid Sector 884-Bravo",
        "Brig. Arvind Verma": "Grid Sector 886-Bravo",
        "Maj. Priya Nair": "Grid Sector 882-Bravo"
    }
}


class SemanticHoneytokenEngine:
    """Manages tactical bait injection and plain-text leak attribution."""

    @classmethod
    def get_officer_honeytokens(cls, officer_name: str) -> Dict[str, str]:
        """Retrieve the designated subtle honeytokens assigned to an officer."""
        tokens = {}
        for param, mapping in HONEYTOKEN_DICTIONARY.items():
            tokens[param] = mapping.get(officer_name, list(mapping.values())[0])
        return tokens

    @classmethod
    def inject_honeytokens_into_text(cls, template_text: str, officer_name: str) -> str:
        """Inject customized honeytoken values into an operational briefing paragraph."""
        tokens = cls.get_officer_honeytokens(officer_name)
        text = template_text
        for param, val in tokens.items():
            placeholder = f"{{{param}}}"
            if placeholder in text:
                text = text.replace(placeholder, val)
        return text

    @classmethod
    def scan_leaked_plaintext(cls, leaked_text: str) -> Dict[str, Any]:
        """
        Scan a leaked text snippet (phone transcript, forum post, telegram message)
        against the active honeytoken registry to pinpoint the leaker.
        """
        text_lower = leaked_text.lower()
        officer_matches = {
            "Col. Rajesh Sharma": 0,
            "Brig. Arvind Verma": 0,
            "Maj. Priya Nair": 0
        }
        identified_tokens = []

        for param, mapping in HONEYTOKEN_DICTIONARY.items():
            for officer, phrase in mapping.items():
                if phrase.lower() in text_lower:
                    officer_matches[officer] += 1
                    identified_tokens.append({
                        "parameter": param,
                        "matched_phrase": phrase,
                        "assigned_to": officer
                    })

        # Find best match
        best_officer = max(officer_matches, key=officer_matches.get)
        match_count = officer_matches[best_officer]

        if match_count > 0:
            confidence = min(99.9, round((match_count / len(HONEYTOKEN_DICTIONARY)) * 100.0, 1))
            return {
                "attribution_found": True,
                "identified_culprit": best_officer,
                "confidence_score": f"{confidence}%",
                "matched_honeytokens": identified_tokens,
                "vector_type": "ANALOG_VOICE_OR_PLAIN_TEXT_LEAK",
                "evidence_status": "HIGH_CONFIDENCE_SEMANTIC_MATCH"
            }
        else:
            return {
                "attribution_found": False,
                "identified_culprit": None,
                "confidence_score": "0%",
                "matched_honeytokens": [],
                "evidence_status": "NO_SEMANTIC_HONEYTOKENS_FOUND"
            }
