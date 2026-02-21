import streamlit as st
from groq import Groq
import json

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FakeGuard · News Verifier",
    page_icon="🔍",
    layout="centered",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0d0d0d;
    color: #f0ece0;
}
.stApp { background: #0d0d0d; }
h1, h2, h3 { font-family: 'Syne', sans-serif; font-weight: 800; }
.hero-title {
    font-size: 3.2rem; font-weight: 800; letter-spacing: -0.03em; line-height: 1.1;
    background: linear-gradient(135deg, #f0ece0 40%, #c8ff00 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.3rem;
}
.hero-sub {
    font-family: 'IBM Plex Mono', monospace; color: #888; font-size: 0.85rem;
    letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 2.5rem;
}
.verdict-box { border-radius: 12px; padding: 2rem; margin-top: 1.5rem; border: 1.5px solid; }
.verdict-real { background: #0a1f0a; border-color: #4cff72; color: #c8ffd4; }
.verdict-fake { background: #1f0a0a; border-color: #ff4c4c; color: #ffd4d4; }
.verdict-uncertain { background: #1a1700; border-color: #ffd200; color: #fff3b0; }
.verdict-label { font-size: 2rem; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 0.3rem; }
.confidence-bar-wrap { background: #222; border-radius: 99px; height: 8px; margin: 1rem 0; overflow: hidden; }
.confidence-bar { height: 8px; border-radius: 99px; }
.mono { font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem; color: #aaa; }
.section-label {
    font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem;
    letter-spacing: 0.12em; text-transform: uppercase; color: #666; margin-bottom: 0.4rem;
}
.stTextArea textarea {
    background: #181818 !important; color: #f0ece0 !important;
    border: 1.5px solid #333 !important; border-radius: 10px !important;
    font-family: 'IBM Plex Mono', monospace !important; font-size: 0.88rem !important;
}
.stButton > button {
    background: #c8ff00; color: #0d0d0d; font-family: 'Syne', sans-serif;
    font-weight: 700; font-size: 1rem; border: none; border-radius: 8px;
    padding: 0.7rem 2.5rem; width: 100%;
}
.divider { border: none; border-top: 1px solid #222; margin: 2rem 0; }
.flag-chip {
    display: inline-block; background: #1e1e1e; border: 1px solid #333;
    border-radius: 6px; padding: 0.25rem 0.6rem;
    font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem; color: #aaa;
    margin: 0.2rem 0.2rem 0 0;
}
.sources-box {
    background: #131313; border-radius: 10px; padding: 1rem 1.2rem;
    border: 1px solid #222; font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem; color: #999; margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero-title">FakeGuard</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">AI-powered news credibility analyzer · Powered by Groq (Free)</div>', unsafe_allow_html=True)

st.markdown('<div class="section-label">Paste article or headline</div>', unsafe_allow_html=True)
news_text = st.text_area(
    label="", placeholder="Paste a news article, headline, or claim here...",
    height=200, label_visibility="collapsed",
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_btn = st.button("🔍 Analyze Now", use_container_width=True)

SYSTEM_PROMPT = """You are an expert fact-checker and media literacy analyst. Analyze the given news article or claim for credibility.

Respond ONLY with a valid JSON object in this exact format (no markdown, no extra text):
{
  "verdict": "REAL" or "FAKE" or "UNCERTAIN",
  "confidence": <integer 0-100>,
  "summary": "<2-3 sentence plain-English verdict explanation>",
  "red_flags": ["<flag1>", "<flag2>"],
  "positive_signals": ["<signal1>", "<signal2>"],
  "reasoning": "<detailed multi-paragraph analysis>",
  "recommended_sources": ["<source1>", "<source2>"]
}

Base your analysis on: sensationalist language, verifiable facts, source credibility, logical consistency, known misinformation patterns."""

def analyze_news(text: str):
    client = Groq()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Analyze this news content:\n\n{text}"}
        ],
        temperature=0.3,
        max_tokens=1500,
    )
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw)

if analyze_btn:
    if not news_text.strip():
        st.warning("Please paste some news text to analyze.")
    else:
        with st.spinner("Analyzing credibility..."):
            try:
                result = analyze_news(news_text.strip())
                verdict = result.get("verdict", "UNCERTAIN")
                confidence = result.get("confidence", 50)
                summary = result.get("summary", "")
                red_flags = result.get("red_flags", [])
                positive_signals = result.get("positive_signals", [])
                reasoning = result.get("reasoning", "")
                sources = result.get("recommended_sources", [])

                verdict_class = {"REAL": "verdict-real", "FAKE": "verdict-fake", "UNCERTAIN": "verdict-uncertain"}.get(verdict, "verdict-uncertain")
                verdict_emoji = {"REAL": "✅", "FAKE": "❌", "UNCERTAIN": "⚠️"}.get(verdict, "⚠️")
                bar_color = {"REAL": "#4cff72", "FAKE": "#ff4c4c", "UNCERTAIN": "#ffd200"}.get(verdict, "#ffd200")

                st.markdown(f"""
                <div class="verdict-box {verdict_class}">
                    <div class="verdict-label">{verdict_emoji} {verdict}</div>
                    <div class="section-label" style="margin-top:0.5rem;">Confidence</div>
                    <div class="confidence-bar-wrap">
                        <div class="confidence-bar" style="width:{confidence}%; background:{bar_color};"></div>
                    </div>
                    <div class="mono">{confidence}% confidence</div>
                    <hr style="border-color:#ffffff18; margin:1rem 0;">
                    <p style="margin:0; line-height:1.6;">{summary}</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown('<hr class="divider">', unsafe_allow_html=True)

                c1, c2 = st.columns(2)
                with c1:
                    st.markdown('<div class="section-label">🚩 Red Flags</div>', unsafe_allow_html=True)
                    if red_flags:
                        chips = "".join(f'<span class="flag-chip">⚠ {f}</span>' for f in red_flags)
                        st.markdown(chips, unsafe_allow_html=True)
                    else:
                        st.markdown('<span class="mono">None detected</span>', unsafe_allow_html=True)
                with c2:
                    st.markdown('<div class="section-label">✅ Credibility Signals</div>', unsafe_allow_html=True)
                    if positive_signals:
                        chips = "".join(f'<span class="flag-chip" style="border-color:#2a3a2a; color:#8fc88f;">✓ {s}</span>' for s in positive_signals)
                        st.markdown(chips, unsafe_allow_html=True)
                    else:
                        st.markdown('<span class="mono">None detected</span>', unsafe_allow_html=True)

                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown('<div class="section-label">🧠 Detailed Analysis</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="sources-box" style="color:#ccc; line-height:1.7;">{reasoning}</div>', unsafe_allow_html=True)

                if sources:
                    st.markdown('<hr class="divider">', unsafe_allow_html=True)
                    st.markdown('<div class="section-label">📚 Verify With These Sources</div>', unsafe_allow_html=True)
                    src_html = "".join(f"<div style='padding:0.3rem 0; border-bottom:1px solid #1e1e1e;'>→ {s}</div>" for s in sources)
                    st.markdown(f'<div class="sources-box">{src_html}</div>', unsafe_allow_html=True)

            except json.JSONDecodeError:
                st.error("Could not parse the analysis. Please try again.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="mono" style="text-align:center; color:#444;">FakeGuard · Always verify with primary sources</div>', unsafe_allow_html=True)