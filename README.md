# Internship Link Resolver

This script processes a Markdown table of internship listings (provided by [CVRVE](https://github.com/cvrve/Summer2025-Internships/tree/dev)) and resolves all application links to their final destinations, saving the results in a CSV file.

## Features

- Extracts internship data from a Markdown table
- Resolves redirect chains to get final application URLs
- Handles concurrent processing for faster execution
- Provides progress tracking with status updates
- Exports results to a clean CSV format

## Requirements

```bash
pip install requests tqdm
```

## Usage

1. Run the script:
```bash
python script.py
```

2. The script will:
   - Fetch the internship data from the source repository
   - Process all application links
   - Resolve redirects concurrently
   - Save results to `summer_internships_normalized.csv`

## Output Format

The CSV file contains the following columns:
- Company
- Role
- Location
- Application Link
- Date Posted

## Configuration

You can adjust the following parameters in `script.py`:
- `MAX_WORKERS`: Number of concurrent threads (default: 50)
- `timeout`: Request timeout in seconds (default: 10)

## Error Handling

- Failed redirects will retain the original URL
- All errors are logged but won't stop the script
- Thread-safe printing ensures readable output

## Contributing

Feel free to open issues or submit pull requests with improvements.