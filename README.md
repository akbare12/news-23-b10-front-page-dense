[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b10-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b10-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# THE WORLD TODAY — Monday 23 November 2026

One image summing up the world's news of Monday 23 November 2026: a dense
front page with 31 stories across 6 regions.

**The day's three biggest stories**

1. **AI rout hits Asia** — the Kospi falls 3.3% to 4,708.54 (intraday -5.8%),
   Samsung -3.1%, SK Hynix -2.5%, as the AI sell-off spreads from Wall Street.
2. **Guterres: regulate AI before it's too late** — the UN chief urges global
   AI safety rules at the Bridgetown summit; 150 delegates back a risk
   framework, a blueprint rather than a treaty.
3. **US lead over China at a record low** — Asia Power Index 2026: US 78.9,
   China 73.6, a gap of 5.3, the narrowest since 2018.

**Inside:** the day in numbers (-3.3%, 5.3, 11,762 Ebola cases, 10T-won Seoul
fund, $450M Skubal deal, 165 Russian missiles in a week, $107.3B Anthropic
IPO), a UTC timeline, 10 more illustrated cards, a world map with numbered
pins, an "Also on Monday" list, and a DATE CHECK box listing what was left
out because it was not 23 November (Democrats reach 258, Sparta II fire,
El Chapo captured — all 22 Nov; EU-Indonesia pact, Nigeria boat — 21 Nov;
ICJ Myanmar ruling — 19 Nov).

Scenes are drawn illustrations, not photographs. Chips mark each story
REPORTED (confirmed by a named source), CLAIM (one side alleges, not
verified) or ONGOING (still developing).

## How it is built

`draw.py` draws the 1024×1024 page with Pillow and saves `entry.png`.
`main.py` (stdlib only) copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
and verifies the copy byte for byte (sha256 + 1024×1024 PNG header check).

Run locally:

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
