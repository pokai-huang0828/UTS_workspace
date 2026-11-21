# Aspect labelling instruction (v2, 2026-11-21)

Changes from v1: three unclear points reported in the 50-review pilot are now spelled out (rules 6, 7, 8).
The aspects, label values and output format are unchanged.

You will read Airbnb guest reviews (English). For EACH review, decide for each of the 7 aspects below
whether the review talks about it, and if so whether the guest was positive, negative, or both.

## Aspects (use exactly these keys)
- cleanliness        : how clean the place was (clean, spotless, dirty, dust, mould, smell, stains, bugs).
- noise              : noise or quietness (street/traffic noise, neighbours, construction, thin walls, "quiet", "peaceful").
- location_transport : the location or neighbourhood; closeness to beach, shops, city, attractions; public transport; walkability.
- checkin            : check-in / check-out and getting in (keys, lockbox, access codes, instructions, early/late check-in, luggage).
- communication      : the host as a person or the host's messages (responsive, helpful, friendly, slow or no reply, rude).
- value              : value for money, price, fees ("worth it", "overpriced", "good value", "expensive").
- amenities_comfort  : things inside the home and comfort (bed, kitchen, wifi, air-con/heating, shower/hot water, space,
                       furniture, appliances, parking, pool, view from the home, "well equipped", "comfortable").

## Label values (use exactly these strings)
- "pos"   : mentioned, only positive
- "neg"   : mentioned, only negative
- "mixed" : mentioned, both positive and negative about the same aspect
- "none"  : not mentioned

## Rules
1. Label only what the review explicitly says. Do not guess.
2. Generic praise with no topic ("great place", "lovely stay", "would recommend", "amazing apartment") is NOT an aspect: all "none".
3. A suggestion or wish ("would be nice to have a fan") counts as "neg" for that aspect.
4. "overall" is the guest's overall feeling for the whole review: "pos", "neg" or "mixed".
5. For every aspect that is not "none", give "evidence": a short quote copied from the review, at most 12 words.
6. Check-in instructions vs the host: clear / unclear check-in or access instructions -> checkin.
   The host being responsive, helpful, friendly (or not) -> communication.
   If one sentence clearly does both ("host sent clear check-in instructions and replied fast"), label both.
7. "overall" is "mixed" when the review contains at least one explicit complaint AND at least one explicit praise.
   It is "neg" only when the guest is clearly unhappy overall. A single small wish inside a happy review -> still "mixed".
8. Cleaning quality (including the cleaner's work) -> cleanliness. "Well maintained", repairs, broken things -> amenities_comfort.
9. Very short reviews are fine: if nothing specific is said, all aspects are "none" and "evidence" is {}.

## Output format
Return ONLY a JSON array with one object per review, in the same order as the input, like this:
[
  {"rid": "R001",
   "labels": {"cleanliness": "pos", "noise": "none", "location_transport": "pos", "checkin": "none",
              "communication": "pos", "value": "none", "amenities_comfort": "neg"},
   "evidence": {"cleanliness": "spotlessly clean", "location_transport": "five minutes walk to the beach",
                "communication": "host replied quickly", "amenities_comfort": "the bed was too soft"},
   "overall": "pos"}
]
No explanations, no markdown fences, nothing before or after the JSON array.
