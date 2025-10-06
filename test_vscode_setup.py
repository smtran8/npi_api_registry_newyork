"""
Test script to verify VSCode setup is working correctly
"""

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import requests
        print("✅ requests module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import requests: {e}")
        return False
    
    try:
        from npi_api_client import NPIRegistryClient
        print("✅ NPIRegistryClient imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import NPIRegistryClient: {e}")
        return False
    
    return True

def test_api_connection():
    """Test API connection"""
    try:
        from npi_api_client import NPIRegistryClient
        client = NPIRegistryClient()
        
        # Test with a simple search
        result = client.search_providers(organization_name='Hospital', limit=1)
        
        if 'result_count' in result:
            print("✅ API connection successful")
            return True
        else:
            print("❌ API connection failed")
            return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing VSCode Setup")
    print("=" * 40)
    
    # Test imports
    print("\n1. Testing imports...")
    imports_ok = test_imports()
    
    if not imports_ok:
        print("\n❌ Setup incomplete. Please check your Python environment.")
        return
    
    # Test API connection
    print("\n2. Testing API connection...")
    api_ok = test_api_connection()
    
    if api_ok:
        print("\n🎉 VSCode setup is working perfectly!")
        print("\nYou can now:")
        print("  • Run scripts with F5 (Debug)")
        print("  • Use the integrated terminal")
        print("  • Edit and debug your code")
        print("  • Run: python3 npi_api_client.py")
        print("  • Run: python3 ny_healthcare_research.py")
    else:
        print("\n⚠️  API connection failed, but VSCode setup is working.")

if __name__ == "__main__":
    main()
