import requests
import zipfile
import io
import sys
import csv
import tldextract
from urllib.parse import urlparse

def fetch_tranco_top1m():
    try:
        url = "https://tranco-list.eu/top-1m.csv.zip"
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; GitHub Actions Workflow)",
            "Accept": "application/zip"
        }
        print(f"Downloading Tranco Top 1M from {url} ...")
        r = requests.get(url, headers=headers, timeout=30)
        print("Tranco response status:", r.status_code)
        r.raise_for_status()

        if not r.content.startswith(b'PK'):
            print("Error: downloaded file does not appear to be a valid ZIP file.")
            return

        z = zipfile.ZipFile(io.BytesIO(r.content))
        csv_filename = z.namelist()[0]
        content = z.read(csv_filename).decode()

        with open("top-1m.csv", "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ Tranco list written to 'top-1m.csv'")
    except Exception as e:
        print("Error fetching Tranco list:", e)

def fetch_phishing_domains():
    domains = set()
    try:
        url_openphish = "https://openphish.com/feed.txt"
        print(f"Downloading OpenPhish data from {url_openphish} ...")
        r = requests.get(url_openphish, timeout=10)
        r.raise_for_status()
        lines = r.text.splitlines()
        for line in lines:
            parsed = urlparse(line)
            ext = tldextract.extract(parsed.netloc)
            if ext.domain and ext.suffix:
                base_domain = f"{ext.domain}.{ext.suffix}".lower()
                domains.add(base_domain)
        print(f"✅ Fetched {len(domains)} phishing domains from OpenPhish.")
    except Exception as e:
        print(f"Error fetching OpenPhish: {e}")
        return

    try:
        with open("phishing-domains.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["domain"])
            for domain in sorted(domains):
                writer.writerow([domain])
        print("✅ Phishing domains written to 'phishing-domains.csv'")
    except Exception as e:
        print("Error writing phishing domains CSV:", e)

def main():
    fetch_tranco_top1m()
    fetch_phishing_domains()

if __name__ == "__main__":
    main()
