"""
New York Healthcare Companies Research Script
A comprehensive script to research healthcare organizations in New York state
"""

from npi_api_client import NPIRegistryClient
import json
import csv
from datetime import datetime
from visualize import visualize_results

def research_ny_healthcare_companies():
    """Comprehensive research of healthcare companies in New York"""
    
    client = NPIRegistryClient()
    
    print("🏥 New York Healthcare Companies Research")
    print("=" * 60)
    
    # Research categories
    research_categories = {
        'Hospitals': ['Hospital', 'Medical Center', 'Health System'],
        'Clinics': ['Clinic', 'Medical Group', 'Health Center'],
        'Specialized Care': ['Psychiatric', 'Rehabilitation', 'Cancer', 'Cardiology'],
        'Nursing Homes': ['Nursing Home', 'Skilled Nursing', 'Long Term Care'],
        'Mental Health': ['Mental Health', 'Behavioral Health', 'Psychiatric']
    }
    
    all_results = []
    
    for category, search_terms in research_categories.items():
        print(f"\n🔍 Researching {category}...")
        category_results = []
        
        for term in search_terms:
            print(f"  Searching for: {term}")
            
            # Search by organization name
            results = client.search_providers(
                organization_name=term,
                enumeration_type='NPI-2',  # Organizations only
                limit=50
            )
            
            if 'result_count' in results and results['result_count'] > 0:
                for result in results.get('results', []):
                    # Filter for New York organizations
                    addresses = result.get('addresses', [])
                    is_ny_org = any(addr.get('state') == 'NY' for addr in addresses)
                    
                    if is_ny_org:
                        org_data = {
                            'category': category,
                            'search_term': term,
                            'npi_number': result.get('number', ''),
                            'organization_name': result.get('basic', {}).get('organization_name', ''),
                            'city': addresses[0].get('city', '') if addresses else '',
                            'state': addresses[0].get('state', '') if addresses else '',
                            'zip_code': addresses[0].get('postal_code', '') if addresses else '',
                            'phone': addresses[0].get('telephone_number', '') if addresses else '',
                            'taxonomy': result.get('taxonomies', [{}])[0].get('desc', '') if result.get('taxonomies') else '',
                            'enumeration_date': result.get('basic', {}).get('enumeration_date', ''),
                            'status': result.get('basic', {}).get('status', '')
                        }
                        category_results.append(org_data)
                        all_results.append(org_data)
        
        print(f"  ✅ Found {len(category_results)} {category.lower()} in NY")
    
    # Save results to files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save as JSON
    json_filename = f"ny_healthcare_companies_{timestamp}.json"
    with open(json_filename, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\n💾 Results saved to {json_filename}")
    
    # Save as CSV
    csv_filename = f"ny_healthcare_companies_{timestamp}.csv"
    if all_results:
        fieldnames = all_results[0].keys()
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_results)
        print(f"💾 Results saved to {csv_filename}")
    
    # Summary statistics
    print(f"\n📊 Research Summary:")
    print(f"Total organizations found: {len(all_results)}")
    
    category_counts = {}
    for result in all_results:
        category = result['category']
        category_counts[category] = category_counts.get(category, 0) + 1
    
    for category, count in category_counts.items():
        print(f"  {category}: {count} organizations")
    
    # Display sample results
    print(f"\n📋 Sample Results:")
    for i, result in enumerate(all_results[:5], 1):
        print(f"\n{i}. {result['organization_name']}")
        print(f"   NPI: {result['npi_number']}")
        print(f"   Location: {result['city']}, {result['state']} {result['zip_code']}")
        print(f"   Category: {result['category']}")
        print(f"   Type: {result['taxonomy']}")
    
    return all_results

def search_specific_companies():
    """Search for specific well-known healthcare companies in NY"""
    
    client = NPIRegistryClient()
    
    print("\n🏢 Searching for Major Healthcare Companies in NY...")
    
    major_companies = [
        'Mount Sinai',
        'New York Presbyterian',
        'NYU Langone',
        'Montefiore',
        'Northwell Health',
        'Memorial Sloan Kettering',
        'Columbia University',
        'Weill Cornell',
        'Lenox Hill',
        'Bellevue Hospital'
    ]
    
    found_companies = []
    
    for company in major_companies:
        print(f"  Searching for: {company}")
        
        results = client.search_providers(
            organization_name=company,
            enumeration_type='NPI-2',
            limit=10
        )
        
        if 'result_count' in results and results['result_count'] > 0:
            for result in results.get('results', []):
                addresses = result.get('addresses', [])
                is_ny_org = any(addr.get('state') == 'NY' for addr in addresses)
                
                if is_ny_org:
                    company_data = {
                        'company_name': result.get('basic', {}).get('organization_name', ''),
                        'npi_number': result.get('number', ''),
                        'city': addresses[0].get('city', '') if addresses else '',
                        'state': addresses[0].get('state', '') if addresses else '',
                        'zip_code': addresses[0].get('postal_code', '') if addresses else '',
                        'phone': addresses[0].get('telephone_number', '') if addresses else '',
                        'taxonomy': result.get('taxonomies', [{}])[0].get('desc', '') if result.get('taxonomies') else ''
                    }
                    found_companies.append(company_data)
                    print(f"    ✅ Found: {company_data['company_name']}")
    
    return found_companies

if __name__ == "__main__":
    # Run comprehensive research
    research_results = research_ny_healthcare_companies()
    
    # Search for major companies
    major_companies = search_specific_companies()
    
    print(f"\n🎯 Research Complete!")
    print(f"Total organizations researched: {len(research_results)}")
    print(f"Major companies found: {len(major_companies)}")

    # Create visualization (saved to PNG)
    try:
        visualize_results(research_results, major_companies)
    except Exception as e:
        print(f"⚠️ Visualization failed: {e}")
