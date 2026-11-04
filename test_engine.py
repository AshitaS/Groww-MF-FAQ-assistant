import unittest

from corpus_data import CHUNKS, SCHEMES, SOURCES
from engine import answer, count_sentences


def a(q):
    return answer(q, use_llm=False)


class Facts(unittest.TestCase):
    def test_elss_lock_in(self):
        r = a("What is the ELSS lock-in?")
        self.assertEqual(r.kind, "answer"); self.assertIn("3 years", r.text)
        self.assertEqual(r.link, SCHEMES["elss"]["page"])

    def test_exit_load_flexi(self):
        r = a("Exit load of HDFC Flexi Cap Fund?")
        self.assertEqual(r.kind, "answer"); self.assertIn("1.00%", r.text); self.assertIn("1 year", r.text)

    def test_exit_load_elss_nil(self):
        r = a("exit load for hdfc elss tax saver")
        self.assertIn("NIL", r.text)

    def test_min_sip_each(self):
        exp = {"large cap": "₹100", "flexi cap": "₹100", "mid cap": "₹100", "elss tax saver": "₹500"}
        for name, amt in exp.items():
            r = a(f"What is the minimum SIP for HDFC {name}?")
            self.assertEqual(r.kind, "answer", name); self.assertIn(amt, r.text, name)

    def test_expense_ratio(self):
        r = a("Expense ratio of HDFC Mid Cap Fund?")
        self.assertIn("0.74%", r.text); self.assertEqual(r.link, SCHEMES["mid"]["page"])

    def test_riskometer_and_benchmark(self):
        self.assertIn("Very High", a("Riskometer of HDFC Large Cap Fund").text)
        self.assertIn("NIFTY 100", a("Benchmark of HDFC Large Cap Fund").text)
        self.assertIn("NIFTY 500", a("What benchmark does the flexi cap fund use?").text)

    def test_scheme_isolation(self):
        r = a("expense ratio of flexi cap")
        self.assertNotIn("1.02%", r.text); self.assertNotIn("0.74%", r.text)

    def test_statements(self):
        self.assertIn("capital gain", a("How to download capital gains statement?").text.lower())
        self.assertIn("statement", a("How do I download my account statement?").text.lower())

    def test_missing_scheme_asks(self):
        self.assertEqual(a("What is the exit load?").kind, "clarify")
        self.assertEqual(a("minimum SIP?").kind, "clarify")

    def test_definitions(self):
        self.assertEqual(a("What is a risk-o-meter?").kind, "answer")
        self.assertIn("six", a("What is a riskometer?").text)
        self.assertIn("AMFI", a("What is an expense ratio?").text)


class Refusals(unittest.TestCase):
    def test_advice(self):
        for q in ["Should I buy HDFC Flexi Cap Fund?", "Which is better, large cap or mid cap?",
                  "Is it a good time to invest in ELSS?", "Should I sell my mid cap fund now",
                  "Recommend a fund for me", "Is HDFC ELSS safe to invest?"]:
            r = a(q); self.assertEqual(r.kind, "refusal", q); self.assertIn("sebi.gov.in", r.link)

    def test_performance(self):
        for q in ["What are the returns of HDFC Flexi Cap?", "Which fund has the best CAGR?", "NAV of mid cap fund today"]:
            r = a(q); self.assertEqual(r.kind, "redirect", q)
        self.assertEqual(a("returns of flexi cap fund").link, SCHEMES["flexi"]["page"])

    def test_pii(self):
        for q in ["My PAN is ABCDE1234F, send statement", "aadhaar 1234 5678 9012", "mail me at a.b@gmail.com",
                  "call 9876543210", "my OTP is 482913", "account 123456789012", "folio number 1234567"]:
            r = a(q); self.assertEqual(r.kind, "pii", q); self.assertNotIn("ABCDE", r.text)

    def test_out_of_scope(self):
        self.assertEqual(a("Expense ratio of SBI Bluechip Fund").kind, "out_of_scope")
        self.assertEqual(a("HDFC Small Cap exit load").kind, "out_of_scope")


class Format(unittest.TestCase):
    QS = ["ELSS lock-in?", "exit load flexi cap", "min sip large cap", "expense ratio mid cap", "riskometer elss",
          "benchmark mid cap", "capital gains statement", "download account statement", "KIM of large cap fund",
          "SID of elss", "what is sip", "factsheet", "entry load", "Should I buy?", "returns?", "xyz"]

    def test_every_answer_has_one_link_and_le3_sentences(self):
        for q in self.QS:
            r = a(q)
            self.assertLessEqual(count_sentences(r.text), 3, q)
            self.assertTrue(r.link.startswith("https://"), q)
            self.assertEqual(r.render().count("http"), 1, q)
            self.assertIn("Last updated from sources:", r.render())

    def test_corpus_size(self):
        self.assertTrue(15 <= len(SOURCES) <= 25)
        urls = [s[3] for s in SOURCES]
        self.assertEqual(len(urls), len(set(urls)))
        for c in CHUNKS:
            self.assertIn(c["url"], urls, c["id"])  # every citation is in the source list


if __name__ == "__main__":
    unittest.main(verbosity=1)


class Regressions(unittest.TestCase):
    def test_download_kim_is_not_statement(self):
        r = answer("How to download the KIM of large cap fund?", use_llm=False)
        self.assertIn("KIM", r.text); self.assertIn("Large Cap", r.text); self.assertIn("KIM", r.link)

    def test_min_sip_without_scheme_clarifies(self):
        self.assertEqual(answer("What is the minimum SIP amount?", use_llm=False).kind, "clarify")

    def test_benchmark_total_return_not_redirected(self):
        self.assertEqual(answer("What is the benchmark total return index of mid cap?", use_llm=False).kind, "answer")

    def test_scheme_only_asks_which_fact(self):
        self.assertEqual(answer("Tell me about HDFC Flexi Cap", use_llm=False).kind, "clarify")
