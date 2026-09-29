# Tabitat privacy policy

_Last updated: 25 September 2026_

**Tabitat collects no data unless you switch it on.** There is no crash reporting, no
advertising, no third-party code and no tracking of any kind. The one optional exception is
anonymous usage statistics, described below: it is off by default, and turning it on takes a
deliberate action plus a permission grant.

## What Tabitat reads

To group tabs and close duplicates, Tabitat reads the **URL, title and tab-group membership** of
your open tabs. This happens entirely inside your browser, in memory, for as long as it takes to
decide which group a tab belongs to or whether it duplicates another tab.

If you switch on **"Never close a tab with unsaved form input"** and grant site access, a small
script watches for typing on pages you visit. It reports exactly one true/false signal per frame —
*"this frame has unsaved input"*. It never reads, stores or transmits what you typed.

If you switch on **AWS account grouping** and grant cookie access, Tabitat reads the `aws-userInfo`
cookie on `aws.amazon.com` to learn which AWS account a console tab belongs to. The cookie is
parsed locally and never leaves your browser.

## What Tabitat stores

All storage is Chrome's local extension storage, on your own machine:

| Stored | Where | Contains |
|---|---|---|
| Your settings | `chrome.storage.local` | The toggles and lists you set on the options page |
| Recently-closed duplicates | `chrome.storage.local` | Up to 20 URLs, so the popup can offer "Reopen". Turn the setting off and nothing is recorded; "Clear the reopen list" erases it |
| Recent tab order | `chrome.storage.session` | Tab **ids** only, never URLs. Cleared when you close the browser |
| Unsaved-input flags | `chrome.storage.session` | Tab and frame ids only. Cleared when you close the browser |
| Statistics opt-in | `chrome.storage.local` | Whether you opted in, and the random install id. Deleted when you opt out |

Uninstalling Tabitat deletes all of it. None of it is synced, backed up, or readable by anyone
but you.

## Anonymous usage statistics (optional, off by default)

If you tick **"Help improve Tabitat with anonymous usage statistics"** on the options page and
grant the permission Chrome then asks for, Tabitat sends a small event to Google Analytics when
you use a feature. It sends **only** the events in this table, and only the values listed:

| Event | Carries |
|---|---|
| `switcher_opened` | Whether it was opened by shortcut or toolbar |
| `switcher_search` | How many tabs matched, rounded to a band: `0`, `1`, `2-4`, `5-9`, `10+` |
| `tab_switched` | Whether you picked with a digit, enter, a click, or the previous-tab shortcut |
| `duplicate_closed` | Your match mode (`smart` / `strict` / `path`), and whether a tab closed or you were switched to one |
| `group_created` | Which rule fired: `aws`, `google`, `atlassian`, `domain` or `subdomain` |

It **never** sends a URL, a hostname, a page or tab title, an AWS account id or alias, anything
you type into the search box, or anything from a form. This is enforced in code, not by
convention: `lib/analytics.js` defines the complete set of events and permitted values, and
anything not on that list is discarded before a request is built. `test/analytics.test.mjs`
proves it, including the case where a URL is passed by mistake.

A random identifier, generated on your machine with `crypto.randomUUID()`, distinguishes one
install from another so that ten events from you are not counted as ten users. It is tied to
nothing about you, your Google account, or your device. **Switching the setting off deletes it**
and revokes the permission — it does not merely stop sending.

If this build ships without a configured analytics endpoint, the setting is inert and nothing is
sent whether it is on or off; the options page says so when that is the case.

## Network requests

Tabitat makes exactly one request that looks like network I/O:

```
chrome-extension://<your-install-id>/_favicon/?pageUrl=…
```

This is the extension's **own origin**, serving Chrome's local favicon cache through the `favicon`
permission. It is used to pick a group colour that matches the site. It does not leave your
machine.

The extension's content security policy is `connect-src 'self' https://www.google-analytics.com`.
Those are the only two destinations the browser will permit — everything else is blocked at the
browser level, not as a promise but as an enforced rule. The Google Analytics origin is reachable
only after you opt in, because the host permission for it is optional and requested at that
moment.

## Permissions, and why each exists

| Permission | Why |
|---|---|
| `tabs` | Read tab URLs and titles to decide grouping and detect duplicates |
| `tabGroups` | Create, name, colour and collapse Chrome tab groups |
| `storage` | Save your settings and the recent-tab order on this machine |
| `favicon` | Read Chrome's local favicon cache to choose a group colour |
| `scripting` | Register the unsaved-input watcher, only after you enable it |
| `cookies` (optional) | Read the AWS console session cookie, only if you enable AWS grouping and grant it |
| Site access (optional) | Run the unsaved-input watcher, only if you enable that setting and grant it |
| `www.google-analytics.com` (optional) | Send the anonymous events above, only if you opt in |

Every optional permission is off by default, requested at the moment you turn its feature on, and
revocable from the options page or `chrome://extensions`.

## Changes

Any change to this policy will be published in this file, with the date above updated, before the
version that relies on it ships.

## Contact

Email <support@pareshpatil.in>.
