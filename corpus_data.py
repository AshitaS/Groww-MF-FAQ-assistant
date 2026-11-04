"""Corpus for the Groww-branded Mutual Fund FAQ assistant (HDFC Mutual Fund, 4 schemes).

Single source of truth: SOURCES (the 25 URLs) and CHUNKS (short fact passages,
each tied to exactly one source URL). Facts were read from the official pages on
RETRIEVED_ON. Refresh by re-opening each page and updating the values below.

Verification status of each source:
  opened    - page was opened in full and facts read from it
  snippet   - only a search-result excerpt of the official page was read
  linked    - URL is linked from an opened official page; not opened itself
"""

RETRIEVED_ON = "2026-11-04"

H = "https://www.hdfcfund.com"
F = "https://files.hdfcfund.com/s3fs-public"

SCHEMES = {
    "large": {
        "name": "HDFC Large Cap Fund",
        "aliases": ["large cap", "largecap", "large-cap"],
        "page": f"{H}/explore/mutual-funds/hdfc-large-cap-fund/direct",
        "kim": f"{F}/KIM/2025-11/KIM%20-%20HDFC%20Large%20Cap%20Fund%20dated%20November%2021%2C%202025_0.pdf?VersionId=XuOtUPPEfOmbQpuzxBMGCAdqsTmowMh4",
        "sid": f"{F}/SID/2025-11/SID%20-%20HDFC%20Large%20Cap%20Fund%20dated%20November%2021%2C%202025_0.pdf?VersionId=EaBqM_CLfPzNZ0sa96.9__cmqJdRI6jq",
        "category": "an open ended equity scheme predominantly investing in large cap stocks",
        "sip": "₹100",
        "ter": "1.02%",
        "exit": "an exit load of 1.00% is payable if units are redeemed or switched out within 1 year from the date of allotment, and no exit load is payable after 1 year",
        "lock": None,
        "benchmark": "NIFTY 100 (Total Return Index)",
    },
    "flexi": {
        "name": "HDFC Flexi Cap Fund",
        "aliases": ["flexi cap", "flexicap", "flexi-cap", "flexi"],
        "page": f"{H}/explore/mutual-funds/hdfc-flexi-cap-fund/direct",
        "kim": f"{F}/KIM/2025-11/KIM%20-%20HDFC%20Flexi%20Cap%20Fund%20dated%20November%2021%2C%202025_1.pdf?VersionId=kjfKm83nM5q0LDh1xu645ZXrnetxOtVr",
        "sid": f"{F}/SID/2025-11/SID%20-%20HDFC%20Flexi%20Cap%20Fund%20dated%20November%2021%2C%202025_0.pdf?VersionId=8eR7i2.EGl_5.cJAlLh6vNEfqjEE0vb2",
        "category": "an open ended dynamic equity scheme investing across large cap, mid cap and small cap stocks",
        "sip": "₹100",
        "ter": "0.75%",
        "exit": "an exit load of 1.00% is payable if units are redeemed or switched out within 1 year from the date of allotment, and no exit load is payable after 1 year",
        "lock": None,
        "benchmark": "NIFTY 500 Total Returns Index (TRI)",
    },
    "elss": {
        "name": "HDFC ELSS Tax Saver",
        "aliases": ["elss", "tax saver", "taxsaver", "tax saving", "tax-saver"],
        "page": f"{H}/explore/mutual-funds/hdfc-elss-tax-saver-fund/direct",
        "kim": f"{F}/KIM/2025-11/KIM%20-%20HDFC%20ELSS%20Tax%20Saver%20dated%20November%2021%2C%202025_0.pdf?VersionId=CWvBjiK_hIuApMLzaZJVRt17Sc6tmlog",
        "sid": f"{F}/SID/2025-11/SID%20-%20HDFC%20ELSS%20Tax%20Saver%20dated%20November%2021%2C%202025.pdf?VersionId=DungYvv2dhOQ1qZfNi4xvypECzXU_tEu",
        "category": "an open ended Equity Linked Savings Scheme with a statutory lock-in of 3 years and tax benefit",
        "sip": "₹500",
        "ter": "1.20%",
        "exit": "the exit load is NIL",
        "lock": "3 years",
        "benchmark": "NIFTY 500 Total Returns Index",
    },
    "mid": {
        "name": "HDFC Mid Cap Fund",
        "aliases": ["mid cap", "midcap", "mid-cap"],
        "page": f"{H}/explore/mutual-funds/hdfc-mid-cap-fund/direct",
        "kim": f"{F}/KIM/2025-11/KIM%20-%20HDFC%20Mid%20Cap%20Fund%20dated%20November%2021%2C%202025_1.pdf?VersionId=lvZLv6TD_uI7sOzea0XCJmAfPcbIHPlw",
        "sid": f"{F}/SID/2025-11/SID%20-%20HDFC%20Mid%20Cap%20Fund%20dated%20November%2021%2C%202025_1.pdf?VersionId=5ke.0bxESSJqrR9SDWhqN9DY_lIIzARd",
        "category": "an open ended equity scheme predominantly investing in mid cap stocks",
        "sip": "₹100",
        "ter": "0.74%",
        "exit": "an exit load of 1.00% is payable if units are redeemed or switched out within 1 year from the date of allotment, and no exit load is payable after 1 year",
        "lock": None,
        "benchmark": "NIFTY Midcap 150 Index (Total Returns Index)",
    },
}

