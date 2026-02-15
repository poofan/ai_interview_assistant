"""
Simple Backend Test - Without Database
"""

print("Testing Backend without DB...")

# Override DATABASE_URL before importing
import os
os.environ['DATABASE_URL'] = 'sqlite:///./test.db'
os.environ['DEBUG'] = 'True'

try:
    from app.main import app
    print("OK - FastAPI app created")
    print(f"   Title: {app.title}")
    print(f"   Version: {app.version}")
    
    # Count routes
    routes = [r for r in app.routes if hasattr(r, 'path') and '/api/v1/' in r.path]
    print(f"   API routes: {len(routes)}")
    
    for route in routes[:5]:
        print(f"      - {list(route.methods)[0] if route.methods else 'GET'} {route.path}")
    
    print("\nOK - Backend components work!")
    print("To run server: uvicorn app.main:app --reload --port 8000")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()


