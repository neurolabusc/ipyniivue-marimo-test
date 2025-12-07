#!/usr/bin/env python3
"""
Minimal build_all.py (fixed)

- Exports all marimo.*.py files to dist/<shortname> using `uv run marimo -y export html-wasm`.
- Injects a resilient fixed top nav (Previous / Chooser / Next) into each exported index.html.
- Writes a small top-level dist/index.html chooser.

Run from the folder containing your marimo.*.py files.
"""
from pathlib import Path
import subprocess, sys, re, html

UV_CMD_BASE = ["uv", "run", "marimo", "-y", "export", "html-wasm"]
DIST = Path("dist")
GLOB = "marimo.*.py"
MARKER = "<!-- MARIMO_NAV_INJECTED -->"

NAV_OUTER = (
    '<div id="marimo-top-nav" '
    'style="position:fixed;left:0;right:0;top:0;z-index:2147483646;'
    'background:linear-gradient(90deg,#0b1220,#07101a);color:#fff;'
    'padding:4px 6px;font-family:system-ui,Arial;font-size:12px;line-height:1;'
    'display:flex;align-items:center;gap:6px;box-shadow:0 1px 3px rgba(0,0,0,0.12);">'
    '<div style="font-weight:700;font-size:0.95em;margin-right:8px;">niivue examples</div>'
    '<div style="font-size:0.85em;color:#d6d9de;">Demo: <strong style="font-weight:700">{title}</strong></div>'
    '<div style="margin-left:auto;display:flex;gap:6px;align-items:center;">'
    '<a id="marimo-nav-prev" href="{prev}" style="color:#111;background:#ffd86b;padding:4px 6px;border-radius:4px;text-decoration:none;font-weight:600;font-size:0.85em;">← Prev</a>'
    '<a id="marimo-nav-chooser" href="../" style="color:#fff;background:#666;padding:4px 6px;border-radius:4px;text-decoration:none;font-weight:600;font-size:0.85em;">Index</a>'
    '<a id="marimo-nav-next" href="{next}" style="color:#fff;background:#0a7;padding:4px 6px;border-radius:4px;text-decoration:none;font-weight:600;font-size:0.85em;">Next →</a>'
    '</div></div>'
)



NAV_SCRIPT = r'''
<script id="marimo-top-nav-script">
(function(){
  const NAV_ID = "marimo-top-nav";
  const navHtml = NAV_HTML_PLACEHOLDER; // backtick literal

  function makeNode() {
    const tmp = document.createElement('div');
    tmp.innerHTML = navHtml;
    return tmp.firstElementChild;
  }

  function ensureStyleVar() {
    // create style element that provides --marimo-top-offset and ensures body respects it
    if (!document.getElementById("marimo-nav-style")) {
      const st = document.createElement('style');
      st.id = "marimo-nav-style";
      // default offset variable; pages will use it via padding-top assigned below
      st.textContent = ':root{--marimo-top-offset:44px;}';
      document.head.appendChild(st);
    }
  }

  function applyOffset(h) {
    // apply padding using the computed height so page content is not hidden under the fixed nav
    try {
      const px = Math.ceil(h);
      // prefer setting padding on known containers, fallback to body/documentElement
      const targets = [document.querySelector('#root'), document.querySelector('main'), document.body];
      let applied = false;
      for (const t of targets) {
        if (t) {
          t.style.boxSizing = 'border-box';
          // only increase padding if new value is larger
          const prev = parseInt(t.style.paddingTop || 0, 10) || 0;
          if (prev < px) t.style.paddingTop = px + 'px';
          applied = true;
        }
      }
      // always set the css var as a reliable reference
      document.documentElement.style.setProperty('--marimo-top-offset', px + 'px');
      if (!applied && document.body) {
        document.body.style.boxSizing = 'border-box';
        document.body.style.paddingTop = px + 'px';
      }
    } catch (e) { console.warn(e); }
  }

  function insertNavAtHtmlRoot() {
    try {
      if (document.getElementById(NAV_ID)) return true;
      const node = makeNode();
      if (!node) return false;
      // Insert before body so node is a child of <html> (documentElement)
      const htmlEl = document.documentElement;
      const body = document.body;
      if (body) {
        htmlEl.insertBefore(node, body);
      } else {
        htmlEl.insertBefore(node, htmlEl.firstChild);
      }
      return true;
    } catch (e) {
      console.warn("insertNavAtHtmlRoot failed", e);
      return false;
    }
  }

  function recomputeAndApply() {
    const nav = document.getElementById(NAV_ID);
    if (!nav) return;
    const h = Math.max(48, Math.ceil(nav.getBoundingClientRect().height));
    ensureStyleVar();
    applyOffset(h);
  }

  function ensureNav() {
    // Try quick insert; then compute offsets
    const ok = insertNavAtHtmlRoot();
    if (ok) recomputeAndApply();
    return ok;
  }

  // Observe documentElement child changes to detect body replacement or nav removal
  function observeRoot() {
    if (window.__marimo_nav_root_obs) return;
    try {
      const obs = new MutationObserver((mutations) => {
        if (!document.getElementById(NAV_ID)) {
          ensureNav();
        } else {
          // if nav exists, recompute height in case layout changed
          recomputeAndApply();
        }
      });
      obs.observe(document.documentElement, { childList: true, subtree: false });
      window.__marimo_nav_root_obs = obs;
    } catch (e) { /* ignore */ }
  }

  // Also watch for size changes that would affect height (window resize)
  window.addEventListener('resize', () => setTimeout(recomputeAndApply, 80));

  function boot() {
    ensureNav();
    // retries to catch late mounts
    setTimeout(ensureNav, 200);
    setTimeout(ensureNav, 700);
    setTimeout(ensureNav, 1500);
    observeRoot();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
</script>
'''


