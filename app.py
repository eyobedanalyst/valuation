import streamlit as st
import re

st.set_page_config(
    page_title="CSS Selector Grader",
    page_icon="🎨",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background-color: #0f0f13; color: #e8e8f0; }
.stApp { background-color: #0f0f13; }
.grader-header { text-align:center; padding:2rem 1rem 1.5rem; border-bottom:1px solid #2e2e42; margin-bottom:2rem; }
.grader-header h1 { font-family:'Space Mono',monospace; font-size:2rem; color:#7c6af7; margin-bottom:0.3rem; }
.grader-header p { color:#888899; font-size:0.95rem; }
.score-badge { display:inline-block; font-family:'Space Mono',monospace; font-size:3rem; font-weight:700; padding:1rem 2.5rem; border-radius:16px; margin:1rem 0; }
.score-2 { background:#0d2e1f; color:#3ecf8e; border:2px solid #3ecf8e; }
.score-1 { background:#2e1f0d; color:#f5a742; border:2px solid #f5a742; }
.score-0 { background:#2e0d0d; color:#f97066; border:2px solid #f97066; }
.feedback-card { background:#1a1a24; border:1px solid #2e2e42; border-radius:12px; padding:1.5rem; margin-top:1rem; line-height:1.7; }
.feedback-card h4 { font-family:'Space Mono',monospace; font-size:0.75rem; text-transform:uppercase; letter-spacing:2px; color:#888899; margin-bottom:0.75rem; }
.ref-tag { display:inline-block; background:#1e1a3a; color:#7c6af7; font-family:'Space Mono',monospace; font-size:0.7rem; padding:3px 10px; border-radius:20px; border:1px solid #7c6af7; margin-bottom:0.75rem; }
.stButton > button { background:#7c6af7 !important; color:white !important; border:none !important; border-radius:8px !important; font-family:'Space Mono',monospace !important; font-size:0.85rem !important; padding:0.6rem 1.8rem !important; width:100%; }
.stButton > button:hover { background:#6a58e0 !important; }
.stTextArea textarea { background:#1a1a24 !important; border:1px solid #2e2e42 !important; color:#e8e8f0 !important; font-family:'Space Mono',monospace !important; font-size:0.78rem !important; border-radius:8px !important; }
[data-testid="stFileUploader"] { background:#1a1a24 !important; border:1px dashed #2e2e42 !important; border-radius:10px !important; }
.stRadio label { color:#e8e8f0 !important; }
</style>
""", unsafe_allow_html=True)

REFERENCE_HTML = """<!DOCTYPE html>
<html><head><title>CSS Selectors Tutorial</title><style>
*{ margin:0; padding:0; box-sizing:border-box; font-family:Arial,Verdana,sans-serif; }
body{ background-color:#f1f1f1; line-height:1.5; }
#mainTitle{ color:white; text-align:center; text-transform:uppercase; letter-spacing:2px; }
header{ background-color:#333; padding:20px; }
h1,h2,h3{ font-weight:bold; }
nav ul{ text-align:center; margin-top:10px; }
nav ul li{ display:inline; margin:15px; }
nav ul li a{ color:white; text-decoration:none; }
.hero{ background-color:#007BFF; color:white; text-align:center; padding:40px; }
.container{ width:80%; margin:40px auto; }
.card{ background:white; margin:20px; padding:20px; border:1px solid #ccc; border-radius:10px; }
.card p{ color:#555; text-align:justify; }
.formSection{ background-color:#fff; padding:40px; margin:30px; border-radius:10px; }
input[type="text"],input[type="email"],input[type="password"],select{ width:100%; padding:10px; margin:10px 0; border:1px solid #aaa; border-radius:5px; }
button{ background-color:green; color:white; padding:10px; border:none; border-radius:5px; font-size:16px; }
footer{ text-align:center; padding:20px; background:#333; color:white; }
</style></head><body>
<header><h1 id="mainTitle">CSS Selectors Learning Website</h1>
<nav><ul><li><a href="#">Home</a></li><li><a href="#">Selectors</a></li><li><a href="#">Register</a></li></ul></nav></header>
<section class="hero"><h2>Welcome Students 👋</h2><p>This page teaches the most important CSS selectors with real examples.</p></section>
<section class="container"><h2>Types of CSS Selectors</h2>
<div class="card"><h3>1. Element Selector</h3><p>Targets HTML elements directly like h1, p, div.</p></div>
<div class="card"><h3>2. ID Selector</h3><p>Targets a unique element using #id.</p></div>
<div class="card"><h3>3. Class Selector</h3><p>Targets multiple elements using .class.</p></div>
<div class="card"><h3>4. Universal Selector</h3><p>Targets ALL elements using *.</p></div>
<div class="card"><h3>5. Group Selector</h3><p>Styles multiple elements together.</p></div>
<div class="card"><h3>6. Attribute Selector</h3><p>Targets elements based on attributes.</p></div>
<div class="card"><h3>7. Descendant Selector</h3><p>Targets elements inside other elements.</p></div></section>
<section class="formSection"><h2>Student Registration Form</h2><form>
<label>Full Name</label><input type="text" placeholder="Enter your name" required>
<label>Email</label><input type="email" placeholder="Enter your email" required>
<label>Password</label><input type="password" required>
<label>Gender</label><input type="radio" name="gender"> Male <input type="radio" name="gender"> Female
<label>Courses</label><input type="checkbox"> HTML <input type="checkbox"> CSS <input type="checkbox"> JavaScript
<label>Country</label><select><option>Ethiopia</option><option>Kenya</option><option>USA</option></select>
<button type="submit">Register</button></form></section>
<footer><p>© 2026 CSS Learning Project</p></footer>
</body></html>"""


def extract_css(html):
    matches = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL | re.IGNORECASE)
    return " ".join(matches)


def check_selectors(css):
    results = {}

    m = re.search(r'\b(body|header|footer|nav|section|h[1-6]|p|div|ul|li|a|input|button|form|select|label)\s*\{', css)
    results["1️⃣ Element Selector"] = (bool(m), f"`{m.group().strip()}`" if m else "Not found — e.g. `body {}` or `footer {}`")

    m = re.search(r'#[a-zA-Z][\w-]*\s*\{', css)
    results["2️⃣ ID Selector"] = (bool(m), f"`{m.group().strip()}`" if m else "Not found — e.g. `#mainTitle {}`")

    m = re.search(r'\.[a-zA-Z][\w-]*\s*\{', css)
    results["3️⃣ Class Selector"] = (bool(m), f"`{m.group().strip()}`" if m else "Not found — e.g. `.hero {}`")

    m = re.search(r'\*\s*\{', css)
    results["4️⃣ Universal Selector"] = (bool(m), "`* {}`" if m else "Not found — add `* { margin:0; padding:0; }`")

    m = re.search(r'[^{},]+,[^{},]+\{', css)
    results["5️⃣ Group Selector"] = (bool(m), f"`{m.group()[:35].strip()}...`" if m else "Not found — e.g. `h1, h2, h3 {}`")

    m = re.search(r'\w[\w-]*\s*\[[\w\-\"\'=~|^$*\s]+\]\s*\{', css)
    results["6️⃣ Attribute Selector"] = (bool(m), f"`{m.group().strip()}`" if m else 'Not found — e.g. `input[type="text"] {}`')

    m = re.search(r'[.#]?[a-zA-Z][\w-]*\s+[a-zA-Z][\w-]*\s*\{', css)
    results["7️⃣ Descendant Selector"] = (bool(m), f"`{m.group().strip()}`" if m else "Not found — e.g. `.card p {}`")

    return results


def check_structure(html):
    hl = html.lower()
    return {
        "Dark header":       bool(re.search(r'<header', hl)),
        "Nav links":         bool(re.search(r'<nav', hl)),
        "Hero section":      bool(re.search(r'class=["\'][^"\']*hero', hl)),
        "Selector cards":    hl.count('card') >= 3,
        "Registration form": bool(re.search(r'<form', hl)),
        "Footer":            bool(re.search(r'<footer', hl)),
    }


def compute_score(sel_results, struct_checks):
    found = sum(1 for v, _ in sel_results.values() if v)
    missing = [k for k, (v, _) in sel_results.items() if not v]
    structs = sum(struct_checks.values())

    if found == 7 and structs >= 5:
        score = 2
        fb = (f"Excellent work! All 7 CSS selector types are correctly used and the page "
              f"structure closely matches the reference ({structs}/6 sections present). "
              "Your CSS is well-organised and shows strong understanding of selectors.")
        rec = "Great job! Challenge yourself next with CSS pseudo-classes like :hover and :nth-child, and combinators like >, +, and ~."
    elif found >= 5 and structs >= 3:
        score = 1
        miss_str = ", ".join(m.split(" ", 1)[1] for m in missing) if missing else "none"
        fb = (f"Good effort! You used {found}/7 selector types and included {structs}/6 required page sections. "
              f"Missing selectors: {miss_str}.")
        rec = f"Add the missing selectors ({miss_str}) and make sure your layout includes all sections from the reference."
    else:
        score = 0
        fb = (f"This submission needs more work. Only {found}/7 CSS selectors were found "
              f"and only {structs}/6 page sections match the reference.")
        rec = ("Re-read the assignment. Your file must include all 7 selector types: "
               "Element, ID, Class, Universal, Group, Attribute, and Descendant.")

    return score, fb, rec


# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="grader-header">
    <h1>🎨 CSS Selector Grader</h1>
    <p>Automated marking tool — no API key required</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<span class="ref-tag">📋 REFERENCE OUTPUT</span>', unsafe_allow_html=True)
    st.caption("This is what the student's page should look like:")
    st.components.v1.html(REFERENCE_HTML, height=500, scrolling=True)

with right:
    st.markdown("**Submit student work**")
    method = st.radio("Input", ["📂 Upload .html file", "📝 Paste HTML code"],
                      horizontal=True, label_visibility="collapsed")
    student_html = ""

    if method == "📂 Upload .html file":
        up = st.file_uploader("Drop file", type=["html", "htm"], label_visibility="collapsed")
        if up:
            student_html = up.read().decode("utf-8", errors="ignore")
            st.success(f"✅ Loaded: `{up.name}`")
            with st.expander("Preview student output"):
                st.components.v1.html(student_html, height=380, scrolling=True)
    else:
        student_html = st.text_area("Paste HTML", height=280,
                                    placeholder="<!DOCTYPE html>\n<html>\n...",
                                    label_visibility="collapsed")

    st.markdown("")
    grade_btn = st.button("⚡  Grade Submission")

if grade_btn:
    if not student_html.strip():
        st.warning("⚠️ Please upload or paste the student's HTML first.")
    else:
        css = extract_css(student_html)
        sel  = check_selectors(css)
        struct = check_structure(student_html)
        score, feedback, recommendation = compute_score(sel, struct)

        st.markdown("---")
        col_score, col_detail = st.columns([1, 2], gap="large")

        with col_score:
            emoji = "🏆" if score == 2 else ("⚠️" if score == 1 else "❌")
            label = "Full marks!" if score == 2 else ("Partial credit" if score == 1 else "Needs improvement")
            st.markdown(f"""
<div style="text-align:center;padding:1rem;">
  <div style="font-family:'Space Mono',monospace;font-size:0.7rem;letter-spacing:2px;color:#888899;text-transform:uppercase;margin-bottom:0.5rem;">Final Score</div>
  <div class="score-badge score-{score}">{emoji} {score}/2</div>
  <div style="color:#888899;font-size:0.85rem;margin-top:0.5rem;">{label}</div>
</div>""", unsafe_allow_html=True)

            st.markdown("**CSS Selectors**")
            for name, (found, detail) in sel.items():
                icon = "✅" if found else "❌"
                st.markdown(f"{icon} {name}")
                if not found:
                    st.caption(f"  ↳ {detail}")

            st.markdown("**Page structure**")
            for section, present in struct.items():
                st.markdown(f"{'✅' if present else '❌'} {section}")

        with col_detail:
            st.markdown(f"""
<div class="feedback-card">
  <h4>📝 Feedback</h4>
  {feedback}
</div>
<div class="feedback-card" style="margin-top:0.75rem;border-color:#3a2e4a;">
  <h4>🚀 Recommendation</h4>
  {recommendation}
</div>""", unsafe_allow_html=True)