LINKS = {
    "kim_listing": f"{H}/mutual-funds/fund-documents/kim",
    "factsheets": f"{H}/mutual-funds/factsheets",
    "ter_reports": f"{H}/statutory-disclosure/total-expense-ratio-of-mutual-fund-schemes/reports",
    "statement": f"{H}/services/consolidated-account-statement",
    "cap_gains": f"{H}/learn/blog/how-get-capital-gain-statement-mutual-fund-schemes-india",
    "faqs": f"{H}/services/faqs",
    "cyber": f"{H}/information/cyber-security-awareness",
    "sebi_circular": "https://www.sebi.gov.in/legal/circulars/oct-2020/circular-on-product-labeling-in-mutual-fund-schemes-risk-o-meter_47796.html",
    "sebi_circular_pdf": "https://www.sebi.gov.in/sebi_data/attachdocs/oct-2020/1602580413614.pdf",
    "sebi_invest": "https://investor.sebi.gov.in/securities-howtoinvest.html",
    "amfi_ter": "https://www.amfiindia.com/investor-corner/investor-center/Expense-Ratio.html",
    "amfi_sip": "https://www.amfiindia.com/articles/mutual-fund",
    "amfi_intro": "https://www.amfiindia.com/investor/knowledge-center-info?zoneName=IntroductionMutualFunds",
}

