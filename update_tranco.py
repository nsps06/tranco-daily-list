import requests
import zipfile
import io
import sys

def main():
    try:
        url = "https://tranco-list.eu/top-1m.csv.zip"
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; GitHub Actions Workflow)",
            "Accept": "application/zip"
        }
        print(f"Downloading from {url} ...")
        r = requests.get(url, headers=headers, timeout=30)
        print("Response status:", r.status_code)
        r.raise_for_status()

        if not r.content.startswith(b'PK'):
            print("Error: downloaded file does not start with 'PK' signature for ZIP files")
            sys.exit(1)

        z = zipfile.ZipFile(io.BytesIO(r.content))
        csv_filename = z.namelist()[0]
        content = z.read(csv_filename).decode()

        with open("top-1m.csv", "w", encoding="utf-8") as f:
            f.write(content)
        print("File written successfully.")
    except Exception as e:
        print("Error:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
