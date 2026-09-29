# tabitat-docs

The public site for [Tabitat](https://tabitat.pareshpatil.in), a Chrome extension that groups tabs
automatically and closes duplicates. This repository exists only to serve that site — the
extension's own source is private.

It is public for one reason: **GitHub Pages does not serve private repositories on the Free plan.**
Splitting the site out keeps the extension source closed while the privacy policy stays reachable
at a stable URL, which the Chrome Web Store requires of every listing.

## What is here

| | |
|---|---|
| `PRIVACY.md` | The privacy policy. **The only file to edit** |
| `scripts/build.py` | Renders the site from it |
| `index.html`, `privacy/index.html` | Generated. Do not edit by hand |
| `CNAME` | The custom domain, `tabitat.pareshpatil.in` |
| `.nojekyll` | Serve the files as they are; no Jekyll processing |

## Changing the policy

```bash
./scripts/build.py && git add -A && git commit -m "update privacy policy" && git push
```

Pages redeploys within a minute of the push. The policy is generated rather than written twice
because the published policy, the extension's behaviour and the disclosures in the Web Store
dashboard all have to agree, and a hand-maintained copy is how they stop agreeing.

## Pages setup

Settings → Pages → Source: **Deploy from a branch**, branch `main`, folder **`/` (root)**, then set
the custom domain to `tabitat.pareshpatil.in` and enable Enforce HTTPS once the certificate issues.

The DNS record already exists: a `CNAME` for `tabitat` pointing at `pareshvpatil.github.io.` in
GoDaddy. It does not need changing — but the **custom domain must be released by the `tabitat`
repository first**, because GitHub allows one repository to claim a given domain at a time.
