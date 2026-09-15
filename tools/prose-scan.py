#!/usr/bin/env python3
"""flag language-profile violations in the site's prose.

usage: tools/prose-scan.py $(find . -name '*.html' -not -path './.git/*')

strips <pre>/<code>/<style>/<script> and all tags, then flags semicolons, colons,
em dashes, contractions and banned vocabulary. colons directly before a code
block or a list are tolerated by the profile, everything else is a hit.
"""
import html, re, sys

BANNED = re.compile(
    r"\b(delve|leverage|utilize|foster|facilitate|navigate|crucial|pivotal|robust|"
    r"comprehensive|innovative|holistic|seamless|cutting-edge|dynamic|landscape|"
    r"ecosystem|framework|paradigm|synergy|tapestry|testament|moreover|furthermore|"
    r"deliberate\w*|exciting|incredible|fascinating)\b", re.I)
CONTRACTION = re.compile(r"\b\w+'(t|re|ve|ll|d|m)\b")

for path in sys.argv[1:]:
    src = open(path).read()
    text = re.sub(r"<(pre|code|style|script)\b.*?</\1>", "", src, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    for lineno, line in enumerate(text.split("\n"), 1):
        t = line.strip()
        if not t:
            continue
        hits = []
        if ";" in t:
            hits.append("semicolon")
        if re.search(r":\s", t) or t.endswith(":"):
            hits.append("colon")
        if "—" in t:
            hits.append("emdash")
        words = BANNED.findall(t)
        if words:
            hits.append("word:" + ",".join(words))
        if CONTRACTION.search(t):
            hits.append("contraction")
        if hits:
            print(f"{path}:{lineno}: [{' '.join(hits)}] {t[:110]}")
