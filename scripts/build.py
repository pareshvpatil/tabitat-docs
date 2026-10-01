#!/usr/bin/env python3
"""Render the Tabitat site from this repo's Markdown.

    scripts/build.py

The privacy policy is generated from PRIVACY.md rather than kept as a second
copy, because the store listing, the extension and the published policy have to
agree and a hand-maintained duplicate is how they stop agreeing.

Output lands at the repository root, which is what GitHub Pages serves for a
repo whose only job is the site.

Handles the subset PRIVACY.md actually uses: headings, paragraphs, tables,
fenced code, and inline bold / code / links / autolinks.
"""
import html as H
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT
DOMAIN = 'tabitat.pareshpatil.in'
SUPPORT = 'support@pareshpatil.in'

# Google Search Console proves ownership by finding this tag on the site root.
# It lives here rather than in index.html because index.html is generated — a
# tag pasted into the output survives exactly until the next build, and the
# failure is silent: verification lapses and nobody notices.
GOOGLE_VERIFICATION = 'A4Yy-S7lsNlATF4fwgxRGWlkLEkgJgw2Vg_ZkQSCdvE'

STYLE = """
:root {
  color-scheme: light dark;
  --font: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --mono: ui-monospace, SFMono-Regular, Menlo, monospace;
  --brand: #0D9488; --brand-ink: #0B7F74; --brand-soft: rgba(13,148,136,.1);
  --ground: #F4F6F8; --surface: #FFFFFF; --text: #16232B; --dim: #5A6B75;
  --faint: #8A99A3; --edge: #E3E9ED;
}
@media (prefers-color-scheme: dark) {
  :root {
    --brand: #2DD4BF; --brand-ink: #5EEAD4; --brand-soft: rgba(45,212,191,.14);
    --ground: #12181C; --surface: #1B2329; --text: #E8EEF1; --dim: #9FB0BA;
    --faint: #7A8B96; --edge: #2A353D;
  }
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--ground); color: var(--text);
       font: 16px/1.65 var(--font); }
main { max-width: 760px; margin: 0 auto; padding: 32px 24px 72px; }
header.bar { border-bottom: 1px solid var(--edge); background: var(--surface); }
header.bar div { max-width: 760px; margin: 0 auto; padding: 14px 24px;
                 display: flex; align-items: center; gap: 10px; }
header.bar svg { width: 26px; height: 26px; }
header.bar b { font-size: 16px; font-weight: 650; letter-spacing: -.01em; }
header.bar nav { margin-left: auto; display: flex; gap: 14px; }
header.bar a { color: var(--dim); text-decoration: none; font-size: 14px; font-weight: 550; }
header.bar a:hover { color: var(--brand-ink); }
h1 { font-size: 28px; letter-spacing: -.02em; margin: 8px 0 4px; }
h2 { font-size: 13px; text-transform: uppercase; letter-spacing: .08em;
     color: var(--faint); margin: 36px 0 10px; }
h3 { font-size: 17px; margin: 28px 0 8px; }
p, li { color: var(--text); }
em.date { color: var(--dim); font-style: normal; font-size: 14px; }
a { color: var(--brand-ink); }
code { font: 13px var(--mono); background: var(--brand-soft); color: var(--brand-ink);
       padding: 1px 5px; border-radius: 5px; }
pre { background: var(--surface); border: 1px solid var(--edge); border-radius: 10px;
      padding: 14px 16px; overflow-x: auto; }
pre code { background: none; color: var(--text); padding: 0; }
table { border-collapse: collapse; width: 100%; margin: 14px 0; font-size: 15px;
        display: block; overflow-x: auto; }
th, td { text-align: left; padding: 9px 12px 9px 0; border-bottom: 1px solid var(--edge);
         vertical-align: top; }
th { color: var(--faint); font-weight: 650; font-size: 13px;
     text-transform: uppercase; letter-spacing: .05em; }
footer { border-top: 1px solid var(--edge); margin-top: 48px; padding-top: 18px;
         color: var(--faint); font-size: 14px; }
.lede { font-size: 18px; color: var(--dim); margin: 0 0 28px; }
.cta { display: inline-block; background: var(--brand); color: #fff; font-weight: 600;
       padding: 10px 18px; border-radius: 10px; text-decoration: none; margin-top: 8px; }
"""

MARK = """<svg viewBox="0 0 64 64" aria-hidden="true"><defs>
<linearGradient id="g" gradientUnits="userSpaceOnUse" x1="6.5" y1="9" x2="56.5" y2="55">
<stop offset="0" stop-color="#10B981"/><stop offset=".38" stop-color="#14B8A6"/>
<stop offset=".72" stop-color="#06B6D4"/><stop offset="1" stop-color="#38BDF8"/>
</linearGradient></defs>
<rect x="20.5" y="14" width="38" height="34" rx="10" fill="#38BDF8" opacity=".45"/>
<g fill="url(#g)"><path d="M13.5 28V13a4 4 0 0 1 8 0v15z"/><path d="M27.5 28V13a4 4 0 0 1 8 0v15z"/>
<rect x="5.5" y="23" width="38" height="32" rx="10"/></g></svg>"""


