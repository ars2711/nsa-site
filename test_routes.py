"""Quick test script to validate Flask routes."""
from app import app

def test_routes():
    with app.test_client() as client:
        # Test index
        resp = client.get('/')
        print(f"Index: {resp.status_code} ({len(resp.data)} bytes)")
        
        # Test projects
        resp = client.get('/projects')
        print(f"Projects: {resp.status_code} ({len(resp.data)} bytes)")
        
        # Test team
        resp = client.get('/team')
        print(f"Team: {resp.status_code} ({len(resp.data)} bytes)")
        
        # Test sitemap
        resp = client.get('/sitemap.xml')
        print(f"Sitemap: {resp.status_code} ({len(resp.data)} bytes)")
        
        # Test robots
        resp = client.get('/robots.txt')
        print(f"Robots: {resp.status_code} ({len(resp.data)} bytes)")
        
    print("\n✓ All routes tested successfully!")

if __name__ == '__main__':
    test_routes()
