---
version: "1.0"
updated: 2026-11-03
status: draft
---

# Content Sources and Casting Methods

## Classical sources {#1}

Bundled Classics.json contains the 64 hexagrams, judgments, line texts, Tuan, Xiang and line images, compiled from [meihua classical data](https://github.com/toastedqu/meihua/blob/main/app/data/classics.json). The retrieval date is 2026-09-19. Individual entries retain Wikisource links and revision IDs, such as 2404991 for Qian. Only public-domain classical text is included, not third-party modern commentary. Rights in modern editions, translations, images and layouts must be considered separately. Attribution does not imply endorsement.

## Reflection and daily reading {#2}

Modern prompts support learning and reflection; they are not complete line-by-line translations or AI chat. Ink imagery is illustrative, not historical evidence. Daily reading uses the device calendar day ordinal and cycles through 64 hexagrams with index (day ordinal − 1) modulo 64. It is neither random casting nor a personal prediction.

## Coin method {#3}

Each line simulates three coins: heads scores 3 and tails 2. Totals 6, 7, 8 and 9 mean old yin, young yang, young yin and old yang. Generate six lines from bottom to top; 6 and 9 change polarity in the resulting hexagram. With independent fair simulated coins, theoretical probabilities are 1/8, 3/8, 3/8 and 1/8. This is a simulation, not physical tossing.

## Number method {#4}

Enter three positive integers from 1 to 1,000,000. If all fields are blank, three random numbers from 1 to 999 are generated. The first modulo 8 selects the upper trigram, the second modulo 8 the lower, and the third modulo 6 the moving line. A zero remainder means 8 or 6. Trigram order is Qian, Dui, Li, Zhen, Xun, Kan, Gen, Kun. Lines are numbered 1–6 from bottom to top.

## Time and calendar {#5}

Let S be the lunar year earthly-branch number (Zi=1 to Hai=12) plus lunar month number (a leap month uses the same number) plus lunar day. S modulo 8 selects the upper trigram. Add the double-hour branch number (Zi=1 to Hai=12) to form T; T modulo 8 selects the lower trigram and T modulo 6 the moving line. Zero remainders follow the same rule. Zi spans 23:00–01:00, but the date changes at 00:00. Device local time and the chosen time zone apply, including system daylight-saving rules; there is no true-solar-time correction. The lunar year changes on lunar New Year, not Start of Spring. Lunar months are not solar-term month pillars.

## Snapshots and limits {#6}

Snapshots store inputs, date, time zone, six line values and algorithm version (currently 1). Traditions may differ. Content supports cultural learning and reflection, not certain predictions or medical, psychological, investment or legal advice. Report source, character, algorithm or translation issues to [apw_service@163.com](mailto:apw_service@163.com).