def inline(text):
    out = H.escape(text)
    out = re.sub(r'`([^`]+)`', lambda m: f'<code>{m.group(1)}</code>', out)
    out = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', out)
    # Single asterisks, after the double ones have been consumed. Requires a
    # non-space at each edge so a stray asterisk mid-sentence is left alone.
    out = re.sub(r'(?<!\w)\*(\S(?:[^*]*\S)?)\*(?!\w)', r'<em>\1</em>', out)
    out = re.sub(r'(?<!\w)_(\S(?:[^_]*\S)?)_(?!\w)', r'<em>\1</em>', out)
    out = re.sub(r'&lt;(https?://[^&]+)&gt;', r'<a href="\1">\1</a>', out)
    out = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', out)
    return out


def render(md):
    lines = md.splitlines()
    html, i = [], 0
    while i < len(lines):
        line = lines[i]

        if line.startswith('```'):
            i += 1
            block = []
            while i < len(lines) and not lines[i].startswith('```'):
                block.append(H.escape(lines[i])); i += 1
            i += 1
            html.append('<pre><code>' + '\n'.join(block) + '</code></pre>')
            continue

        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            html.append(f'<h{level}>{inline(line[level:].strip())}</h{level}>')
            i += 1
            continue

        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append(lines[i]); i += 1
            cells = [[c.strip() for c in r.strip('|').split('|')] for r in rows]
            body = [r for r in cells[1:] if not set(''.join(r)) <= set('-: ')]
            html.append('<table><thead><tr>'
                        + ''.join(f'<th>{inline(c)}</th>' for c in cells[0])
                        + '</tr></thead><tbody>'
                        + ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>'
                                  for r in body)
                        + '</tbody></table>')
            continue

        if not line.strip():
            i += 1
            continue

        para = []
        while i < len(lines) and lines[i].strip() and not lines[i][0] in '#|`':
            para.append(lines[i].strip()); i += 1
        text = ' '.join(para)
        cls = ' class="date"' if text.startswith('_Last updated') else ''
        if cls:
            html.append(f'<p><em{cls}>{inline(text.strip("_"))}</em></p>')
        else:
            html.append(f'<p>{inline(text)}</p>')
    return '\n'.join(html)


def page(title, body, nav_here, verify=False):
    nav = ''.join(
        f'<a href="{href}"{" style=\'color:var(--brand-ink)\'" if label == nav_here else ""}>{label}</a>'
        for label, href in (('Privacy', '/privacy/'),))
    verification = (f'\n<meta name="google-site-verification" content="{GOOGLE_VERIFICATION}" />'
                    if verify and GOOGLE_VERIFICATION else '')
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />{verification}
<title>{H.escape(title)}</title>
<style>{STYLE}</style></head>
<body>
<header class="bar"><div>{MARK}<b>Tabitat</b><nav>{nav}</nav></div></header>
<main>
{body}
<footer>&copy; 2026 Paresh V Patil &middot; <a href="mailto:{SUPPORT}">{SUPPORT}</a></footer>
</main></body></html>
"""


def main():
    (DOCS / 'privacy').mkdir(parents=True, exist_ok=True)
    (DOCS / 'CNAME').write_text(DOMAIN + '\n')
    (DOCS / '.nojekyll').write_text('')

    policy = render((ROOT / 'PRIVACY.md').read_text())
    (DOCS / 'privacy' / 'index.html').write_text(page('Tabitat — privacy policy', policy, 'Privacy'))

    landing = """<h1>Tabitat</h1>
<p class="lede">Automatic tab groups, and one tab per page.</p>
<p>Tabitat keeps a Chrome tab strip in order without you thinking about it. Tabs are grouped as
they open — by domain, or by rules that understand AWS accounts, Google document types and
Jira versus Confluence. Open a link to a page you already have open and the new tab stays while
the stale one closes. And a numbered switcher reaches any recent tab, or searches every open one,
in two keystrokes.</p>

<h2>What it does</h2>
<table><thead><tr><th>Feature</th><th>Detail</th></tr></thead><tbody>
<tr><td>AWS accounts</td><td>Console tabs separate by account, each in its own colour, so Production and Staging never share a group</td></tr>
<tr><td>Google Workspace</td><td>Tabs separate by document type rather than piling into one group</td></tr>
<tr><td>Jira and Confluence</td><td>One Atlassian site splits in two; two different sites never merge</td></tr>
<tr><td>Duplicate tabs</td><td>The new tab stays, the stale one closes — and pinned tabs, tabs playing audio and tabs holding unsaved input are never closed</td></tr>
<tr><td>Tab switcher</td><td>A numbered list of recent tabs, or type to search every open tab by title, URL or group</td></tr>
</tbody></table>

<h2>Privacy</h2>
<p><strong>No data collection.</strong> No analytics, no telemetry, no third-party code and no
server. The extension's content security policy blocks outbound connections at the browser level,
and every permission that could be sensitive is optional and off by default. The detail is in the
<a href="/privacy/">privacy policy</a>.</p>

<h2>Availability</h2>
<p>Coming to the Chrome Web Store.</p>

<h2>Support</h2>
<p>Questions, bug reports and feature requests: <a href="mailto:%s">%s</a></p>
""" % (SUPPORT, SUPPORT)
    (DOCS / 'index.html').write_text(page('Tabitat — automatic tab groups for Chrome', landing, None, verify=True))

    for name in ('CNAME', '.nojekyll', 'index.html', 'privacy/index.html'):
        f = DOCS / name
        print(f'  {name}  {f.stat().st_size:,} bytes')


if __name__ == '__main__':
    main()
