"""
AI Trends Tracker
Streamlit app that wraps the last30days-skill to research topics across
Reddit, X, YouTube, TikTok, Instagram, Hacker News, and Polymarket.
"""

import os
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

import streamlit as st

# ── Paths ───────────────────────────────────────────────────────────────────
SKILL_DIR = Path.home() / ".claude" / "skills" / "last30days" / "scripts"
SCRIPT = SKILL_DIR / "last30days.py"
CONFIG_DIR = Path.home() / ".config" / "last30days"
ENV_FILE = CONFIG_DIR / ".env"

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Trends Tracker",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .block-container { padding-top: 1.5rem; }
  h1 { font-size: 1.8rem !important; }
  .stTextInput > label { font-weight: 600; }
  .report-container {
    background: #0e1117;
    border: 1px solid #2d2d2d;
    border-radius: 8px;
    padding: 1.5rem;
    font-family: 'SF Mono', monospace;
    font-size: 0.85rem;
    white-space: pre-wrap;
    overflow-x: auto;
  }
  .source-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    margin: 2px;
  }
  .status-ok   { color: #22c55e; }
  .status-miss { color: #ef4444; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────────────────
def load_env() -> dict:
    """Load saved API keys from ~/.config/last30days/.env"""
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()
    return env


def save_env(keys: dict):
    """Persist API keys to ~/.config/last30days/.env"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    lines = []
    for k, v in keys.items():
        if v:
            lines.append(f"{k}={v}")
    ENV_FILE.write_text("\n".join(lines) + "\n")
    ENV_FILE.chmod(0o600)


def build_env(keys: dict) -> dict:
    """Build subprocess environment with current API keys."""
    env = os.environ.copy()
    for k, v in keys.items():
        if v:
            env[k] = v
    # Point yt-dlp to the installed binary
    env["PATH"] = "/opt/homebrew/bin:" + env.get("PATH", "")
    return env


def build_cmd(topic: str, days: int, depth: str, sources: list[str]) -> list[str]:
    """Build the last30days.py CLI command."""
    cmd = [sys.executable, str(SCRIPT), topic, f"--days={days}", "--emit=md"]
    if depth == "Quick":
        cmd.append("--quick")
    elif depth == "Deep":
        cmd.append("--deep")
    if sources:
        cmd.append(f"--search={','.join(sources)}")
    return cmd


def parse_source_status(output: str) -> dict:
    """Parse which sources returned results from the markdown output."""
    status = {}
    source_map = {
        "reddit": "Reddit", "x": "X/Twitter", "youtube": "YouTube",
        "tiktok": "TikTok", "instagram": "Instagram",
        "hackernews": "Hacker News", "polymarket": "Polymarket",
    }
    for key, label in source_map.items():
        has_data = bool(re.search(rf'(^#{1,3}\s+{label}|{label}.*\d+|\b{key}\b)', output, re.IGNORECASE | re.MULTILINE))
        status[label] = has_data
    return status


# ── Sidebar: API Keys ─────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📡 AI Trends")
    st.caption("Powered by [last30days-skill](https://github.com/mvanhorn/last30days-skill) + yt-dlp")
    st.divider()

    st.subheader("API Keys")
    saved = load_env()

    with st.expander("Configure keys", expanded=not saved.get("OPENAI_API_KEY")):
        openai_key = st.text_input(
            "OpenAI API Key", value=saved.get("OPENAI_API_KEY", ""),
            type="password", help="Required for Reddit research"
        )
        xai_key = st.text_input(
            "xAI API Key", value=saved.get("XAI_API_KEY", ""),
            type="password", help="X/Twitter fallback (optional — browser cookies work too)"
        )
        auth_token = st.text_input(
            "X Auth Token", value=saved.get("AUTH_TOKEN", ""),
            type="password", help="From x.com cookies (optional)"
        )
        ct0 = st.text_input(
            "X CT0 Token", value=saved.get("CT0", ""),
            type="password", help="From x.com cookies (optional)"
        )
        scrape_key = st.text_input(
            "ScrapeCreators API Key", value=saved.get("SCRAPECREATORS_API_KEY", ""),
            type="password", help="Required for TikTok + Instagram"
        )
        brave_key = st.text_input(
            "Brave Search API Key", value=saved.get("BRAVE_API_KEY", ""),
            type="password", help="Optional web search"
        )

        if st.button("Save Keys", type="primary", use_container_width=True):
            save_env({
                "OPENAI_API_KEY": openai_key,
                "XAI_API_KEY": xai_key,
                "AUTH_TOKEN": auth_token,
                "CT0": ct0,
                "SCRAPECREATORS_API_KEY": scrape_key,
                "BRAVE_API_KEY": brave_key,
            })
            st.success("Keys saved!")
            st.rerun()

    st.divider()

    # Source availability indicators
    st.subheader("Source Status")
    has_openai = bool(saved.get("OPENAI_API_KEY") or openai_key)
    has_x = bool(saved.get("XAI_API_KEY") or xai_key or saved.get("AUTH_TOKEN") or auth_token)
    has_scrape = bool(saved.get("SCRAPECREATORS_API_KEY") or scrape_key)

    def dot(ok): return "🟢" if ok else "🔴"

    st.markdown(f"""
{dot(has_openai)} Reddit *(OpenAI key)*
{dot(has_x)} X/Twitter *(xAI key or browser cookies)*
🟢 YouTube *(yt-dlp, free)*
{dot(has_scrape)} TikTok *(ScrapeCreators)*
{dot(has_scrape)} Instagram *(ScrapeCreators)*
🟢 Hacker News *(Algolia, free)*
🟢 Polymarket *(Gamma API, free)*
""")


# ── Main UI ──────────────────────────────────────────────────────────────────
st.title("AI Trends Tracker")
st.caption("Get a report of the most popular posts, demos, and use cases for any topic across social platforms.")

# Search form
with st.form("search_form"):
    topic = st.text_input(
        "Topic to research",
        placeholder="e.g. Claude MCP servers, AI video generation, vibe coding",
        label_visibility="collapsed",
    )

    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        days = st.slider("Look back (days)", min_value=1, max_value=30, value=30, step=1)

    with col2:
        depth = st.radio(
            "Research depth",
            ["Quick", "Default", "Deep"],
            index=1,
            horizontal=True,
            help="Quick: ~2 min | Default: ~5 min | Deep: ~8 min",
        )

    with col3:
        submitted = st.form_submit_button(
            "Run Report", type="primary", use_container_width=True
        )

    # Source toggles
    st.markdown("**Sources**")
    src_cols = st.columns(7)
    source_map = {
        "reddit": "Reddit",
        "youtube": "YouTube",
        "hn": "HN",
        "polymarket": "Polymarket",
        "x": "X",
        "tiktok": "TikTok",
        "instagram": "Instagram",
    }
    selected_sources = []
    for i, (key, label) in enumerate(source_map.items()):
        with src_cols[i]:
            if st.checkbox(label, value=True, key=f"src_{key}"):
                selected_sources.append(key)


# ── Run ───────────────────────────────────────────────────────────────────────
if submitted:
    if not topic.strip():
        st.warning("Please enter a topic to research.")
        st.stop()

    if not SCRIPT.exists():
        st.error(f"last30days script not found at `{SCRIPT}`. Check that the skill is installed.")
        st.stop()

    if not selected_sources:
        st.warning("Select at least one source.")
        st.stop()

    # Reload saved keys in case they were updated
    saved = load_env()
    env_vars = build_env({
        "OPENAI_API_KEY": saved.get("OPENAI_API_KEY", ""),
        "XAI_API_KEY": saved.get("XAI_API_KEY", ""),
        "AUTH_TOKEN": saved.get("AUTH_TOKEN", ""),
        "CT0": saved.get("CT0", ""),
        "SCRAPECREATORS_API_KEY": saved.get("SCRAPECREATORS_API_KEY", ""),
        "BRAVE_API_KEY": saved.get("BRAVE_API_KEY", ""),
    })

    cmd = build_cmd(topic.strip(), days, depth, selected_sources)

    st.divider()
    date_from = (date.today() - timedelta(days=days)).strftime("%b %d")
    date_to = date.today().strftime("%b %d, %Y")
    st.markdown(f"### Report: **{topic}** &nbsp;&nbsp; `{date_from} – {date_to}`")

    depth_label = {"Quick": "~2 min", "Default": "~5 min", "Deep": "~8 min"}[depth]
    status_placeholder = st.empty()
    status_placeholder.info(f"Researching across {len(selected_sources)} sources ({depth_label})...")

    progress_bar = st.progress(0, text="Starting research...")

    output_placeholder = st.empty()
    error_placeholder = st.empty()

    # Stream output
    stdout_lines: list[str] = []

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env_vars,
            cwd=str(SKILL_DIR),
            text=True,
            bufsize=1,
        )

        # Read stdout line by line and update display
        source_progress = {s: False for s in selected_sources}
        done_count = 0

        stdout_pipe = proc.stdout
        stderr_pipe = proc.stderr
        if stdout_pipe and stderr_pipe:
            for line in iter(stdout_pipe.readline, ""):
                stdout_lines.append(line)
                combined = "".join(stdout_lines)

                # Detect source completions from output
                for src in list(source_progress.keys()):
                    if not source_progress[src]:
                        if re.search(rf'\b{src}\b', combined, re.IGNORECASE):
                            source_progress[src] = True
                            done_count = sum(source_progress.values())
                            pct = int((done_count / len(selected_sources)) * 90)
                            progress_bar.progress(
                                pct,
                                text=f"Fetching... {done_count}/{len(selected_sources)} sources"
                            )

                # Show live output
                output_placeholder.markdown(combined)

            stdout_pipe.close()
            stderr_output = stderr_pipe.read()
        else:
            stderr_output = ""
        proc.wait()

        progress_bar.progress(100, text="Complete!")
        status_placeholder.empty()

        final_output = "".join(stdout_lines)

        if proc.returncode != 0 and not final_output.strip():
            error_placeholder.error(
                f"Script exited with code {proc.returncode}.\n\n**stderr:**\n```\n{stderr_output[:2000]}\n```"
            )
        else:
            if stderr_output and proc.returncode != 0:
                with st.expander("Warnings/Errors"):
                    st.code(stderr_output[:3000], language="text")

            # Final formatted display
            output_placeholder.empty()
            progress_bar.empty()

            st.markdown(final_output)

            # Download button
            st.download_button(
                label="Download Report (Markdown)",
                data=final_output,
                file_name=f"trends_{topic.replace(' ', '_')}_{date.today()}.md",
                mime="text/markdown",
            )

    except FileNotFoundError:
        status_placeholder.error(f"Python not found at `{sys.executable}`")
    except Exception as e:
        status_placeholder.error(f"Unexpected error: {e}")
