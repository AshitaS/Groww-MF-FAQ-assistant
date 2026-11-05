[README.md](https://github.com/user-attachments/files/34434074/README.md)
# Groww · Mutual Fund FAQ Assistant (facts-only RAG)

A small chat app that answers *factual* questions about four HDFC Mutual Fund schemes using only official public pages (HDFC Mutual Fund, SEBI, AMFI). Every answer is at most 3 sentences, carries exactly one source link and a "Last updated from sources" date. It refuses advice, does not quote returns/NAV, and rejects messages containing personal details.

- **Product context:** Groww (the assistant is the kind of FAQ widget a Groww-style app would embed).
- **AMC:** HDFC Mutual Fund. **Schemes:** HDFC Large Cap Fund, HDFC Flexi Cap Fund, HDFC ELSS Tax Saver, HDFC Mid Cap Fund.
- **Live app:** https://hdfc-mf-faq-assistant.streamlit.app/
- **Corpus:** 25 public pages (listed below).

## Setup
```bash
python3 -m pip install -r requirements.txt
python3 -m unittest test_engine      # 20 tests
python3 -m streamlit run app.py
```
Optional wording layer: set `ANTHROPIC_API_KEY` (model via `MF_FAQ_MODEL`). Output is validated (max 3 sentences, no links, no new numbers) and falls back to the retrieved text. Without a key the app is fully rule-based and deterministic.

Hosting: push this folder to GitHub, then deploy on Streamlit Community Cloud with `app.py` as the main file.

## How it maps to the milestone themes
- **W1, Thinking like a model:** `engine.answer()` identifies the fact and scheme asked, then decides in order: personal details, advice refusal, returns/NAV redirect, out-of-scope fund, clarifying question, then answer. Covered by `test_engine.py`.
- **W2, LLMs and prompting:** fixed, polite refusal wording with an educational link; one consistent citation format; a concise grounded prompt in `llm.py` (optional, validated output).
- **W3, RAG only:** BM25 retrieval over a small curated corpus with scheme and topic boosting; every chunk carries exactly one URL from the source list, and a test checks that.

## Files
`app.py` UI, `engine.py` guardrails and retrieval, `corpus_data.py` sources and facts, `llm.py` optional wording, `test_engine.py`, `sources.csv` / `sources.md`, `sample_qa.md`, `DISCLAIMER.md`, `scripts/make_outputs.py` (regenerates the CSV, sample Q&A and this README).

## Disclaimer (as shown in the UI)
**Facts-only. No investment advice.**

Mutual fund investments are subject to market risks; read all scheme related documents carefully.
This assistant quotes facts from official public pages (HDFC Mutual Fund, SEBI, AMFI). It does not recommend, compare or rate schemes, and does not quote returns or NAV. Please do not share personal details (PAN, Aadhaar, account/folio numbers, OTP, email, phone).

## Source list (25 pages, checked 2026-11-04)
Status: **opened** = page read in full on the check date; **linked** = linked from an opened official page, not yet opened.

| ID | Title | Publisher | Status | URL |
|---|---|---|---|---|
| S01 | HDFC MF - Fund Documents (KIM) listing | HDFC MF | opened | https://www.hdfcfund.com/mutual-funds/fund-documents/kim |
| S02 | HDFC MF - How to get a capital gain statement (updated 3 Jul 2026) | HDFC MF | opened | https://www.hdfcfund.com/learn/blog/how-get-capital-gain-statement-mutual-fund-schemes-india |
| S03 | HDFC ELSS - Tax Saver Fund (Direct) scheme page | HDFC MF | opened | https://www.hdfcfund.com/explore/mutual-funds/hdfc-elss-tax-saver-fund/direct |
| S04 | HDFC Flexi Cap Fund (Direct) scheme page | HDFC MF | opened | https://www.hdfcfund.com/explore/mutual-funds/hdfc-flexi-cap-fund/direct |
| S05 | HDFC Large Cap Fund (Direct) scheme page | HDFC MF | opened | https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-cap-fund/direct |
| S06 | HDFC Mid Cap Fund (Direct) scheme page | HDFC MF | opened | https://www.hdfcfund.com/explore/mutual-funds/hdfc-mid-cap-fund/direct |
| S07 | HDFC MF - Download Statement (account statement) | HDFC MF | opened | https://www.hdfcfund.com/services/consolidated-account-statement |
| S08 | HDFC MF - Investor FAQs index | HDFC MF | opened | https://www.hdfcfund.com/services/faqs |
| S09 | HDFC MF - Monthly factsheets | HDFC MF | opened | https://www.hdfcfund.com/mutual-funds/factsheets |
| S10 | HDFC MF - Total Expense Ratio reports | HDFC MF | opened | https://www.hdfcfund.com/statutory-disclosure/total-expense-ratio-of-mutual-fund-schemes/reports |
| S11 | HDFC MF - Cyber security awareness | HDFC MF | opened | https://www.hdfcfund.com/information/cyber-security-awareness |
| S12 | KIM - HDFC Large Cap Fund (21 Nov 2025) | HDFC MF | opened | https://files.hdfcfund.com/s3fs-public/KIM/2025-11/KIM%20-%20HDFC%20Large%20Cap%20Fund%20dated%20November%2021%2C%202025_0.pdf?VersionId=XuOtUPPEfOmbQpuzxBMGCAdqsTmowMh4 |
| S13 | KIM - HDFC Flexi Cap Fund (21 Nov 2025) | HDFC MF | linked | https://files.hdfcfund.com/s3fs-public/KIM/2025-11/KIM%20-%20HDFC%20Flexi%20Cap%20Fund%20dated%20November%2021%2C%202025_1.pdf?VersionId=kjfKm83nM5q0LDh1xu645ZXrnetxOtVr |
| S14 | KIM - HDFC ELSS Tax Saver (21 Nov 2025) | HDFC MF | linked | https://files.hdfcfund.com/s3fs-public/KIM/2025-11/KIM%20-%20HDFC%20ELSS%20Tax%20Saver%20dated%20November%2021%2C%202025_0.pdf?VersionId=CWvBjiK_hIuApMLzaZJVRt17Sc6tmlog |
| S15 | KIM - HDFC Mid Cap Fund (21 Nov 2025) | HDFC MF | linked | https://files.hdfcfund.com/s3fs-public/KIM/2025-11/KIM%20-%20HDFC%20Mid%20Cap%20Fund%20dated%20November%2021%2C%202025_1.pdf?VersionId=lvZLv6TD_uI7sOzea0XCJmAfPcbIHPlw |
| S16 | SID - HDFC Large Cap Fund (21 Nov 2025) | HDFC MF | linked | https://files.hdfcfund.com/s3fs-public/SID/2025-11/SID%20-%20HDFC%20Large%20Cap%20Fund%20dated%20November%2021%2C%202025_0.pdf?VersionId=EaBqM_CLfPzNZ0sa96.9__cmqJdRI6jq |
| S17 | SID - HDFC Flexi Cap Fund (21 Nov 2025) | HDFC MF | linked | https://files.hdfcfund.com/s3fs-public/SID/2025-11/SID%20-%20HDFC%20Flexi%20Cap%20Fund%20dated%20November%2021%2C%202025_0.pdf?VersionId=8eR7i2.EGl_5.cJAlLh6vNEfqjEE0vb2 |
| S18 | SID - HDFC ELSS Tax Saver (21 Nov 2025) | HDFC MF | linked | https://files.hdfcfund.com/s3fs-public/SID/2025-11/SID%20-%20HDFC%20ELSS%20Tax%20Saver%20dated%20November%2021%2C%202025.pdf?VersionId=DungYvv2dhOQ1qZfNi4xvypECzXU_tEu |
| S19 | SID - HDFC Mid Cap Fund (21 Nov 2025) | HDFC MF | linked | https://files.hdfcfund.com/s3fs-public/SID/2025-11/SID%20-%20HDFC%20Mid%20Cap%20Fund%20dated%20November%2021%2C%202025_1.pdf?VersionId=5ke.0bxESSJqrR9SDWhqN9DY_lIIzARd |
| S20 | SEBI circular - Product labeling in MF schemes: Risk-o-meter (5 Oct 2020) | SEBI | opened | https://www.sebi.gov.in/legal/circulars/oct-2020/circular-on-product-labeling-in-mutual-fund-schemes-risk-o-meter_47796.html |
| S21 | SEBI circular PDF - Risk-o-meter (5 Oct 2020) | SEBI | opened | https://www.sebi.gov.in/sebi_data/attachdocs/oct-2020/1602580413614.pdf |
| S22 | SEBI Investor - How to invest in the securities market | SEBI | linked | https://investor.sebi.gov.in/securities-howtoinvest.html |
| S23 | AMFI - What is Expense Ratio | AMFI | opened | https://www.amfiindia.com/investor-corner/investor-center/Expense-Ratio.html |
| S24 | AMFI - Mutual fund / SIP article | AMFI | opened | https://www.amfiindia.com/articles/mutual-fund |
| S25 | AMFI - Introduction to Mutual Funds (knowledge center) | AMFI | linked | https://www.amfiindia.com/investor/knowledge-center-info?zoneName=IntroductionMutualFunds |

## Sample Q&A (generated from the real engine)
### 1. What is the ELSS lock-in period?
*Type: answer*

HDFC ELSS Tax Saver is an Equity Linked Savings Scheme with a statutory lock-in period of 3 years. Per its scheme page, investments qualify for a deduction under Section 80C of up to ₹1.5 lakh.

Source: https://www.hdfcfund.com/explore/mutual-funds/hdfc-elss-tax-saver-fund/direct
Last updated from sources: 2026-11-04

### 2. What is the exit load of HDFC Flexi Cap Fund?
*Type: answer*

For HDFC Flexi Cap Fund, an exit load of 1.00% is payable if units are redeemed or switched out within 1 year from the date of allotment, and no exit load is payable after 1 year.

Source: https://www.hdfcfund.com/explore/mutual-funds/hdfc-flexi-cap-fund/direct
Last updated from sources: 2026-11-04

### 3. What is the minimum SIP for HDFC Mid Cap Fund?
*Type: answer*

The minimum SIP amount for HDFC Mid Cap Fund is ₹100, as shown on its scheme page. The scheme FAQ says SIP and lump sum both need at least ₹100, and any additional purchase must also be at least ₹100.

Source: https://www.hdfcfund.com/explore/mutual-funds/hdfc-mid-cap-fund/direct
Last updated from sources: 2026-11-04

### 4. What is the expense ratio of HDFC Large Cap Fund?
*Type: answer*

The Total Expense Ratio (TER) shown on the HDFC Large Cap Fund Direct Plan page is 1.02%, including additional expenses and GST on management fees. The Regular Plan has its own page and figure, and TER can change, so check the linked page for the current number.

Source: https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-cap-fund/direct
Last updated from sources: 2026-11-04

### 5. What is the benchmark of HDFC Flexi Cap Fund?
*Type: answer*

HDFC Flexi Cap Fund is benchmarked against the NIFTY 500 Total Returns Index (TRI), as listed on its scheme page.

Source: https://www.hdfcfund.com/explore/mutual-funds/hdfc-flexi-cap-fund/direct
Last updated from sources: 2026-11-04

### 6. What is the riskometer level of HDFC ELSS Tax Saver?
*Type: answer*

The HDFC ELSS Tax Saver page shows its riskometer as Very High (product label: very high risk) and also displays a separate benchmark riskometer.

Source: https://www.hdfcfund.com/explore/mutual-funds/hdfc-elss-tax-saver-fund/direct
Last updated from sources: 2026-11-04

### 7. How do I download my capital gains statement?
*Type: answer*

A capital gain statement covers gains or losses on redeemed mutual fund units and can be requested from the registrars CAMS or KFintech, from your investment platform, from the AMC website, or as a consolidated account statement in capital-gains format via CAMS or NSDL. It is generally free and usually available after the financial year ends in March, so it can be used for ITR filing.

Source: https://www.hdfcfund.com/learn/blog/how-get-capital-gain-statement-mutual-fund-schemes-india
Last updated from sources: 2026-11-04

### 8. Should I buy HDFC Flexi Cap Fund?
*Type: refusal*

I can only share facts from official sources, so I can't advise whether to buy, sell, switch or hold any scheme. I can tell you facts such as a scheme's expense ratio, exit load, minimum SIP, lock-in, riskometer or benchmark. To learn how to approach investing, see SEBI's investor education page.

Source: https://investor.sebi.gov.in/securities-howtoinvest.html
Last updated from sources: 2026-11-04

### 9. What are the returns of HDFC Mid Cap Fund?
*Type: redirect*

I don't compute, quote or compare returns or NAVs because they change and need context. The official scheme page and monthly factsheet show performance data.

Source: https://www.hdfcfund.com/explore/mutual-funds/hdfc-mid-cap-fund/direct
Last updated from sources: 2026-11-04

### 10. (message withheld: contains personal details)
*Type: pii*

Please don't share personal details such as PAN, Aadhaar, account or folio numbers, OTPs, emails or phone numbers. I haven't kept your message, so please remove them and ask again. To stay safe from scams, see HDFC Mutual Fund's cyber safety guide.

Source: https://www.hdfcfund.com/information/cyber-security-awareness
Last updated from sources: 2026-11-04

## Known limits
- The corpus is a **hand-curated snapshot dated 2026-11-04**; fees such as TER and exit load change, so re-check before relying on it. Nothing is scraped at runtime.
- TER shown is from the Direct Plan page; the Regular Plan differs.
- The capital-gains statement answer cites an HDFC Mutual Fund guide whose URL contains `/learn/blog/`. It is published by the AMC itself (first-party), not a third-party blog.
- Sources marked `linked` (other KIM/SID PDFs, SEBI investor page, AMFI introduction page) were not opened during the build; please click them.
- KIM/SID PDFs are cited for "where is the document" questions but their text is not searched.
- The benchmark riskometer level is not captured (image only).
- The optional LLM layer is untested.
- Not covered: other AMCs/schemes, performance, tax advice, account-specific queries.
