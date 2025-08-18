#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for image_extractor.py to verify markdown directory functionality
"""

import sys
import os
from pathlib import Path

# Add the bin/win32 directory to the path so we can import the image extractor
sys.path.insert(0, str(Path(__file__).parent / "bin" / "win32"))

try:
    from image_extractor import ImageExtractor, extract_images_from_document
    print("✓ Successfully imported image_extractor")
except ImportError as e:
    print(f"✗ Failed to import image_extractor: {e}")
    sys.exit(1)

def test_image_extractor_initialization():
    """Test that ImageExtractor can be initialized with markdown_dir parameter"""
    print("\n=== Testing ImageExtractor Initialization ===")
    
    # Test with default parameters
    try:
        extractor1 = ImageExtractor("test-document.txt")
        print("✓ ImageExtractor initialized with default parameters")
        print(f"  - Document path: {extractor1.document_path}")
        print(f"  - Output dir: {extractor1.output_dir}")
        print(f"  - Markdown dir: {extractor1.markdown_dir}")
    except Exception as e:
        print(f"✗ Failed to initialize with default parameters: {e}")
        return False
    
    # Test with custom output directory
    try:
        extractor2 = ImageExtractor("test-document.txt", "custom_output")
        print("✓ ImageExtractor initialized with custom output directory")
        print(f"  - Output dir: {extractor2.output_dir}")
        print(f"  - Markdown dir: {extractor2.markdown_dir}")
    except Exception as e:
        print(f"✗ Failed to initialize with custom output directory: {e}")
        return False
    
    # Test with custom markdown directory
    try:
        extractor3 = ImageExtractor("test-document.txt", "custom_output", "custom_markdown")
        print("✓ ImageExtractor initialized with custom markdown directory")
        print(f"  - Output dir: {extractor3.output_dir}")
        print(f"  - Markdown dir: {extractor3.markdown_dir}")
    except Exception as e:
        print(f"✗ Failed to initialize with custom markdown directory: {e}")
        return False
    
    return True

def test_relative_path_calculation():
    """Test the relative path calculation functionality"""
    print("\n=== Testing Relative Path Calculation ===")

    try:
        # Test default scenario (markdown in DocuGenius, images in DocuGenius/images)
        extractor1 = ImageExtractor("test-document.txt")
        test_image_path1 = Path("DocuGenius/images/test-document/image1.png")
        relative_path1 = extractor1._calculate_relative_path(test_image_path1)

        print(f"✓ Default relative path calculation successful")
        print(f"  - Image path: {test_image_path1}")
        print(f"  - Markdown dir: {extractor1.markdown_dir}")
        print(f"  - Relative path: {relative_path1}")

        # Test custom scenario
        extractor2 = ImageExtractor("test-document.txt", "custom_images", "custom_markdown")
        test_image_path2 = Path("custom_images/test-document/image1.png")
        relative_path2 = extractor2._calculate_relative_path(test_image_path2)

        print(f"✓ Custom relative path calculation successful")
        print(f"  - Image path: {test_image_path2}")
        print(f"  - Markdown dir: {extractor2.markdown_dir}")
        print(f"  - Relative path: {relative_path2}")

        return True
    except Exception as e:
        print(f"✗ Failed to calculate relative path: {e}")
        return False

def test_extract_images_from_document_function():
    """Test the main extract_images_from_document function"""
    print("\n=== Testing extract_images_from_document Function ===")

    try:
        # Test with different markdown modes
        modes = ["simple", "grouped", "inline"]

        for mode in modes:
            result = extract_images_from_document(
                "test-document.txt",
                "test_output",
                "test_markdown",
                mode
            )

            print(f"✓ Mode '{mode}' executed successfully")
            print(f"  - Success: {result.get('success', 'N/A')}")
            print(f"  - Error: {result.get('error', 'None')}")
            print(f"  - Images count: {result.get('images_count', 0)}")
            print(f"  - Has simple_image_list: {'simple_image_list' in result}")
            print(f"  - Has image_references_by_page: {'image_references_by_page' in result}")

        return True
    except Exception as e:
        print(f"✗ Failed to execute extract_images_from_document: {e}")
        return False

def main():
    """Run all tests"""
    print("DocuGenius Image Extractor Test Suite")
    print("=" * 50)
    
    tests = [
        test_image_extractor_initialization,
        test_relative_path_calculation,
        test_extract_images_from_document_function
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
