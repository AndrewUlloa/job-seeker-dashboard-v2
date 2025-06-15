#!/usr/bin/env python3
"""
Comprehensive deployment tests to catch issues before deploying to Hugging Face
"""

import os
import sys
import traceback
import pandas as pd
from pathlib import Path

def test_imports():
    """Test that all required imports work correctly."""
    print("🧪 Testing imports...")
    
    try:
        import gradio as gr
        print(f"✅ Gradio version: {gr.__version__}")
        
        import pandas as pd
        print(f"✅ Pandas version: {pd.__version__}")
        
        import plotly.express as px
        import plotly
        print(f"✅ Plotly version: {plotly.__version__}")
        
        import numpy as np
        print(f"✅ NumPy version: {np.__version__}")
        
        from datetime import datetime
        import tempfile
        print(f"✅ Standard library imports: OK")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    return True

def test_app_import():
    """Test that the main app can be imported without errors."""
    print("\n🧪 Testing app import...")
    
    try:
        from app import FastJobSeekerDashboard, create_fast_interface
        print("✅ App modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ App import error: {e}")
        traceback.print_exc()
        return False

def test_data_loading():
    """Test that data files exist and can be loaded."""
    print("\n🧪 Testing data file availability...")
    
    # Check for data files
    data_files = [
        'optimized_employers.parquet',
        'LCA_2025_dashboard_ready.csv'
    ]
    
    files_found = 0
    for file in data_files:
        if os.path.exists(file):
            print(f"✅ Found: {file}")
            files_found += 1
        else:
            print(f"⚠️  Missing: {file}")
    
    if files_found == 0:
        print("❌ No data files found!")
        return False
    
    # Test data loading
    try:
        from app import FastJobSeekerDashboard
        dashboard = FastJobSeekerDashboard()
        
        if dashboard.data is not None:
            print(f"✅ Data loaded successfully: {len(dashboard.data):,} records")
            return True
        else:
            print("❌ Data loading failed")
            return False
            
    except Exception as e:
        print(f"❌ Data loading error: {e}")
        return False

def test_interface_creation():
    """Test that the Gradio interface can be created without errors."""
    print("\n🧪 Testing interface creation...")
    
    try:
        from app import create_fast_interface
        
        # This should not raise any errors
        demo = create_fast_interface()
        
        if demo is not None:
            print("✅ Interface created successfully")
            return True
        else:
            print("❌ Interface creation returned None")
            return False
            
    except Exception as e:
        print(f"❌ Interface creation error: {e}")
        traceback.print_exc()
        return False

def test_core_functionality():
    """Test core search and filtering functionality."""
    print("\n🧪 Testing core functionality...")
    
    try:
        from app import FastJobSeekerDashboard
        dashboard = FastJobSeekerDashboard()
        
        if dashboard.data is None:
            print("⚠️  Skipping functionality tests - no data loaded")
            return True
        
        # Test basic search
        result_df, summary, chart = dashboard.search_employers(
            search_text='', states=[], cities=[], classifications=[], 
            min_score=0.0, min_approval=0.0, only_cap_exempt=False, 
            year_filter='All Years'
        )
        print(f"✅ Basic search: {len(result_df)} results")
        
        # Test cap-exempt filtering
        result_cap_exempt, _, _ = dashboard.search_employers(
            search_text='', states=[], cities=[], classifications=[], 
            min_score=0.0, min_approval=0.0, only_cap_exempt=True, 
            year_filter='All Years'
        )
        print(f"✅ Cap-exempt filtering: {len(result_cap_exempt)} results")
        
        # Test full results
        full_df, full_summary = dashboard.get_full_results(
            search_text='', states=[], cities=[], classifications=[], 
            min_score=0.0, min_approval=0.0, only_cap_exempt=True, 
            year_filter='All Years'
        )
        print(f"✅ Full results: {len(full_df)} results")
        
        # Test CSV download
        csv_path = dashboard.download_csv(
            search_text='', states=[], cities=[], classifications=[], 
            min_score=0.0, min_approval=0.0, only_cap_exempt=True, 
            year_filter='All Years'
        )
        
        if csv_path and os.path.exists(csv_path):
            print(f"✅ CSV download: {csv_path}")
            # Clean up
            os.remove(csv_path)
        else:
            print("❌ CSV download failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        traceback.print_exc()
        return False

def test_gradio_compatibility():
    """Test Gradio component compatibility."""
    print("\n🧪 Testing Gradio component compatibility...")
    
    try:
        import gradio as gr
        
        # Test components used in the app
        components_to_test = [
            ('Textbox', lambda: gr.Textbox(label="Test", placeholder="Test")),
            ('Dropdown', lambda: gr.Dropdown(choices=['A', 'B'], label="Test", multiselect=True)),
            ('Slider', lambda: gr.Slider(minimum=0, maximum=1, value=0.5, label="Test")),
            ('Checkbox', lambda: gr.Checkbox(label="Test", value=True)),
            ('Button', lambda: gr.Button("Test", variant="primary", size="lg")),
            ('Dataframe', lambda: gr.Dataframe(label="Test", interactive=False, wrap=True)),
            ('File', lambda: gr.File(visible=False)),
            ('Plot', lambda: gr.Plot(label="Test")),
            ('Markdown', lambda: gr.Markdown("Test")),
            ('State', lambda: gr.State(False)),
            ('Column', lambda: gr.Column(visible=False)),
            ('Row', lambda: gr.Row()),
            ('Accordion', lambda: gr.Accordion("Test", open=False)),
            ('Blocks', lambda: gr.Blocks(title="Test"))
        ]
        
        for component_name, component_func in components_to_test:
            try:
                component = component_func()
                print(f"✅ {component_name}: OK")
            except Exception as e:
                print(f"❌ {component_name}: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Gradio compatibility test error: {e}")
        return False

def test_requirements():
    """Check if all required packages are available."""
    print("\n🧪 Testing requirements...")
    
    required_packages = [
        'gradio',
        'pandas', 
        'plotly',
        'numpy'
    ]
    
    try:
        import pkg_resources
        
        for package in required_packages:
            try:
                pkg_resources.get_distribution(package)
                print(f"✅ {package}: installed")
            except pkg_resources.DistributionNotFound:
                print(f"❌ {package}: not found")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Requirements check error: {e}")
        return False

def run_all_tests():
    """Run all deployment tests."""
    print("🚀 Running deployment tests...\n")
    
    tests = [
        ("Import Tests", test_imports),
        ("App Import", test_app_import),
        ("Data Loading", test_data_loading),
        ("Interface Creation", test_interface_creation),
        ("Core Functionality", test_core_functionality),
        ("Gradio Compatibility", test_gradio_compatibility),
        ("Requirements", test_requirements)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"{'='*50}")
        print(f"Running: {test_name}")
        print(f"{'='*50}")
        
        try:
            result = test_func()
            if result:
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            traceback.print_exc()
        
        print()
    
    print(f"{'='*50}")
    print(f"RESULTS: {passed}/{total} tests passed")
    print(f"{'='*50}")
    
    if passed == total:
        print("🎉 All tests passed! Ready for deployment.")
        return 0
    else:
        print("❌ Some tests failed. Do not deploy!")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code) 