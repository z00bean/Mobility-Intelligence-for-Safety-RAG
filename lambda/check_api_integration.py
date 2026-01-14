#!/usr/bin/env python3
"""
Unit Test for API Integration
**Validates: Requirements 8.4**

This test validates API endpoint compatibility and request format
to ensure the new interface maintains proper integration with the existing API.
"""

import re
import json
from typing import Dict, Any, Optional

def read_html_file(filename: str = "index.html") -> str:
    """Read the HTML file content."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def extract_api_endpoint_details(html_content: str) -> Dict[str, Any]:
    """Extract API endpoint configuration from HTML content."""
    details = {
        'endpoint_url': None,
        'method': None,
        'content_type': None,
        'request_body_format': None,
        'response_format': None,
        'error_handling': False,
        'timeout_handling': False
    }
    
    # Extract fetch URL
    fetch_pattern = r'fetch\s*\(\s*["\']([^"\']+)["\']'
    fetch_match = re.search(fetch_pattern, html_content)
    if fetch_match:
        details['endpoint_url'] = fetch_match.group(1)
    
    # Extract HTTP method
    method_pattern = r'method:\s*["\']([^"\']+)["\']'
    method_match = re.search(method_pattern, html_content)
    if method_match:
        details['method'] = method_match.group(1).upper()
    
    # Extract Content-Type header
    content_type_pattern = r'["\']Content-Type["\']:\s*["\']([^"\']+)["\']'
    content_type_match = re.search(content_type_pattern, html_content)
    if content_type_match:
        details['content_type'] = content_type_match.group(1)
    
    # Check request body format
    if 'JSON.stringify' in html_content:
        details['request_body_format'] = 'json'
        
        # Extract the structure being stringified
        stringify_pattern = r'JSON\.stringify\s*\(\s*\{([^}]+)\}\s*\)'
        stringify_match = re.search(stringify_pattern, html_content)
        if stringify_match:
            details['request_structure'] = stringify_match.group(1).strip()
    
    # Check response format
    if '.json()' in html_content:
        details['response_format'] = 'json'
    
    # Check error handling
    details['error_handling'] = 'catch' in html_content and ('err' in html_content or 'error' in html_content)
    
    # Check timeout handling (basic check)
    details['timeout_handling'] = 'timeout' in html_content.lower()
    
    return details

def validate_api_endpoint_compatibility() -> Dict[str, Any]:
    """Test API endpoint compatibility with expected format."""
    html_content = read_html_file()
    if not html_content:
        return {'error': 'Could not read HTML file'}
    
    api_details = extract_api_endpoint_details(html_content)
    
    # Expected API configuration based on requirements
    expected_config = {
        'endpoint_url': 'https://qn4fgxzu09.execute-api.us-east-1.amazonaws.com/chat',
        'method': 'POST',
        'content_type': 'application/json',
        'request_body_format': 'json',
        'response_format': 'json'
    }
    
    validation_results = {}
    
    # Test 1: Endpoint URL
    validation_results['endpoint_url_correct'] = (
        api_details['endpoint_url'] == expected_config['endpoint_url']
    )
    
    # Test 2: HTTP Method
    validation_results['method_correct'] = (
        api_details['method'] == expected_config['method']
    )
    
    # Test 3: Content-Type Header
    validation_results['content_type_correct'] = (
        api_details['content_type'] == expected_config['content_type']
    )
    
    # Test 4: Request Body Format
    validation_results['request_format_correct'] = (
        api_details['request_body_format'] == expected_config['request_body_format']
    )
    
    # Test 5: Response Format
    validation_results['response_format_correct'] = (
        api_details['response_format'] == expected_config['response_format']
    )
    
    # Test 6: Error Handling Present
    validation_results['error_handling_present'] = api_details['error_handling']
    
    return {
        'validation_results': validation_results,
        'api_details': api_details,
        'expected_config': expected_config,
        'all_tests_passed': all(validation_results.values())
    }

def validate_request_format() -> Dict[str, Any]:
    """Test that the request format matches API expectations."""
    html_content = read_html_file()
    if not html_content:
        return {'error': 'Could not read HTML file'}
    
    # Extract the request body structure
    request_structure_tests = {}
    
    # Test 1: Query parameter is included in request
    query_in_request = 'query' in html_content and 'JSON.stringify' in html_content
    request_structure_tests['query_parameter_present'] = query_in_request
    
    # Test 2: Request uses the query variable
    query_variable_pattern = r'JSON\.stringify\s*\(\s*\{\s*query\s*\}'
    query_variable_used = bool(re.search(query_variable_pattern, html_content))
    request_structure_tests['query_variable_used'] = query_variable_used
    
    # Test 3: Input value is captured correctly
    input_capture_pattern = r'document\.getElementById\s*\(\s*["\']queryInput["\']\s*\)\.value'
    input_captured = bool(re.search(input_capture_pattern, html_content))
    request_structure_tests['input_value_captured'] = input_captured
    
    # Test 4: Input is trimmed
    input_trimmed = '.trim()' in html_content
    request_structure_tests['input_trimmed'] = input_trimmed
    
    # Test 5: Empty query validation
    empty_query_check = 'if (!query)' in html_content or 'if (query === "")' in html_content or 'if (!query.trim())' in html_content
    request_structure_tests['empty_query_validation'] = empty_query_check
    
    return {
        'request_structure_tests': request_structure_tests,
        'all_request_tests_passed': all(request_structure_tests.values())
    }

def validate_response_handling() -> Dict[str, Any]:
    """Test that response handling matches API expectations."""
    html_content = read_html_file()
    if not html_content:
        return {'error': 'Could not read HTML file'}
    
    response_tests = {}
    
    # Test 1: Response is parsed as JSON
    response_tests['json_parsing'] = '.json()' in html_content
    
    # Test 2: Success response handling
    success_handling = 'data.answer' in html_content
    response_tests['success_response_handling'] = success_handling
    
    # Test 3: Error response handling
    error_handling = 'data.error' in html_content or 'res.status' in html_content
    response_tests['error_response_handling'] = error_handling
    
    # Test 4: Network error handling
    network_error_handling = 'catch' in html_content and 'err' in html_content
    response_tests['network_error_handling'] = network_error_handling
    
    # Test 5: Response status check
    status_check = 'res.ok' in html_content or 'res.status' in html_content
    response_tests['response_status_check'] = status_check
    
    # Test 6: Response display in chat
    response_display = 'miso-message' in html_content and 'appendChild' in html_content
    response_tests['response_display'] = response_display
    
    return {
        'response_tests': response_tests,
        'all_response_tests_passed': all(response_tests.values())
    }

def run_api_integration_tests() -> bool:
    """Run all API integration unit tests."""
    print("🧪 Running Unit Tests: API Integration")
    print("=" * 50)
    
    all_passed = True
    
    # Test 1: API Endpoint Compatibility
    print("\n📡 Test 1: API Endpoint Compatibility")
    endpoint_results = validate_api_endpoint_compatibility()
    
    if 'error' in endpoint_results:
        print(f"❌ Error: {endpoint_results['error']}")
        return False
    
    for test_name, passed in endpoint_results['validation_results'].items():
        status = "✅" if passed else "❌"
        test_display = test_name.replace('_', ' ').title()
        print(f"   {status} {test_display}")
        if not passed:
            all_passed = False
            expected = endpoint_results['expected_config']
            actual = endpoint_results['api_details']
            if 'endpoint_url' in test_name:
                print(f"      Expected: {expected['endpoint_url']}")
                print(f"      Actual: {actual['endpoint_url']}")
            elif 'method' in test_name:
                print(f"      Expected: {expected['method']}")
                print(f"      Actual: {actual['method']}")
            elif 'content_type' in test_name:
                print(f"      Expected: {expected['content_type']}")
                print(f"      Actual: {actual['content_type']}")
    
    # Test 2: Request Format
    print("\n📤 Test 2: Request Format")
    request_results = validate_request_format()
    
    if 'error' in request_results:
        print(f"❌ Error: {request_results['error']}")
        return False
    
    for test_name, passed in request_results['request_structure_tests'].items():
        status = "✅" if passed else "❌"
        test_display = test_name.replace('_', ' ').title()
        print(f"   {status} {test_display}")
        if not passed:
            all_passed = False
    
    # Test 3: Response Handling
    print("\n📥 Test 3: Response Handling")
    response_results = validate_response_handling()
    
    if 'error' in response_results:
        print(f"❌ Error: {response_results['error']}")
        return False
    
    for test_name, passed in response_results['response_tests'].items():
        status = "✅" if passed else "❌"
        test_display = test_name.replace('_', ' ').title()
        print(f"   {status} {test_display}")
        if not passed:
            all_passed = False
    
    # Summary
    print(f"\n📊 Test Summary:")
    endpoint_passed = endpoint_results['all_tests_passed']
    request_passed = request_results['all_request_tests_passed']
    response_passed = response_results['all_response_tests_passed']
    
    print(f"   API Endpoint Compatibility: {'✅ PASSED' if endpoint_passed else '❌ FAILED'}")
    print(f"   Request Format: {'✅ PASSED' if request_passed else '❌ FAILED'}")
    print(f"   Response Handling: {'✅ PASSED' if response_passed else '❌ FAILED'}")
    
    if all_passed:
        print(f"\n🎉 All API Integration Tests PASSED")
        print("   The new interface maintains full compatibility with the existing API")
    else:
        print(f"\n❌ Some API Integration Tests FAILED")
        print("   API compatibility issues detected")
    
    return all_passed

if __name__ == "__main__":
    success = run_api_integration_tests()
    exit(0 if success else 1)