# --- FIXED chooser template: double the braces so .format() won't interpret CSS {} ---
CHOOSER_TEMPLATE = """<!doctype html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>niivue examples</title>
<style>body {{font-family:system-ui,Arial;padding:2rem}} .card {{border:1px solid #ddd;padding:1rem;border-radius:8px;margin-bottom:1rem}} a.btn {{background:#0366d6;color:#fff;padding:.5rem .8rem;border-radius:6px;text-decoration:none}}</style>
</head><body><h1><a href="https://github.com/neurolabusc/ipyniivue-marimo-test" style="text-decoration:none; color:inherit;">niivue examples</a></h1>{cards}</body></html>
"""

def shortname(p: Path):
    s = p.stem
    return s.split(".",1)[1] if "." in s else s

def run_export(src: Path, outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    cmd = UV_CMD_BASE + [str(src), "-o", str(outdir)]
    print("EXPORT:", " ".join(cmd))
    subprocess.run(cmd, check=True)

def inject_resilient(index_html: Path, title: str, prev_rel: str, next_rel: str):
    if not index_html.exists():
        print("skip inject, missing:", index_html)
        return
    txt = index_html.read_text(encoding="utf-8")
    if MARKER in txt:
        print("nav already present in", index_html)
        return

    nav_html = NAV_OUTER.format(title=html.escape(title),
                                prev=html.escape(prev_rel),
                                next=html.escape(next_rel))
    nav_js_literal = "`" + nav_html.replace("`", "\\`") + "`"
    script = NAV_SCRIPT.replace("NAV_HTML_PLACEHOLDER", nav_js_literal)

    head_m = re.search(r'(<head[^>]*>)', txt, flags=re.IGNORECASE)
    body_m = re.search(r'(<body[^>]*>)', txt, flags=re.IGNORECASE)

    if not body_m:
        print("no <body> found in", index_html, " — skipping injection")
        return

    # Insert a static nav into the file's body so user sees it during initial load.
    insert_at_body = body_m.end()
    newtxt = txt[:insert_at_body] + "\n" + nav_html + "\n" + MARKER + "\n" + txt[insert_at_body:]

    # Insert the resilience/fix script into head if present; otherwise place it before body tag
    if head_m:
        insert_at_head = head_m.end()
        newtxt = newtxt[:insert_at_head] + "\n" + script + "\n" + newtxt[insert_at_head:]
    else:
        newtxt = newtxt[:body_m.start()] + script + "\n" + newtxt[body_m.start():]

    index_html.write_text(newtxt, encoding="utf-8")
    print("injected fixed-nav+script into", index_html)


def make_chooser(dist: Path, names):
    cards = []
    for n in names:
        cards.append(f'<div class="card"><h2>{html.escape(n)}</h2><p><a class="btn" href="./{n}/">Open {html.escape(n)}</a></p></div>')
    dist.mkdir(parents=True, exist_ok=True)
    (dist / "index.html").write_text(CHOOSER_TEMPLATE.format(cards="\n".join(cards)), encoding="utf-8")
    print("wrote chooser at", dist / "index.html")

def main():
    cwd = Path(".").resolve()
    files = sorted(cwd.glob(GLOB))
    if not files:
        print("No files matching", GLOB); sys.exit(1)
    items = [(p, shortname(p)) for p in files]
    DIST.mkdir(parents=True, exist_ok=True)
    for src, short in items:
        out = DIST / short
        run_export(src, out)
    names = [short for _, short in items]
    n = len(names)
    for i, name in enumerate(names):
        prev_name = names[(i-1) % n]
        next_name = names[(i+1) % n]
        idx = DIST / name / "index.html"
        prev_rel = f"../{prev_name}/"
        next_rel = f"../{next_name}/"
        inject_resilient(idx, title=name, prev_rel=prev_rel, next_rel=next_rel)
    make_chooser(DIST, names)
    print("done. serve with: python -m http.server --directory dist 8000")

if __name__ == "__main__":
    main()
