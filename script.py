import csv
import re
import requests
from concurrent.futures import ThreadPoolExecutor
import threading
from tqdm import tqdm

print_lock = threading.Lock()

def safe_print(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)

def extract_link(cell):
    match = re.search(r'href="([^"]+)"', cell)
    return match.group(1) if match else cell

def resolve_redirect(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        return response.url if response.ok else url
    except requests.RequestException as e:
        return url

# Fetch the Markdown content from the URL
url = 'https://raw.githubusercontent.com/cvrve/Summer2025-Internships/refs/heads/dev/README.md'
response = requests.get(url)
if response.status_code == 200:
    lines = response.text.splitlines()
else:
    raise Exception(f"Failed to fetch the file. Status code: {response.status_code}")

# Extract the table lines
table_start = False
table_lines = []
for line in lines:
    if '| ---' in line:
        table_start = True
        continue
    if table_start:
        if line.strip() == '':
            break
        table_lines.append(line.strip())

# Parse the Markdown table
headers = [header.strip() for header in table_lines[0].split('|') if header.strip()]
rows = [
    [col.strip() for col in row.split('|') if col.strip()]
    for row in table_lines[1:]
]

# Add meaningful headers
headers = ["Company", "Role", "Location", "Application Link", "Date Posted"]

# Clean the "Application Link" column
cleaned_rows = []
for row in rows:
    cleaned_row = row[:]
    if len(cleaned_row) > 3:
        cleaned_row[3] = extract_link(cleaned_row[3])
    cleaned_rows.append(cleaned_row)

# Handle rows with "↳" in the Company column
for i in range(1, len(cleaned_rows)):
    if cleaned_rows[i][0] == "↳":
        cleaned_rows[i][0] = cleaned_rows[i - 1][0]

# Resolve redirects in the "Application Link" column
resolved_rows = []
MAX_WORKERS = 50

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    future_to_row = {
        executor.submit(resolve_redirect, row[3]): row
        for row in cleaned_rows if len(row) > 3
    }
    for future in tqdm(future_to_row, desc="Resolving redirects"):
        row = future_to_row[future]
        try:
            resolved_url = future.result()
            resolved_row = row[:]
            resolved_row[3] = resolved_url
            resolved_rows.append(resolved_row)
        except Exception as e:
            safe_print(f"Error processing {row[3]}: {str(e)}")
            resolved_rows.append(row)

# Write the resolved data to a new CSV file
output_file_path = 'summer_internships_normalized.csv'
with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(headers)
    csvwriter.writerows(resolved_rows)

print(f"\nCSV file with resolved links has been saved to {output_file_path}")