# ---- The 25 sources -------------------------------------------------------
# (id, title, publisher, url, type, status)
SOURCES = [
    ("S01", "HDFC MF - Fund Documents (KIM) listing", "HDFC MF", LINKS["kim_listing"], "KIM index page", "opened"),
    ("S02", "HDFC MF - How to get a capital gain statement (updated 3 Jul 2026)", "HDFC MF", LINKS["cap_gains"], "Tax-document guide", "opened"),
    ("S03", "HDFC ELSS - Tax Saver Fund (Direct) scheme page", "HDFC MF", SCHEMES["elss"]["page"], "Scheme page", "opened"),
    ("S04", "HDFC Flexi Cap Fund (Direct) scheme page", "HDFC MF", SCHEMES["flexi"]["page"], "Scheme page", "opened"),
    ("S05", "HDFC Large Cap Fund (Direct) scheme page", "HDFC MF", SCHEMES["large"]["page"], "Scheme page", "opened"),
    ("S06", "HDFC Mid Cap Fund (Direct) scheme page", "HDFC MF", SCHEMES["mid"]["page"], "Scheme page", "opened"),
    ("S07", "HDFC MF - Download Statement (account statement)", "HDFC MF", LINKS["statement"], "Statement guide", "opened"),
    ("S08", "HDFC MF - Investor FAQs index", "HDFC MF", LINKS["faqs"], "FAQ index", "opened"),
    ("S09", "HDFC MF - Monthly factsheets", "HDFC MF", LINKS["factsheets"], "Factsheet index", "opened"),
    ("S10", "HDFC MF - Total Expense Ratio reports", "HDFC MF", LINKS["ter_reports"], "Fee disclosure", "opened"),
    ("S11", "HDFC MF - Cyber security awareness", "HDFC MF", LINKS["cyber"], "Investor education", "opened"),
    ("S12", "KIM - HDFC Large Cap Fund (21 Nov 2025)", "HDFC MF", SCHEMES["large"]["kim"], "KIM (PDF)", "opened"),
    ("S13", "KIM - HDFC Flexi Cap Fund (21 Nov 2025)", "HDFC MF", SCHEMES["flexi"]["kim"], "KIM (PDF)", "linked"),
    ("S14", "KIM - HDFC ELSS Tax Saver (21 Nov 2025)", "HDFC MF", SCHEMES["elss"]["kim"], "KIM (PDF)", "linked"),
    ("S15", "KIM - HDFC Mid Cap Fund (21 Nov 2025)", "HDFC MF", SCHEMES["mid"]["kim"], "KIM (PDF)", "linked"),
    ("S16", "SID - HDFC Large Cap Fund (21 Nov 2025)", "HDFC MF", SCHEMES["large"]["sid"], "SID (PDF)", "linked"),
    ("S17", "SID - HDFC Flexi Cap Fund (21 Nov 2025)", "HDFC MF", SCHEMES["flexi"]["sid"], "SID (PDF)", "linked"),
    ("S18", "SID - HDFC ELSS Tax Saver (21 Nov 2025)", "HDFC MF", SCHEMES["elss"]["sid"], "SID (PDF)", "linked"),
    ("S19", "SID - HDFC Mid Cap Fund (21 Nov 2025)", "HDFC MF", SCHEMES["mid"]["sid"], "SID (PDF)", "linked"),
    ("S20", "SEBI circular - Product labeling in MF schemes: Risk-o-meter (5 Oct 2020)", "SEBI", LINKS["sebi_circular"], "Regulation", "opened"),
    ("S21", "SEBI circular PDF - Risk-o-meter (5 Oct 2020)", "SEBI", LINKS["sebi_circular_pdf"], "Regulation (PDF)", "opened"),
    ("S22", "SEBI Investor - How to invest in the securities market", "SEBI", LINKS["sebi_invest"], "Investor education", "linked"),
    ("S23", "AMFI - What is Expense Ratio", "AMFI", LINKS["amfi_ter"], "Investor education", "opened"),
    ("S24", "AMFI - Mutual fund / SIP article", "AMFI", LINKS["amfi_sip"], "Investor education", "opened"),
    ("S25", "AMFI - Introduction to Mutual Funds (knowledge center)", "AMFI", LINKS["amfi_intro"], "Investor education", "linked"),
]


# ---- Chunks ----------------------------------------------------------------
def _chunk(cid, text, url, scheme=None, topic="general"):
    return {"id": cid, "text": text, "url": url, "scheme": scheme, "topic": topic,
            "retrieved_on": RETRIEVED_ON}


