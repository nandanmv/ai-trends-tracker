# AI Trends Tracker

A Streamlit app that generates trend reports for any topic across Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News, and Polymarket — for a time period you choose.

Built on top of [last30days-skill](https://github.com/mvanhorn/last30days-skill) and [yt-dlp](https://github.com/yt-dlp/yt-dlp).

![Python](https://img.shields.io/badge/python-3.10+-blue) ![Streamlit](https://img.shields.io/badge/streamlit-1.5+-red)

## What it does

Enter a topic (e.g. *"Claude MCP servers"*, *"AI video generation"*, *"vibe coding"*) and get a structured report showing:

- Most popular posts and threads per platform
- Engagement metrics (upvotes, views, likes, comment counts)
- Brief summaries of what the community is saying
- Cross-platform convergence (same story trending on multiple sources)
- Polymarket prediction odds on related topics

## Quick Start

```bash
git clone https://github.com/nandanmv/ai-trends-tracker.git
cd ai-trends-tracker

# Install the last30days-skill
git clone https://github.com/mvanhorn/last30days-skill.git ~/.claude/skills/last30days

# Install yt-dlp (macOS)
brew install yt-dlp

# Install dependencies
pip3 install streamlit --break-system-packages

# Launch
./run.sh
```

Open [http://localhost:8501](http://localhost:8501).

## API Keys

Configure in the sidebar when the app is running. Keys are saved to `~/.config/last30days/.env` (chmod 600).

| Key | Source | Required? |
|-----|--------|-----------|
| OpenAI API Key | Reddit research | Yes (for Reddit) |
| xAI API Key | X/Twitter fallback | Optional |
| X Auth Token + CT0 | X/Twitter via cookies | Optional (auto-read from Chrome/Safari) |
| ScrapeCreators API Key | TikTok + Instagram | Optional |
| Brave Search API Key | Web search | Optional |

**Free sources** (no key needed): YouTube (yt-dlp), Hacker News (Algolia), Polymarket (Gamma API).

## Usage

1. Enter your topic in the search bar
2. Set the lookback window (1–30 days)
3. Choose research depth: Quick (~2 min) / Default (~5 min) / Deep (~8 min)
4. Toggle which platforms to include
5. Click **Run Report**
6. Download the report as Markdown

## File Structure

```
ai-trends-tracker/
├── app.py        # Streamlit UI
├── run.sh        # Launch script
├── README.md
└── USERGUIDE.md
```

The research engine lives in `~/.claude/skills/last30days/` (installed separately).

## Requirements

- Python 3.10+
- [streamlit](https://streamlit.io) (`pip3 install streamlit`)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) (`brew install yt-dlp`)
- [last30days-skill](https://github.com/mvanhorn/last30days-skill) (cloned to `~/.claude/skills/last30days`)

## Note on X/Twitter on Mac

When first running, macOS may prompt for your login keychain password so the app can read Chrome cookies for X authentication. Click **Always Allow**.
