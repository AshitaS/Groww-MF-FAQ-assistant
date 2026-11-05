import html

import streamlit as st

from engine import DISCLAIMER, SCHEMES, answer
from corpus_data import RETRIEVED_ON

st.set_page_config(page_title="Groww MF FAQ Assistant", page_icon="💬", layout="centered")

WELCOME = "Hi! Ask me factual questions about four HDFC Mutual Fund schemes, answered only from official public pages."
EXAMPLES = [
    "What is the ELSS lock-in period?",
    "What is the exit load of HDFC Flexi Cap Fund?",
    "How do I download my capital gains statement?",
]
BADGES = {  # answer kind -> (label, css class)
    "answer": ("FACT", "ok"),
    "refusal": ("NO ADVICE", "warn"),
    "redirect": ("REDIRECT", "info"),
    "clarify": ("NEED A DETAIL", "mute"),
    "pii": ("PRIVACY", "bad"),
    "out_of_scope": ("OUT OF SCOPE", "mute"),
    "no_answer": ("NOT FOUND", "mute"),
}
# Short labels for the reference cards (facts verified on the scheme pages, 2026-11-04).
CARD = {
    "large": ("Large Cap", "Equity", "NIFTY 100 TRI"),
    "flexi": ("Flexi Cap", "Equity", "NIFTY 500 TRI"),
    "elss": ("ELSS Tax Saver", "Equity · 3-year lock-in", "NIFTY 500 TRI"),
    "mid": ("Mid Cap", "Equity", "NIFTY Midcap 150 TRI"),
}

if "history" not in st.session_state:   # kept in this browser session only; nothing is written to disk
    st.session_state.history = []
if "dark" not in st.session_state:
    st.session_state.dark = False       # light mode by default

LIGHT = dict(bg="#F6F8FB", card="#FFFFFF", card2="#F1F5F9", ink="#14213D", mute="#5F6B85", line="#E2E8F0",
             g="#00A67E", b="#3D6BFF", shadow="0 10px 30px rgba(27,42,90,.08)", glow="rgba(0,166,126,.12)")
DARK = dict(bg="#0B0F1C", card="#141C34", card2="#18223F", ink="#E8ECF5", mute="#93A0BA", line="#2A3556",
            g="#00D09C", b="#5B8CFF", shadow="0 20px 60px rgba(0,0,0,.4)", glow="rgba(0,208,156,.15)")
T = DARK if st.session_state.dark else LIGHT
VARS = ";".join(f"--{k}:{v}" for k, v in T.items())

st.markdown(
    f"""
<style>
:root {{ {VARS} }}
#MainMenu, footer, header[data-testid="stHeader"] {{ visibility:hidden; height:0; }}
.stApp {{ background:var(--bg); color:var(--ink); }}
.block-container {{ max-width:900px; padding-top:1.4rem; padding-bottom:6rem; }}
.stApp, .stApp p, .stApp span, .stApp label {{ color:var(--ink); }}
.top {{ display:flex; justify-content:space-between; align-items:center; }}
.brand {{ display:flex; align-items:center; gap:10px; font-weight:700; font-size:16px; color:var(--ink); }}
.logo {{ width:30px; height:30px; border-radius:9px; background:linear-gradient(135deg,#00D09C,#3D6BFF);
         display:grid; place-items:center; color:#fff; font-weight:800; }}
.pill {{ display:inline-block; font-size:12px; font-weight:600; color:var(--g); border:1px solid var(--g);
         padding:6px 12px; border-radius:999px; background:var(--glow); }}
h1.title {{ font-size:34px; line-height:1.15; margin:18px 0 6px; padding:0; letter-spacing:-.02em; color:var(--ink); }}
h1.title span {{ background:linear-gradient(90deg,var(--g),var(--b)); -webkit-background-clip:text; color:transparent; }}
.sub {{ color:var(--mute) !important; font-size:15px; line-height:1.5; max-width:640px; margin-bottom:4px; }}
.lab {{ font-size:12px; letter-spacing:.12em; color:var(--mute); text-transform:uppercase; font-weight:700; margin:22px 0 10px; }}
/* buttons: example cards and theme toggle */
.stButton > button {{ background:var(--card); color:var(--ink); border:1px solid var(--line); border-radius:14px;
                      box-shadow:var(--shadow); font-weight:600; font-size:14px; line-height:1.4; width:100%;
                      padding:.8rem 1rem; min-height:76px; text-align:left; transition:all .15s; }}
.stButton > button:hover {{ border-color:var(--g); color:var(--g); }}
.stButton > button p {{ color:inherit !important; }}
.tog .stButton > button {{ min-height:0; border-radius:999px; padding:.3rem .9rem; font-size:12.5px; box-shadow:none; text-align:center; }}
[data-testid="stChatInput"] {{ border-radius:999px; background:var(--card); border:1px solid var(--line); box-shadow:var(--shadow); }}
[data-testid="stChatInput"] textarea {{ color:var(--ink); background:transparent; }}
[data-testid="stBottom"] > div, [data-testid="stBottomBlockContainer"] {{ background:var(--bg); }}
.res {{ margin-top:18px; border-radius:20px; background:var(--card); border:1px solid var(--line); overflow:hidden; box-shadow:var(--shadow); }}
.res .h {{ display:flex; justify-content:space-between; align-items:center; gap:12px; padding:12px 20px; background:var(--card2);
           border-bottom:1px solid var(--line); font-size:13px; color:var(--mute); }}
.badge {{ font-size:11px; font-weight:700; padding:3px 10px; border-radius:999px; white-space:nowrap; }}
.ok {{ background:var(--glow); color:var(--g); }} .warn {{ background:rgba(255,176,32,.18); color:#B26A00; }}
.info {{ background:rgba(61,107,255,.14); color:var(--b); }} .bad {{ background:rgba(255,92,92,.16); color:#D23B3B; }}
.mute {{ background:var(--card2); color:var(--mute); }}
.res .b {{ padding:18px 22px 6px; font-size:17px; line-height:1.55; color:var(--ink); }}
.src {{ margin:14px 22px 18px; background:var(--card2); border:1px solid var(--line); border-left:3px solid var(--g);
        border-radius:10px; padding:10px 14px; font-size:12.5px; }}
.src .t {{ font-weight:700; margin-bottom:2px; color:var(--ink); }}
.src a {{ color:var(--b); word-break:break-all; text-decoration:none; }} .src a:hover {{ text-decoration:underline; }}
.src .d {{ color:var(--mute); margin-top:3px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:12px; }}
.sc {{ background:var(--card); border:1px solid var(--line); border-radius:16px; padding:14px; box-shadow:var(--shadow); }}
.sc .n {{ font-weight:700; font-size:15px; color:var(--ink); }} .sc .c {{ font-size:11.5px; color:var(--mute); margin-bottom:8px; }}
.sc .r {{ display:flex; justify-content:space-between; gap:8px; font-size:12px; padding:4px 0; border-top:1px solid var(--line); color:var(--ink); }}
.sc .r span {{ color:var(--mute); }} .sc .r b {{ font-weight:600; text-align:right; }}
.foot {{ text-align:center; color:var(--mute); font-size:12px; margin-top:26px; line-height:1.7; border-top:1px solid var(--line); padding-top:14px; }}
.foot b {{ color:var(--ink); }}
</style>
""",
    unsafe_allow_html=True,
)


