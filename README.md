# NPI Registry API Research Project

This project explores healthcare companies in New York state using the CMS NPI Registry API.

## Setup

1. Install dependencies:
```bash

2. Run the main script:
```bash
python npi_api_client.py
```

## Features

- Search for healthcare organizations in New York state
- Search by medical specialty
- Export results to CSV
- Detailed provider information lookup

## API Documentation

The NPI Registry API is a free, public RESTful service provided by CMS:
- Base URL: `https://npiregistry.cms.hhs.gov/api/`
- No authentication required
- Returns JSON data
- Maximum 1200 results per query

## Usage Examples

```python
from npi_api_client import NPIRegistryClient

client = NPIRegistryClient()

# Search for organizations in NY
orgs = client.search_ny_healthcare_organizations(limit=50)

# Search by specialty
hospitals = client.search_by_specialty("Hospital", "NY", limit=20)

# Get specific provider details
provider = client.get_provider_details("1234567890")
```
## Output Example
pip install -r requirements.txt<img width="651" height="282" alt="Screenshot 2025-10-05 at 10 19 17 PM" src="https://github.com/user-attachments/assets/68b358d4-d00d-4a8d-9436-242bf06e0ce2" />```
