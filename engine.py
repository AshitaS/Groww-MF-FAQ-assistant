"""Facts-only MF FAQ engine: guardrails -> retrieval (BM25) -> grounded answer.

Order of decisions (W1: decide answer vs refuse):
  1. PII in the message        -> refuse, never echo or store the message
  2. Advice / opinion question -> polite refusal + educational link
  3. Performance / returns     -> no numbers, link to the official page/factsheet
  4. Factual question          -> retrieve a chunk, answer in <= 3 sentences + 1 link
"""
import math
import re
from collections import Counter
from dataclasses import dataclass

from corpus_data import CHUNKS, LINKS, RETRIEVED_ON, SCHEMES

DISCLAIMER = "Facts-only. No investment advice."
MAX_SENTENCES = 3

# ---------------------------------------------------------------- guardrails
PII_PATTERNS = [
    re.compile(r"\b[A-Za-z]{5}[0-9]{4}[A-Za-z]\b"),                   # PAN
    re.compile(r"(?<!\d)\d{4}[\s-]?\d{4}[\s-]?\d{4}(?!\d)"),           # Aadhaar (12 digits)
    re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),                           # email
    re.compile(r"(?<!\d)(?:\+?91[\s-]?)?[6-9]\d{9}(?!\d)"),            # Indian mobile
    re.compile(r"(?<!\d)\d{9,18}(?!\d)"),                              # account-like numbers
    re.compile(r"\botp\b\D{0,15}\d{4,8}", re.I),                       # OTP value
    re.compile(r"\bfolio\b\D{0,15}\d{5,}", re.I),                      # folio number
]

ADVICE = re.compile(
    r"\b(should (i|we)|shall i|is it (good|safe|worth|wise)|worth (it|investing|buying)|"
    r"recommend|suggest|advise|which (one )?(is )?(better|best)|best (fund|scheme|mutual|elss|sip)|"
    r"better than|good (fund|scheme|investment|time)|right time|safe to invest|"
    r"(buy|sell|hold|switch|redeem|stop|continue|start) (it|this|the|my|now|more)|"
    r"my portfolio|portfolio|will (it|the fund) (grow|rise|fall|beat|give)|predict|future value)\b",
    re.I)

PERFORMANCE = re.compile(
    r"\b(returns?|cagr|xirr|performance|performed|outperform\w*|beat|profit\w*|"
    r"how much (did|has|will)|growth rate|nav)\b", re.I)

OTHER_AMC = re.compile(
    r"\b(sbi|icici|axis|kotak|nippon|mirae|parag parikh|ppfas|quant|dsp|tata|uti|aditya birla|"
    r"franklin|invesco|motilal|bandhan|hsbc|canara|groww mutual)\b", re.I)
OTHER_HDFC = re.compile(
    r"\bhdfc\b.*\b(small cap|balanced|hybrid|liquid|debt|nifty|sensex|index|gold|focused|"
    r"multi.?cap|top 100|equity fund)\b", re.I)

# ---------------------------------------------------------------- topics
TOPIC_RULES = [  # (topic, regex) - first match wins
    ("capital_gains", re.compile(r"capital.?gains?|tax (statement|document|report)|itr|tax filing", re.I)),
    ("documents_sid", re.compile(r"\bsid\b|scheme information", re.I)),
    ("documents_kim", re.compile(r"\bkim\b|key information", re.I)),
    ("factsheet", re.compile(r"fact.?sheet|fund facts", re.I)),
    ("statement", re.compile(r"statement|\bcas\b|account summary|download|folio summary", re.I)),
    ("entry_load", re.compile(r"entry load", re.I)),
    ("exit_load", re.compile(r"exit.?load|exit charge|redemption (fee|charge)|early (exit|redeem|withdraw)", re.I)),
    ("expense_ratio", re.compile(r"expense|\bter\b|fund management (fee|charge)", re.I)),
    ("lock_in", re.compile(r"lock.?in|locked", re.I)),
    ("riskometer", re.compile(r"risk.?o.?meter|risk meter|risk level|riskometer|how risky|risk grade", re.I)),
    ("benchmark", re.compile(r"benchmark|compared against|tracks which index", re.I)),
    ("min_sip", re.compile(r"min(imum)?|lowest|least|smallest|start (a )?sip|sip amount|lump.?sum|how much (to|can) (invest|start)", re.I)),
    ("sip_def", re.compile(r"\bsip\b|systematic investment", re.I)),
]
DEFINITION = re.compile(r"\b(what is|what's|what are|meaning of|define|explain|full form)\b", re.I)

STOP = set("the a an of for to in on is are what whats how do does i me my and or it this that "
           "with at by be as from can which when where who about tell give please hdfc fund".split())


def _tok(text):
    return [w for w in re.findall(r"[a-z0-9₹]+", text.lower()) if w not in STOP]


