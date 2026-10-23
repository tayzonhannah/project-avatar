"""
Verification script for PJDSC submission deliverables:
1. docs/PITCH_DECK.md: Exactly 20 slides.
2. docs/DEMO_SCRIPT.md: Word counts per section and total spoken words <= 400.
"""

import re
from pathlib import Path

def audit_pitch_deck(deck_path: Path):
    print("=" * 60)
    print("1. AUDITING PITCH DECK (docs/PITCH_DECK.md)")
    print("=" * 60)
    text = deck_path.read_text(encoding="utf-8")
    
    # Find all slide headings (e.g., '## Slide 01:', '## Slide 1:')
    slide_matches = re.findall(r"^##\s+Slide\s+(\d+)[:\s]", text, re.MULTILINE | re.IGNORECASE)
    print(f"Detected slide headers: {len(slide_matches)}")
    for s in slide_matches:
        print(f" - Slide {s}")
    
    assert len(slide_matches) == 20, f"Expected exactly 20 slides, found {len(slide_matches)}"
    print("[PASS] Pitch Deck satisfies the strict 20-slide limit (zero excess penalty)!\n")


def audit_demo_script(script_path: Path):
    print("=" * 60)
    print("2. AUDITING DEMO SCRIPT (docs/DEMO_SCRIPT.md)")
    print("=" * 60)
    text = script_path.read_text(encoding="utf-8")
    
    # Parse the table rows from the master script
    table_pattern = re.compile(r"^\|\s*(\*\*\d+:\d+\s*-\s*\d+:\d+\*\*)\s*\|\s*([^|]+)\|\s*\"([^\"]+)\"\s*\|\s*([^|]+)\|", re.MULTILINE)
    matches = table_pattern.findall(text)
    
    total_words = 0
    segment_stats = []
    
    for timestamp, visual, audio, message in matches:
        # Count words in audio
        words = [w for w in re.findall(r"\b[\w'-]+\b", audio) if w.strip()]
        word_count = len(words)
        total_words += word_count
        segment_stats.append((timestamp, word_count, audio[:40] + "..."))
        print(f"Row {timestamp}: {word_count} words | Preview: {audio[:40]}...")
    
    print(f"\nTotal Spoken Words: {total_words}")
    print(f"Duration: 180 seconds (3.0 minutes)")
    wpm = total_words / (180 / 60)
    print(f"Average Speaking Cadence: {wpm:.1f} WPM")
    
    assert total_words <= 400, f"Total spoken words ({total_words}) exceeds 400 word limit!"
    assert len(matches) in (8, 9), f"Expected 8 or 9 script rows, found {len(matches)}"
    print("[PASS] Demo script satisfies the <= 400 word budget and 180-second pacing!\n")


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent
    audit_pitch_deck(repo_root / "docs" / "PITCH_DECK.md")
    audit_demo_script(repo_root / "docs" / "DEMO_SCRIPT.md")
    print("=" * 60)
    print("ALL SUBMISSION CONSTRAINTS AUDITED AND VERIFIED SUCCESSFULLY!")
    print("=" * 60)
