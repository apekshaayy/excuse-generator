# LOL: Your Excuse Generator

A side project I built because typing out a believable excuse under pressure is genuinely hard, so I made an app do it for me.

## The idea

You tell it where you are, where you're supposed to be, and what you're bailing on (school, college, meetup, date). It looks at what's actually happening around you right now — the weather, the traffic on your route — and writes an excuse that sounds like it's actually true, because most of it is.

You also get to pick how panicked it should sound, from a mild "so sorry, running late" to full meltdown mode.

## What's under the hood

This was mainly an excuse (pun intended) to practice a few things I wanted to get better at:

- **Working with AI APIs** — Gemini writes the actual excuse text, tuned by a distress-level slider that shifts its tone.
- **Maps integration** — real geocoding and live driving directions between two points, not made-up numbers.
- **Prompt engineering** — the excuse doesn't sound generic because it isn't; real numbers (exact temperature, exact delay in minutes, real distance) get fed straight into the prompt, so the output sounds specific instead of templated.
- **Building a context-aware app** — the whole point was that the output changes based on real, live external data instead of being hardcoded or random.

## Known limitations (a.k.a. things I ran into)

- Geocoding sometimes gets a little too literal — typing just "Pashan" resolved to Pashan Lake instead of the general area, so vague place names can throw off the route. Being specific (e.g. "NCL, Pashan, Pune") works much better.
- Weather is pulled from the exact coordinates of your location, so very rural or oddly-named spots might not resolve cleanly.
- Free-tier API limits mean this isn't built for heavy/rapid-fire use — it's a for-fun tool, not a real alibi generator (please don't actually skip class because of this).

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```
Actually just click the link under the About section. Don't hassle with pips and py and whatnots. 
