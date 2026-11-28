"""Pull the verified free proxy list from solproxy.net and write it out as
plain text (one proxy per line), JSON and per-country files, then refresh the
stats block in README.md."""
import json
import os
import re
import shutil
import urllib.request

API = os.environ.get("SOLPROXY_LIST_API", "https://solproxy.net/free-proxy-list/api.json?protocol=all")

req = urllib.request.Request(API, headers={"User-Agent": "solproxy-free-proxy-list/1.0"})
with urllib.request.urlopen(req, timeout=60) as r:
    data = json.load(r)

proxies = sorted(data["proxies"], key=lambda p: (p.get("latency_ms") or 10**9))
if not proxies:
    raise SystemExit("empty list, keeping the previous commit")


def line(p):
    return f'{p["ip"]}:{p["port"]}'


def write(path, rows):
    with open(path, "w") as f:
        f.write("\n".join(rows) + ("\n" if rows else ""))


write("http.txt", [line(p) for p in proxies if p.get("protocol") != "https"])
write("https.txt", [line(p) for p in proxies if p.get("protocol") == "https"])
write("all.txt", [("https://" if p.get("protocol") == "https" else "http://") + line(p) for p in proxies])
for kind in ("residential", "datacenter", "mobile"):
    write(f"{kind}.txt", [line(p) for p in proxies if p.get("type") == kind])
with open("proxies.json", "w") as f:
    json.dump({"updated_at": data.get("updated_at"), "count": len(proxies), "proxies": proxies}, f, indent=1)

shutil.rmtree("countries", ignore_errors=True)
os.makedirs("countries")
by_country = {}
for p in proxies:
    by_country.setdefault(p.get("country") or "XX", []).append(line(p))
for cc, rows in by_country.items():
    write(f"countries/{cc}.txt", rows)

counts = {k: sum(1 for p in proxies if p.get("type") == k) for k in ("residential", "datacenter", "mobile")}
top = sorted(by_country.items(), key=lambda kv: -len(kv[1]))[:10]
stats = "\n".join([
    f"**Last update:** {data.get('updated_at', '')[:16].replace('T', ' ')} UTC  ",
    f"**Working proxies:** {len(proxies)} "
    f"({counts['residential']} residential, {counts['datacenter']} datacenter, {counts['mobile']} mobile)  ",
    "**Top countries:** " + ", ".join(f"{cc} {len(rows)}" for cc, rows in top),
])
with open("README.md") as f:
    readme = f.read()
readme = re.sub(r"(<!-- stats -->).*?(<!-- /stats -->)", lambda m: f"{m.group(1)}\n{stats}\n{m.group(2)}",
                readme, flags=re.S)
with open("README.md", "w") as f:
    f.write(readme)
