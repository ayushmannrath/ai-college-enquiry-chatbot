"""Run on your own machine: prints a test-query table and accuracy.
Usage: python evaluate.py   (needs the project requirements installed)"""
from nlp_model import CollegeEnquiryChatbot

CASES = [  # (user query, expected category)
    ("What are the eligibility criteria?", "Admissions"),
    ("How do I apply online?", "Admissions"),
    ("Which documents do I need to submit?", "Admissions"),
    ("What courses do you offer?", "Courses"),
    ("How much is the tuition fee?", "Fees"),
    ("Can I pay fees in installments?", "Fees"),
    ("Do you give scholarships?", "Scholarships"),
    ("What is the placement percentage?", "Placements"),
    ("Tell me about hostel facilities", "Facilities"),
    ("Is there a library?", "Facilities"),
    ("xyzabc random nonsense", None),
    ("Who won the cricket world cup?", None),
]
bot = CollegeEnquiryChatbot("college_faq_dataset.csv")
ok = 0
print(f"{'Query':45} {'Expected':13} {'Got':13} {'Conf':>6}  Result")
for q, exp in CASES:
    r = bot.get_response(q)
    got = None if r["is_fallback"] else r["category"]
    good = got == exp
    ok += good
    print(f"{q:45} {str(exp):13} {str(got):13} {r['confidence']:6.1%}  {'PASS' if good else 'FAIL'}")
print(f"\nAccuracy: {ok}/{len(CASES)} = {ok/len(CASES):.0%}")
