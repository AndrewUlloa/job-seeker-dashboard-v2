#!/usr/bin/env python3
"""
Specific test for Gradio compatibility issues that could break deployment
"""

import sys
import traceback

def test_gradio_dataframe_compatibility():
    """Test specific Gradio Dataframe parameters that may not be supported in all versions."""
    print("🧪 Testing Gradio Dataframe compatibility...")
    
    try:
        import gradio as gr
        print(f"✅ Gradio version: {gr.__version__}")
        
        # Test basic Dataframe creation
        df_basic = gr.Dataframe(label="Test", interactive=False, wrap=True)
        print("✅ Basic Dataframe creation: OK")
        
        # Test potentially problematic parameters (advisory warnings, not failures)
        problematic_params = [
            ('max_rows', lambda: gr.Dataframe(label="Test", max_rows=None)),
            ('max_height', lambda: gr.Dataframe(label="Test", max_height=400)),
            ('overflow_row_behaviour', lambda: gr.Dataframe(label="Test", overflow_row_behaviour='paginate')),
        ]
        
        warnings = []
        for param_name, param_func in problematic_params:
            try:
                component = param_func()
                print(f"✅ {param_name} parameter: SUPPORTED")
            except TypeError as e:
                if 'unexpected keyword argument' in str(e):
                    print(f"⚠️  {param_name} parameter: NOT SUPPORTED - {e}")
                    warnings.append(param_name)
                else:
                    raise e
        
        if warnings:
            print(f"📋 Summary: {len(warnings)} parameter(s) not supported: {', '.join(warnings)}")
            print("💡 This is advisory - deployment can proceed if app works")
        
        return True  # Always return True for compatibility tests
        
    except Exception as e:
        print(f"❌ Gradio Dataframe compatibility test failed: {e}")
        traceback.print_exc()
        return False

def test_gradio_button_parameters():
    """Test Gradio Button parameters."""
    print("\n🧪 Testing Gradio Button compatibility...")
    
    try:
        import gradio as gr
        
        # Test button parameters that might not be supported
        button_params = [
            ('variant+size', lambda: gr.Button("Test", variant="primary", size="lg")),
            ('variant_only', lambda: gr.Button("Test", variant="secondary")),
            ('size_only', lambda: gr.Button("Test", size="sm")),
        ]
        
        for param_name, param_func in button_params:
            try:
                component = param_func()
                print(f"✅ Button {param_name}: SUPPORTED")
            except TypeError as e:
                if 'unexpected keyword argument' in str(e):
                    print(f"⚠️  Button {param_name}: NOT SUPPORTED - {e}")
                else:
                    raise e
        
        return True
        
    except Exception as e:
        print(f"❌ Gradio Button compatibility test failed: {e}")
        return False

def test_gradio_file_parameters():
    """Test Gradio File component parameters."""
    print("\n🧪 Testing Gradio File compatibility...")
    
    try:
        import gradio as gr
        
        # Test file parameters
        file_params = [
            ('visible', lambda: gr.File(visible=False)),
            ('label', lambda: gr.File(label="Test File")),
        ]
        
        for param_name, param_func in file_params:
            try:
                component = param_func()
                print(f"✅ File {param_name}: SUPPORTED")
            except TypeError as e:
                if 'unexpected keyword argument' in str(e):
                    print(f"⚠️  File {param_name}: NOT SUPPORTED - {e}")
                else:
                    raise e
        
        return True
        
    except Exception as e:
        print(f"❌ Gradio File compatibility test failed: {e}")
        return False

def test_app_interface_creation():
    """Test that our specific app interface can be created."""
    print("\n🧪 Testing app interface creation...")
    
    try:
        from app import create_fast_interface
        
        demo = create_fast_interface()
        if demo is not None:
            print("✅ App interface creation: SUCCESS")
            return True
        else:
            print("❌ App interface creation: FAILED (returned None)")
            return False
            
    except Exception as e:
        print(f"❌ App interface creation: FAILED - {e}")
        traceback.print_exc()
        return False

def main():
    """Run all Gradio compatibility tests."""
    print("🚀 Running Gradio Compatibility Tests\n")
    
    tests = [
        ("Dataframe Compatibility", test_gradio_dataframe_compatibility),
        ("Button Parameters", test_gradio_button_parameters),
        ("File Parameters", test_gradio_file_parameters),
        ("App Interface Creation", test_app_interface_creation),
    ]
    
    passed = 0
    total = len(tests)
    critical_failures = 0
    
    for test_name, test_func in tests:
        print(f"{'='*60}")
        print(f"Running: {test_name}")
        print(f"{'='*60}")
        
        try:
            result = test_func()
            if result:
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
                # Only app interface creation is critical for deployment
                if test_name == "App Interface Creation":
                    critical_failures += 1
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            if test_name == "App Interface Creation":
                critical_failures += 1
            traceback.print_exc()
        
        print()
    
    print(f"{'='*60}")
    print(f"RESULTS: {passed}/{total} tests passed")
    print(f"{'='*60}")
    
    if critical_failures > 0:
        print("❌ Critical deployment failures detected!")
        print("🚫 App interface cannot be created - deployment blocked!")
        return 1
    elif passed == total:
        print("🎉 All compatibility tests passed!")
        return 0
    else:
        print("⚠️  Some compatibility warnings detected.")
        print("✅ App interface works - deployment can proceed!")
        print("💡 Warnings are advisory and help avoid future issues.")
        return 0  # Return 0 (success) for warnings

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 