# ---------------------------------------------------------------- retrieval (BM25)
class Retriever:
    def __init__(self, chunks, k1=1.5, b=0.75):
        self.chunks, self.k1, self.b = chunks, k1, b
        self.docs = [Counter(_tok(c["text"] + " " + c["topic"].replace("_", " ") +
                                  " " + (SCHEMES[c["scheme"]]["name"] if c["scheme"] else "")))
                     for c in chunks]
        self.lens = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lens) / len(self.lens)
        df = Counter(t for d in self.docs for t in d)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def score(self, query, i):
        d, s = self.docs[i], 0.0
        for t in _tok(query):
            if t in d:
                tf = d[t]
                s += self.idf[t] * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * self.lens[i] / self.avg))
        return s

    def search(self, query, scheme=None, topic=None, k=3):
        ranked = []
        for i, c in enumerate(self.chunks):
            if scheme and c["scheme"] not in (None, scheme):
                continue  # never mix another scheme's facts into the answer
            s = self.score(query, i)
            if scheme and c["scheme"] == scheme:
                s += 2.0
            if topic and c["topic"] == topic:
                s += 6.0
            ranked.append((s, c))
        ranked.sort(key=lambda x: -x[0])
        return ranked[:k]


RETRIEVER = Retriever(CHUNKS)


def detect_scheme(q):
    ql = q.lower()
    for key in ("elss", "mid", "large", "flexi"):  # ELSS first: "tax saver" is unambiguous
        if any(a in ql for a in SCHEMES[key]["aliases"]):
            return key
    return None


def detect_topic(q):
    for topic, rx in TOPIC_RULES:
        if rx.search(q):
            return topic
    return None


# ---------------------------------------------------------------- answers
@dataclass
class Answer:
    kind: str          # answer | refusal | redirect | clarify | pii | out_of_scope | no_answer
    text: str
    link: str
    updated: str = RETRIEVED_ON
    sources: tuple = ()

    def render(self):
        return f"{self.text}\n\nSource: {self.link}\nLast updated from sources: {self.updated}"


def count_sentences(text):
    return len([s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s])


def contains_pii(q):
    return any(p.search(q) for p in PII_PATTERNS)


SCHEME_LIST = "HDFC Large Cap Fund, HDFC Flexi Cap Fund, HDFC ELSS Tax Saver and HDFC Mid Cap Fund"


def answer(question, use_llm=True):
    q = (question or "").strip()
    if not q:
        return Answer("clarify", "Please type a factual question about one of the covered schemes.",
                      LINKS["kim_listing"])

    if contains_pii(q):
        return Answer(
            "pii",
            "Please don't share personal details such as PAN, Aadhaar, account or folio numbers, OTPs, emails or phone numbers. "
            "I haven't kept your message, so please remove them and ask again. "
            "To stay safe from scams, see HDFC Mutual Fund's cyber safety guide.",
            LINKS["cyber"])

    scheme = detect_scheme(q)
    topic = detect_topic(q)

    if ADVICE.search(q):
        return Answer(
            "refusal",
            "I can only share facts from official sources, so I can't advise whether to buy, sell, switch or hold any scheme. "
            "I can tell you facts such as a scheme's expense ratio, exit load, minimum SIP, lock-in, riskometer or benchmark. "
            "To learn how to approach investing, see SEBI's investor education page.",
            LINKS["sebi_invest"])

    if PERFORMANCE.search(q) and topic not in ("statement", "capital_gains", "benchmark"):
        link = SCHEMES[scheme]["page"] if scheme else LINKS["factsheets"]
        return Answer(
            "redirect",
            "I don't compute, quote or compare returns or NAVs because they change and need context. "
            "The official scheme page and monthly factsheet show performance data.",
            link)

    if (OTHER_AMC.search(q) or OTHER_HDFC.search(q)) and not scheme:
        return Answer("out_of_scope",
                      f"I only cover four schemes: {SCHEME_LIST}. I can't answer for other funds.",
                      LINKS["kim_listing"])

    scheme_topics = {"expense_ratio", "exit_load", "min_sip", "lock_in", "riskometer", "benchmark",
                     "documents_kim", "documents_sid"}

    # Definition-style questions that need no scheme
    if topic == "riskometer" and not scheme:
        topic = "riskometer_def"
    elif topic == "expense_ratio" and not scheme and DEFINITION.search(q):
        topic = "expense_ratio_def"
    elif topic == "sip_def" and not scheme:
        pass

    if topic == "lock_in" and not scheme and re.search(r"\belss\b|tax", q, re.I):
        scheme = "elss"

    if scheme and not topic:
        return Answer("clarify",
                      f"What would you like to know about {SCHEMES[scheme]['name']}? I can share its expense ratio, exit load, "
                      f"minimum SIP, lock-in, riskometer, benchmark, KIM or SID.",
                      SCHEMES[scheme]["page"])

    if topic in scheme_topics and not scheme:
        return Answer("clarify",
                      f"Which scheme do you mean? I cover {SCHEME_LIST}.",
                      LINKS["kim_listing"])

    if not topic:  # no recognised fact asked: don't guess from stray word overlap
        return Answer("no_answer",
                      "I couldn't find that in my official sources. The HDFC Mutual Fund fund-documents page lists each scheme's KIM and SID.",
                      LINKS["kim_listing"])

    hits = RETRIEVER.search(q, scheme=scheme, topic=topic, k=3)
    if not hits or hits[0][0] < 1.0:
        return Answer("no_answer",
                      "I couldn't find that in my official sources. The HDFC Mutual Fund fund-documents page lists each scheme's KIM and SID.",
                      LINKS["kim_listing"])

    chunk = hits[0][1]
    text = chunk["text"]
    if use_llm:
        try:
            from llm import rephrase
            text = rephrase(q, chunk["text"]) or text
        except Exception:
            pass
    assert count_sentences(text) <= MAX_SENTENCES, f"answer too long for {chunk['id']}"
    return Answer("answer", text, chunk["url"], chunk["retrieved_on"], (chunk["id"],))
