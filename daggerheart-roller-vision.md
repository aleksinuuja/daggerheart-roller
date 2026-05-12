# Daggerheart Roller — Vision Document

## What This Is

A single-page Progressive Web App (PWA) for rolling Daggerheart dice during solo simulation sessions. Installable on mobile and desktop via browser. No backend. No login. No cost to host (deploy to GitHub Pages).

---

## Core Mechanic (Daggerheart Rules)

Daggerheart uses a **2d12 dual-dice system** called the Duality Dice.

- Roll **1d12 Hope** (gold die) and **1d12 Fear** (black die) simultaneously  
- Add a **trait modifier** (the relevant character trait, can be negative)  
- Compare the **total** against a **Difficulty** set by the GM  
- The higher individual die determines whether the result carries **Hope** or **Fear**

### Outcome Logic

```
total = Hope_die + Fear_die + modifier

if Hope_die == Fear_die:
  outcome = "Critical Success"
  # Automatically succeeds regardless of Difficulty
  # Player gains a Hope, clears a Stress, and deals critical damage on attack rolls
  # A Critical Success counts as rolling "with Hope"

elif total >= difficulty:
  if Hope_die > Fear_die:  outcome = "Success with Hope"   # player gains a Hope
  else:                    outcome = "Success with Fear"   # GM gains a Fear

else:  # total < difficulty
  if Hope_die > Fear_die:  outcome = "Failure with Hope"   # minor consequence, player gains a Hope
  else:                    outcome = "Failure with Fear"   # major consequence, GM gains a Fear
```

There is no "tie" outcome other than Critical Success. Matching Duality Dice always produce a Critical Success, overriding the Difficulty comparison entirely.

### Advantage / Disadvantage

Advantage and disadvantage use a **d6**, not an extra d12. They modify the total, not the dice pool composition.

- **Advantage**: Roll an additional **d6**, add the result to the total  
- **Disadvantage**: Roll an additional **d6**, subtract the result from the total  
- Multiple advantage/disadvantage dice cancel each other one-for-one; you never roll both simultaneously  
- When a player helps an ally (Help an Ally), they roll their own advantage d6 and the acting player adds the highest result — multiple helpers can each roll but only the single highest result is added  
- Advantage and disadvantage dice do not affect the Hope/Fear die comparison; only the two d12s determine Hope or Fear

---

## Inputs

| Field | Type | Notes |
| :---- | :---- | :---- |
| Modifier | Integer (can be negative) | Trait modifier added to total. Defaults to 0 |
| Advantage/Disadvantage | \+/- stepper | Number of d6 advantage dice (positive) or disadvantage dice (negative). Defaults to 0\. They cancel out; the net value is what gets rolled |
| Difficulty | Integer | Set by GM. Defaults to 12 |

---

## Output

### Visual display

- Show the Hope die result and Fear die result prominently  
- Show the total: `Hope + Fear + modifier = total vs difficulty N`  
- Show the outcome label clearly: **"Critical Success\!"**, **"Success with Hope"**, **"Success with Fear"**, **"Failure with Hope"**, **"Failure with Fear"**  
- Critical Success should be visually distinct (matching dice is a special event)  
- If advantage/disadvantage dice were rolled, show their individual results and the net modifier applied

### Copyable text string

A single-line summary for pasting into LLM-driven simulators. Auto-generated after every roll. One-tap copy button.

Format:

```
Rolled Hope [X] / Fear [Y] +[modifier] vs difficulty [D]. [Outcome].
```

Examples:

```
Rolled Hope 3 / Fear 11 +3 vs difficulty 14. Success with Fear.
Rolled Hope 7 / Fear 4 +0 vs difficulty 10. Success with Hope.
Rolled Hope 2 / Fear 6 -1 vs difficulty 12. Failure with Fear.
Rolled Hope 8 / Fear 8 +2 vs difficulty 15. Critical Success!
Rolled Hope 1 / Fear 9 +0 vs difficulty 12. Failure with Fear.
```

If advantage/disadvantage dice were used, append their net result in parentheses:

```
Rolled Hope 8 / Fear 5 +2 vs difficulty 12. Success with Hope. (Advantage d6: +4)
Rolled Hope 3 / Fear 9 +1 vs difficulty 14. Failure with Fear. (Disadvantage d6: -3)
```

If modifier is 0 and no advantage, omit the modifier from the string:

```
Rolled Hope 7 / Fear 4 vs difficulty 10. Success with Hope.
```

---

## UX Principles

- **Mobile-first**: The primary use case is a phone on the table during a session. Large tap targets. No tiny inputs.  
- **One-handed operable**: Roll button should be thumb-reachable at screen bottom  
- **Instant**: No loading states, no confirmations. Roll → result appears immediately  
- **Copy is prominent**: The copyable string should be visually separated and the copy button should be obvious — this is the main output for simulator use  
- **Persistent inputs**: Bonus, advantage, and difficulty should remember their last values across sessions (localStorage)  
- **Works offline**: Full PWA with service worker. Once loaded, works with no connection

---

## Aesthetic Direction

Dark, tactile, slightly arcane. Think worn leather and candlelight, not glass-and-chrome. The dual Hope/Fear dice should feel like two opposing forces. Avoid generic fantasy kitsch.

- Dark background (near-black, warm-toned, not cold)  
- The Hope die: gold or amber accent  
- The Fear die: silver or cool-grey accent  
- Outcome text: large, confident, readable at a glance  
- Typography: a distinctive serif or slab-serif for outcome labels; clean readable font for numbers and inputs

---

## PWA Requirements

- `manifest.json` with name, short\_name, icons, theme\_color, display: standalone  
- Service worker with cache-first strategy for offline use  
- `apple-mobile-web-app-capable` meta tags for iOS home screen install  
- Single HTML file \+ manifest \+ service worker (no build step required)  
- Deploy target: GitHub Pages (static, no server)

---

## File Structure

```
/
├── index.html        # App shell + all JS + inline or linked CSS
├── manifest.json     # PWA manifest
├── sw.js             # Service worker
└── icons/            # App icons (192x192, 512x512 minimum)
```

---

## Out of Scope

- Roll history log (could be added later)  
- Character sheet integration  
- Multiplayer / shared sessions  
- Any backend or user accounts