def ask(question):
    result = answer(question)
    # Never keep a message that contained personal details.
    shown = "(message withheld: it contained personal details)" if result.kind == "pii" else question
    st.session_state.history.append((shown, result))


# ---- header -------------------------------------------------------------
left, right = st.columns([5, 1])
with left:
    st.markdown(
        f'<div class="top"><div class="brand"><div class="logo">₹</div>Groww · MF FAQ</div></div>'
        f'<div style="margin-top:10px"><span class="pill">ℹ️ {html.escape(DISCLAIMER)}</span></div>',
        unsafe_allow_html=True,
    )
with right:
    st.markdown('<div class="tog">', unsafe_allow_html=True)
    if st.button("☀️ Light" if st.session_state.dark else "🌙 Dark", key="theme"):
        st.session_state.dark = not st.session_state.dark
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    f'<h1 class="title">Mutual fund facts, <span>straight from the source.</span></h1>'
    f'<div class="sub">{html.escape(WELCOME)}</div>',
    unsafe_allow_html=True,
)

# ---- example questions + ask bar -----------------------------------------
st.markdown('<div class="lab">Try an example</div>', unsafe_allow_html=True)
cols = st.columns(len(EXAMPLES))
for i, (col, ex) in enumerate(zip(cols, EXAMPLES)):
    if col.button(ex, key=f"ex{i}", use_container_width=True):
        ask(ex)

typed = st.chat_input("Or type your own question, e.g. 'Minimum SIP of HDFC Mid Cap Fund?'")
if typed:
    ask(typed)

# ---- answers (newest first) ---------------------------------------------
for q, r in reversed(st.session_state.history):
    label, css = BADGES.get(r.kind, ("ANSWER", "mute"))
    link = html.escape(r.link, quote=True)
    st.markdown(
        f"""
<div class="res">
  <div class="h"><span>{html.escape(q)}</span><span class="badge {css}">{label}</span></div>
  <div class="b">{html.escape(r.text)}</div>
  <div class="src"><div class="t">Source</div>
    <a href="{link}" target="_blank" rel="noopener noreferrer">{link}</a>
    <div class="d">Last updated from sources: {html.escape(r.updated)}</div></div>
</div>
""",
        unsafe_allow_html=True,
    )

# ---- covered schemes (reference only) ------------------------------------
cards = ""
for key, (name, sub, bench) in CARD.items():
    s = SCHEMES[key]
    cards += (
        f'<div class="sc"><div class="n">{html.escape(name)}</div><div class="c">HDFC · {html.escape(sub)}</div>'
        f'<div class="r"><span>Benchmark</span><b>{html.escape(bench)}</b></div>'
        f'<div class="r"><span>Min SIP</span><b>{html.escape(s["sip"])}</b></div>'
        f'<div class="r"><span>Risk</span><b>Very High</b></div></div>'
    )
st.markdown(f'<div class="lab">Covered schemes</div><div class="grid">{cards}</div>', unsafe_allow_html=True)

st.markdown(
    f"""<div class="foot"><b>{html.escape(DISCLAIMER)}</b> Source data last checked {html.escape(RETRIEVED_ON)}.<br>
Mutual fund investments are subject to market risks; read all scheme related documents carefully.
Please don't share PAN, Aadhaar, account numbers, OTPs, emails or phone numbers.</div>""",
    unsafe_allow_html=True,
)
