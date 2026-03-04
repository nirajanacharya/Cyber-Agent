"""Check if monitoring is configured correctly."""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def check_setup():
    """Check monitoring setup."""
    checks_passed = 0
    total_checks = 4
    

    print("1. Checking LOGFIRE_TOKEN...")
    token = os.getenv("LOGFIRE_TOKEN")
    if token:
        print(f"  Token found ({token[:20]}...)")
        checks_passed += 1
    else:
        print("    LOGFIRE_TOKEN not found in .env")
    
  
    print("\n2. Checking Logfire installation...")
    try:
        import logfire
        print(f"    Logfire installed (v{logfire.__version__})")
        checks_passed += 1
    except ImportError:
        print("    Logfire not installed (run: pip install logfire)")
    

    print("\n3. Checking monitoring modules...")
    monitoring_files = [
        "monitoring/logfire_config.py",
        "monitoring/agent_monitor.py",
        "monitoring/session_tracker.py",
        "monitoring/feedback_collector.py",
    ]
    all_exist = all(Path(f).exists() for f in monitoring_files)
    if all_exist:
        print("  All monitoring modules present")
        checks_passed += 1
    else:
        print("   Some monitoring modules missing")
    

    print("\n4. Testing Logfire connection...")
    if token and 'logfire' in sys.modules:
        try:
            from monitoring.logfire_config import setup_logfire
            setup_logfire("test-connection")
            print("    Connected to Logfire!")
            print(f"    Dashboard: https://logfire.pydantic.dev/")
            checks_passed += 1
        except Exception as e:
            print(f"    Connection failed: {e}")
    else:
        print("   ⏭️  Skipped (prerequisites not met)")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Results: {checks_passed}/{total_checks} checks passed")
    print(f"{'='*60}")
    
    if checks_passed == total_checks:
        print(" Ready to collect monitoring data!")
        print("\nNext: Run 'streamlit run streamlit_app/app.py'")
    else:
        print("  Fix the issues above before collecting data")

if __name__ == "__main__":
    check_setup()