def _build_chunks():
    out = []
    for key, s in SCHEMES.items():
        n, page = s["name"], s["page"]
        out.append(_chunk(
            f"{key}-ter",
            f"The Total Expense Ratio (TER) shown on the {n} Direct Plan page is {s['ter']}, including additional expenses and GST on management fees. "
            f"The Regular Plan has its own page and figure, and TER can change, so check the linked page for the current number.",
            page, key, "expense_ratio"))
        out.append(_chunk(
            f"{key}-exit",
            f"For {n}, {s['exit']}.",
            page, key, "exit_load"))
        sip_extra = {
            "elss": " The scheme FAQ says SIP and lump sum both need at least ₹500, and any additional purchase must also be at least ₹500.",
            "mid": " The scheme FAQ says SIP and lump sum both need at least ₹100, and any additional purchase must also be at least ₹100.",
            "flexi": " The scheme FAQ adds that this is as specified by the scheme, so check the scheme information document for the latest requirements.",
            "large": "",
        }[key]
        out.append(_chunk(
            f"{key}-sip",
            f"The minimum SIP amount for {n} is {s['sip']}, as shown on its scheme page.{sip_extra}",
            page, key, "min_sip"))
        if s["lock"]:
            out.append(_chunk(
                f"{key}-lock",
                f"{n} is an Equity Linked Savings Scheme with a statutory lock-in period of {s['lock']}. "
                f"Per its scheme page, investments qualify for a deduction under Section 80C of up to ₹1.5 lakh.",
                page, key, "lock_in"))
        else:
            out.append(_chunk(
                f"{key}-lock",
                f"The {n} page lists its lock-in period as NA (not applicable), so no lock-in is stated for this scheme.",
                page, key, "lock_in"))
        out.append(_chunk(
            f"{key}-risk",
            f"The {n} page shows its riskometer as Very High (product label: very high risk) and also displays a separate benchmark riskometer.",
            page, key, "riskometer"))
        out.append(_chunk(
            f"{key}-bench",
            f"{n} is benchmarked against the {s['benchmark']}, as listed on its scheme page.",
            page, key, "benchmark"))
        out.append(_chunk(
            f"{key}-kim",
            f"The Key Information Memorandum (KIM) for {n} is dated November 21, 2025 and is available at the linked PDF.",
            s["kim"], key, "documents_kim"))
        out.append(_chunk(
            f"{key}-sid",
            f"The Scheme Information Document (SID) for {n} is dated November 21, 2025 and is available at the linked PDF.",
            s["sid"], key, "documents_sid"))

    out.append(_chunk(
        "gen-entry-load",
        "HDFC's scheme pages note that mutual funds in India currently do not levy entry loads, and show the entry load as NA.",
        SCHEMES["elss"]["page"], None, "entry_load"))
    out.append(_chunk(
        "gen-statement",
        "On HDFC Mutual Fund's Download Statement page you enter your PAN or folio, verify with an OTP, choose a duration such as the current financial year, and select Send Email. "
        "The account statement is free and can be PAN-based (all folios under that PAN) or folio-based (one folio).",
        LINKS["statement"], None, "statement"))
    out.append(_chunk(
        "gen-capgains",
        "A capital gain statement covers gains or losses on redeemed mutual fund units and can be requested from the registrars CAMS or KFintech, from your investment platform, from the AMC website, "
        "or as a consolidated account statement in capital-gains format via CAMS or NSDL. "
        "It is generally free and usually available after the financial year ends in March, so it can be used for ITR filing.",
        LINKS["cap_gains"], None, "capital_gains"))
    out.append(_chunk(
        "gen-kim-listing",
        "HDFC Mutual Fund lists the KIM, SID and scheme summary documents for all its schemes on its Fund Documents page.",
        LINKS["kim_listing"], None, "documents"))
    out.append(_chunk(
        "gen-factsheet",
        "HDFC Mutual Fund publishes factsheets, endeavoured monthly, with scheme objective, inception date, fund manager, portfolio holdings, risk ratios and historical performance.",
        LINKS["factsheets"], None, "factsheet"))
    out.append(_chunk(
        "gen-riskometer",
        "SEBI's circular of October 5, 2020 defines the mutual fund risk-o-meter with six levels: Low, Low to Moderate, Moderate, Moderately High, High and Very High. "
        "The risk-o-meter is evaluated monthly and disclosed by AMCs with their portfolio disclosures.",
        LINKS["sebi_circular"], None, "riskometer_def"))
    out.append(_chunk(
        "gen-ter-def",
        "AMFI describes the expense ratio as the cost of running and managing a mutual fund, which is charged to the scheme.",
        LINKS["amfi_ter"], None, "expense_ratio_def"))
    out.append(_chunk(
        "gen-sip-def",
        "AMFI describes a Systematic Investment Plan (SIP) as a plan offered by mutual funds in which you invest a fixed amount in a scheme periodically at fixed intervals, for example once a month.",
        LINKS["amfi_sip"], None, "sip_def"))
    return out


CHUNKS = _build_chunks()
