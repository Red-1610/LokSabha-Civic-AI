"""
DemocracyOS — Test Suite
Run: python test_app.py
"""

import sys
import os
import re

PASS = "[OK]"
FAIL = "[FAIL]"
results = []


def check(name: str, condition: bool, detail: str = ""):
    icon = PASS if condition else FAIL
    print(f"  {icon}  {name}" + (f" - {detail}" if detail else ""))
    results.append((name, condition))


print("\nDemocracyOS Test Suite\n" + "-" * 40)

# ── 1. Imports ──────────────────────────────────────────────────────────────
print("\n[1] Dependency imports")

try:
    import requests
    check("requests import", True, requests.__version__)
except ImportError as e:
    check("requests import", False, str(e))

try:
    import streamlit
    check("streamlit import", True, streamlit.__version__)
except ImportError as e:
    check("streamlit import", False, str(e))

# ── 2. Syntax ────────────────────────────────────────────────────────────────
print("\n[2] Syntax check")
import py_compile
app_path = os.path.join(os.path.dirname(__file__), "app.py")
try:
    py_compile.compile(app_path, doraise=True)
    check("app.py compiles", True)
except py_compile.PyCompileError as e:
    check("app.py compiles", False, str(e))

# ── 3. Security ───────────────────────────────────────────────────────────────
print("\n[3] Security checks")
with open(app_path, encoding="utf-8") as f:
    src = f.read()

# Check no hardcoded API key patterns
hardcoded_google = re.search(r'AIza[0-9A-Za-z\-_]{35}', src)
check("No hardcoded Google API key", not hardcoded_google)

# Check sanitise function exists
check("sanitise() function defined", "def sanitise" in src)

# Check timeout in requests
check("requests.get uses timeout", "timeout=" in src)

# Check env var usage for keys
check("Uses os.getenv for API keys", "os.getenv" in src)

# ── 4. Accessibility ─────────────────────────────────────────────────────────
print("\n[4] Accessibility checks")
check("Skip link present", 'skip-link' in src)
check("aria-label attributes used", 'aria-label' in src)
check("role= attributes used", 'role="' in src)
check("aria-live region present", 'aria-live' in src)
check("sr-only class defined", 'sr-only' in src)

# ── 5. Google services ────────────────────────────────────────────────────────
print("\n[5] Google services")
check("Google Gemini integration", 'genai.GenerativeModel' in src)
check("Google Translate widget", 'google.translate.TranslateElement' in src)
check("Google Fonts imported", 'fonts.googleapis.com' in src)
check("translate_a script tag", 'translate_a/element.js' in src)

# ── 6. File sizes ─────────────────────────────────────────────────────────────
print("\n[6] Repository size")
total = 0
for fname in ["app.py", "requirements.txt", "README.md"]:
    fpath = os.path.join(os.path.dirname(__file__), fname)
    if os.path.exists(fpath):
        sz = os.path.getsize(fpath)
        total += sz
        check(f"{fname} size", True, f"{sz/1024:.1f} KB")

check("Total repo size < 1 MB", total < 1 * 1024 * 1024, f"{total/1024/1024:.2f} MB")

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n" + "-" * 40)
passed = sum(1 for _, ok in results if ok)
total_tests = len(results)
print(f"\n  Results: {passed}/{total_tests} passed\n")

if passed == total_tests:
    print("  SUCCESS: All tests passed!")
    sys.exit(0)
else:
    failed = [name for name, ok in results if not ok]
    print(f"  WARNING: Failed: {', '.join(failed)}")
    sys.exit(1)

