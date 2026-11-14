# Free Proxy List: HTTP & HTTPS, tested every minute

![Updated every minute](https://img.shields.io/badge/updated-every%20minute-brightgreen)
![Format](https://img.shields.io/badge/format-txt%20%7C%20json-blue)

A free list of working HTTP and HTTPS proxies. Every proxy here passed a live HTTPS test on
[solproxy.net](https://solproxy.net/free-proxy-list) in the last check, and dead ones are dropped.
This repository is refreshed **every minute**, sorted fastest first.

<!-- stats -->
**Last update:** 2026-11-14 18:04 UTC  
**Working proxies:** 1128 (297 residential, 821 datacenter, 10 mobile)  
**Top countries:** US 345, DE 112, FR 56, RO 47, NL 42, GB 39, IN 38, LV 35, LT 30, CA 29
<!-- /stats -->

## Download

All files are plain text, one proxy per line, sorted by latency (fastest first).

| File | Contents | Link |
| --- | --- | --- |
| `http.txt` | HTTP proxies, `ip:port` | [raw](https://raw.githubusercontent.com/solproxy/sol-free-proxy-list/main/http.txt) |
| `https.txt` | Proxies that speak TLS, `ip:port` | [raw](https://raw.githubusercontent.com/solproxy/sol-free-proxy-list/main/https.txt) |
| `all.txt` | Everything, with scheme (`http://` / `https://`) | [raw](https://raw.githubusercontent.com/solproxy/sol-free-proxy-list/main/all.txt) |
| `residential.txt` | Home ISP IPs | [raw](https://raw.githubusercontent.com/solproxy/sol-free-proxy-list/main/residential.txt) |
| `datacenter.txt` | Hosting / cloud IPs | [raw](https://raw.githubusercontent.com/solproxy/sol-free-proxy-list/main/datacenter.txt) |
| `mobile.txt` | Mobile carrier IPs | [raw](https://raw.githubusercontent.com/solproxy/sol-free-proxy-list/main/mobile.txt) |
| `countries/XX.txt` | By exit country, ISO code (`US`, `DE`, `IN`...) | [US](https://raw.githubusercontent.com/solproxy/sol-free-proxy-list/main/countries/US.txt) · [DE](https://raw.githubusercontent.com/solproxy/sol-free-proxy-list/main/countries/DE.txt) · [all](countries/) |
| `proxies.json` | Country, ISP, type, latency, speed, uptime, last check | [raw](https://raw.githubusercontent.com/solproxy/sol-free-proxy-list/main/proxies.json) |

Need it to the minute? The same list is served live by the **list API**, re-tested every minute, no account needed:

```
https://solproxy.net/free-proxy-list/api.txt
https://solproxy.net/free-proxy-list/api.json
```

Filters: `?country=DE`, `?type=residential|datacenter|mobile`, `?protocol=https|all`.

## Quick start

**curl**

```bash
curl -s https://raw.githubusercontent.com/solproxy/sol-free-proxy-list/main/http.txt | head -5
curl -x http://$(curl -s https://raw.githubusercontent.com/solproxy/sol-free-proxy-list/main/http.txt | head -1) https://api.ipify.org
```

**Python**

```python
import random, requests

proxies = requests.get(
    "https://raw.githubusercontent.com/solproxy/sol-free-proxy-list/main/http.txt", timeout=30
).text.split()

for _ in range(5):  # free proxies die often: try a few
    p = "http://" + random.choice(proxies)
    try:
        r = requests.get("https://api.ipify.org?format=json",
                         proxies={"http": p, "https": p}, timeout=15)
        print(p, r.json())
        break
    except requests.RequestException:
        continue
```

**Node.js**

```js
const res = await fetch("https://raw.githubusercontent.com/solproxy/sol-free-proxy-list/main/http.txt");
const proxies = (await res.text()).trim().split("\n");
console.log(proxies[Math.floor(Math.random() * proxies.length)]);
```

**One country, from JSON**

```python
import requests
data = requests.get("https://raw.githubusercontent.com/solproxy/sol-free-proxy-list/main/proxies.json").json()
de = [f'{p["ip"]}:{p["port"]}' for p in data["proxies"] if p["country"] == "DE"]
```

## Or skip the list: connect to `ws.solproxy.net:8501`

Instead of downloading the list and checking which proxies are still alive, connect to one
address, `ws.solproxy.net:8501`, and log in with your free token. SOLProxy picks a live proxy for every request and swaps it
out the moment it dies.

1. [Create a free account](https://solproxy.net/register) and copy your **token** from the dashboard.
2. Use it as the proxy password: `http://free:YOUR_TOKEN@ws.solproxy.net:8501`

```python
import requests

proxy = "http://free:YOUR_TOKEN@ws.solproxy.net:8501"
r = requests.get("https://api.ipify.org?format=json",
                 proxies={"http": proxy, "https": proxy}, timeout=30)
print(r.json())   # the exit IP, not yours
```

```bash
curl -x "http://free:YOUR_TOKEN@ws.solproxy.net:8501" https://api.ipify.org
```

**Pick country, type or a sticky IP** by putting flags in the username (token stays the password):

| Username | Effect |
| --- | --- |
| `free` | New exit IP on every request |
| `de`, `us`, `tr`... | Prefer an exit in that country (falls back to another country if none is alive) |
| `residential`, `datacenter`, `mobile` | Only that IP type (strict: 503 if none is alive) |
| `sticky1m`, `sticky10m`, `sticky1h` | Keep the same exit IP for that long |
| `de-residential-sticky10m` | Combine them with `-` |

**Limits:** 25 GB a month free with a token (resets on the 1st, UTC). Without a token it still
works for 1 GB per IP per day, then answers `407` until you add one. Members only get proxies that
passed at least 9 of their last 10 checks.

## What these proxies are, honestly

These are **public open proxies** found on the internet: misconfigured routers, servers and devices.
They are not SOLProxy's own network. They are slow, they die within minutes or hours, and many
targets block them. Some intercept HTTPS (they present their own certificate), so
**never send passwords, cookies or personal data through them**.

For scraping that has to keep working, SOLProxy sells residential proxies at **$0.30/GB**,
pay as you go, no subscription: [solproxy.net/pricing](https://solproxy.net/pricing).

## How it works

1. solproxy.net scans public proxy sources and tests every candidate over HTTPS, every minute.
2. Every minute, SOLProxy's server runs [`scripts/update.py`](scripts/update.py), which pulls the verified
   list and rewrites the files here. Only the latest snapshot is kept, so cloning stays small.
   (raw.githubusercontent.com may cache a file for up to 5 minutes.)
3. If the API returns nothing, the previous list is kept instead of committing an empty one.

## Acceptable use

For lawful use only. See the [acceptable use policy](https://solproxy.net/abuse).
The list is provided as is, with no guarantee of availability or safety.

If this list saves you time, a ⭐ helps others find it.
