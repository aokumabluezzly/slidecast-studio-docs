"""Setup-page behavior shared by the Japanese and English finishing passes."""
from __future__ import annotations
import re


def finish_setup_html(html: str) -> str:
    # Finishers may run on an already finished page. Repair the old duplicate
    # declaration too, then insert exactly one copy before syncState runs.
    html = re.sub(r"(?m)^const initialHash=location\.hash;[ \t]*\n", "", html)
    anchor = "const chapters=[...document.querySelectorAll('.chapter')];"
    if html.count(anchor) != 1:
        raise ValueError("Setup page must contain one chapter initialization")
    html = html.replace(anchor, anchor + "\nconst initialHash=location.hash;", 1)
    html = html.replace("const openFromHash=()=>{", "const openFromHash=(hash=location.hash)=>{", 1)
    html = html.replace("decodeURIComponent(location.hash.slice(1))", "decodeURIComponent(hash.slice(1))", 1)
    html = html.replace("addEventListener('hashchange',openFromHash);", "addEventListener('hashchange',()=>openFromHash());", 1)
    html = html.replace("if(location.hash)requestAnimationFrame(openFromHash);", "if(initialHash)requestAnimationFrame(()=>openFromHash(initialHash));", 1)

    # Native grouping also keeps the sections exclusive if scripting is disabled.
    def group(match: re.Match[str]) -> str:
        attrs = re.sub(r'\s+name="[^"]*"', '', match.group(1))
        return '<details name="setup-chapters"' + attrs + '>'
    html = re.sub(r'<details\b([^>]*\bclass="chapter"[^>]*)>', group, html)
    return html
