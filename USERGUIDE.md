# AI Trends Tracker — User Guide

## Overview

AI Trends Tracker lets you research what people are saying about any topic across Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News, and Polymarket — all in one report. You pick the topic and how far back to look (up to 90 days).

---

## First-Time Setup

### 1. Install dependencies

**yt-dlp** (YouTube research, free):
```bash
brew install yt-dlp
```

**last30days-skill** (the research engine):
```bash
git clone https://github.com/mvanhorn/last30days-skill.git ~/.claude/skills/last30days
```

**Streamlit** (the web UI):
```bash
pip3 install streamlit --break-system-packages
```

### 2. Launch the app

```bash
./run.sh
```

This opens the app at [http://localhost:8501](http://localhost:8501).

### 3. Add your API keys

Open the sidebar and expand **Configure keys**. You only need the keys for the platforms you want to research.

| Platform | Key needed | Where to get it |
|----------|-----------|-----------------|
| Reddit | OpenAI API Key | [platform.openai.com](https://platform.openai.com) |
| X/Twitter | xAI API Key (optional) | [x.ai/api](https://x.ai/api) |
| X/Twitter (alternative) | Auth Token + CT0 from browser cookies | See below |
| TikTok | ScrapeCreators API Key | [scrapecreators.com](https://scrapecreators.com) |
| Instagram | ScrapeCreators API Key | same as TikTok |
| Web search | Brave Search API Key | [brave.com/search/api](https://brave.com/search/api) |
| YouTube | None | Uses yt-dlp, fully free |
| Hacker News | None | Uses Algolia API, fully free |
| Polymarket | None | Uses Gamma API, fully free |

Click **Save Keys** — they are stored in `~/.config/last30days/.env` with permissions set to owner-only (chmod 600).

---

## Getting X/Twitter cookies (alternative to xAI key)

If you don't have an xAI API key, the app can read X authentication directly from your browser cookies.

1. Log in to [x.com](https://x.com) in Chrome or Safari
2. Run the app — it will auto-detect the cookies
3. On first run, macOS will show a keychain prompt asking for your **Mac login password** — this is normal. Click **Always Allow**

---

## Running a Report

### Step 1 — Enter your topic

Type any topic in the search bar. Be as specific or broad as you like:

- `Claude MCP servers`
- `AI video generation tools`
- `open source LLM fine-tuning`
- `GPT-4o use cases in healthcare`

### Step 2 — Set the time window

Use the **Look back (days)** slider to set how far back to search (1–90 days). The default is 30 days.

### Step 3 — Choose research depth

| Mode | Time | Posts per source |
|------|------|-----------------|
| Quick | ~2 min | 8–12 |
| Default | ~5 min | 20–30 |
| Deep | ~8 min | 50–70 |

### Step 4 — Select sources

Toggle platforms on/off. Sources with a green dot in the sidebar are active (configured or free). Sources with a red dot need an API key.

### Step 5 — Run

Click **Run Report**. Output streams live as each platform is queried in parallel. When complete, a **Download Report** button appears to save the report as a Markdown file.

---

## Understanding the Report

The report is structured as Markdown with sections for each platform, followed by a synthesis. Key things to look for:

- **Engagement numbers** — upvotes, view counts, comment counts shown per post
- **Cross-platform tags** — `[also on: Reddit, HN]` means the same story appeared on multiple sources
- **Polymarket odds** — real-money prediction market probabilities on related topics
- **Top voices** — handles and subreddits most active on the topic

---

## Troubleshooting

**No Reddit results**
Add your OpenAI API key in the sidebar. Reddit research uses the OpenAI Responses API.

**No X/Twitter results**
Either add an xAI API key, or log into x.com in Chrome and re-run (the app reads browser cookies). On the first run macOS will prompt for your login keychain password — this is expected, click Allow.

**Script not found error**
Make sure the skill is cloned: `git clone https://github.com/mvanhorn/last30days-skill.git ~/.claude/skills/last30days`

**TikTok / Instagram empty**
These require a ScrapeCreators API key. The free tier includes 100 credits.

**yt-dlp not found**
Run `brew install yt-dlp` then restart the app.

**Research times out**
Try switching to **Quick** mode, or reduce the number of selected sources.

---

## Re-launching

After the first setup, just run:
```bash
./run.sh
```

Or directly:
```bash
python3 -m streamlit run app.py
```
