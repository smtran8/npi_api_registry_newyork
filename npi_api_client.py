"""
NPI Registry API Client
A Python client for interacting with the CMS NPI Registry API
"""

import requests
import json
import pandas as pd
from typing import Dict, List, Optional
import time

class NPIRegistryClient:
    """Client for interacting with the NPI Registry API"""
    
    def __init__(self):
        self.base_url = "https://npiregistry.cms.hhs.gov/api/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'NPI-Research-Client/1.0'
        })
    
    def search_providers(self, **kwargs) -> Dict:
        """
        Search for healthcare providers using various criteria
        
        Args:
            **kwargs: Search parameters including:
                - number: NPI number
                - first_name: Provider first name
                - last_name: Provider last name
                - organization_name: Organization name
                - city: City
                - state: State (2-letter code)
                - postal_code: ZIP code
                - taxonomy_description: Provider specialty
                - limit: Number of results (max 1200)
        
        Returns:
            Dict: API response containing provider data
        """
        # Add required version parameter
        params = {'version': '2.1'}
        params.update(kwargs)
        
        try:
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return {"error": str(e)}
    
    def search_ny_healthcare_organizations(self, limit: int = 100) -> List[Dict]:
        """
        Search for healthcare organizations in New York state
        
        Args:
            limit: Maximum number of results to return
            
        Returns:
            List[Dict]: List of healthcare organizations
        """
        # Search for organizations in NY using city and enumeration_type
        search_params = {
            'city': 'New York',
            'enumeration_type': 'NPI-2',  # NPI-2 = Organization
            'limit': min(limit, 1200)  # API limit is 1200
        }
        
        results = self.search_providers(**search_params)
        
        if 'result_count' in results and results['result_count'] > 0:
            return results.get('results', [])
        else:
            print("No results found or error in search")
            return []
    
    def search_by_specialty(self, specialty: str, state: str = 'NY', limit: int = 100) -> List[Dict]:
        """
        Search for providers by medical specialty
        
        Args:
            specialty: Medical specialty/taxonomy description
            state: State code (default: NY)
            limit: Maximum number of results
            
        Returns:
            List[Dict]: List of providers with the specified specialty
        """
        search_params = {
            'taxonomy_description': specialty,
            'state': state,
            'limit': min(limit, 1200)
        }
        
        results = self.search_providers(**search_params)
        
        if 'result_count' in results and results['result_count'] > 0:
            return results.get('results', [])
        else:
            print(f"No results found for specialty: {specialty}")
            return []
    
    def get_provider_details(self, npi_number: str) -> Dict:
        """
        Get detailed information for a specific provider by NPI number
        
        Args:
            npi_number: 10-digit NPI number
            
        Returns:
            Dict: Provider information
        """
        results = self.search_providers(number=npi_number)
        
        if 'result_count' in results and results['result_count'] > 0:
            return results['results'][0]
        else:
            return {"error": "Provider not found"}
    
    def save_to_csv(self, data: List[Dict], filename: str):
        """
        Save search results to CSV file
        
        Args:
            data: List of provider dictionaries
            filename: Output CSV filename
        """
        if not data:
            print("No data to save")
            return
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

def main():
    """Example usage of the NPI Registry Client"""
    client = NPIRegistryClient()
    
    print("🔍 NPI Registry API Client")
    print("=" * 50)
    
    # Test basic API connectivity
    print("\n1. Testing API connectivity...")
    test_result = client.search_providers(organization_name='Hospital', limit=1)
    if 'result_count' in test_result:
        print(f"✅ API is working! Found {test_result['result_count']} total providers")
    else:
        print("❌ API connection failed")
        return
    
    # Search for healthcare organizations in NY
    print("\n2. Searching for healthcare organizations in New York...")
    ny_orgs = client.search_ny_healthcare_organizations(limit=10)
    
    if ny_orgs:
        print(f"✅ Found {len(ny_orgs)} healthcare organizations in NY")
        
        # Display first few results
        for i, org in enumerate(ny_orgs[:3], 1):
            print(f"\nOrganization {i}:")
            print(f"  Name: {org.get('basic', {}).get('organization_name', 'N/A')}")
            print(f"  NPI: {org.get('number', 'N/A')}")
            print(f"  Address: {org.get('addresses', [{}])[0].get('address_1', 'N/A')}")
    else:
        print("❌ No organizations found")
    
    # Search by specialty
    print("\n3. Searching for hospitals in NY...")
    hospitals = client.search_by_specialty("Hospital", "NY", limit=5)
    
    if hospitals:
        print(f"✅ Found {len(hospitals)} hospitals in NY")
        for i, hospital in enumerate(hospitals[:2], 1):
            print(f"\nHospital {i}:")
            print(f"  Name: {hospital.get('basic', {}).get('organization_name', 'N/A')}")
            print(f"  NPI: {hospital.get('number', 'N/A')}")

if __name__ == "__main__":
    main()
