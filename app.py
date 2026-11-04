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

st.title("Groww · Mutual Fund FAQ")
st.write(WELCOME)
st.caption(f"Covers: {', '.join(s['name'] for s in SCHEMES.values())}.")
st.info(DISCLAIMER, icon="ℹ️")

if "history" not in st.session_state:   # kept in this browser session only; nothing is written to disk
    st.session_state.history = []


def ask(question):
    result = answer(question)
    # Never keep a message that contained personal details.
    shown = "(message withheld: it contained personal details)" if result.kind == "pii" else question
    st.session_state.history.append((shown, result))


st.write("**Try an example:**")
cols = st.columns(len(EXAMPLES))
for col, ex in zip(cols, EXAMPLES):
    if col.button(ex, use_container_width=True):
        ask(ex)

typed = st.chat_input("Ask a factual question, e.g. 'Minimum SIP of HDFC Mid Cap Fund?'")
if typed:
    ask(typed)

for q, r in st.session_state.history:
    with st.chat_message("user"):
        st.write(q)
    with st.chat_message("assistant"):
        st.write(r.text)
        st.markdown(f"Source: [{r.link}]({r.link})")
        st.caption(f"Last updated from sources: {r.updated}")

st.divider()
st.caption(f"{DISCLAIMER} Source data last checked {RETRIEVED_ON}. "
           "Mutual fund investments are subject to market risks; read all scheme related documents carefully.")
