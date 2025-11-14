import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TMS_01.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

client = Client()

print("=== DEBUGGING SIGNUP ISSUE ===")

# Test data
test_cases = [
    {
        'name': 'Valid signup',
        'data': {
            'username': 'testuser123',
            'email': 'test123@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        }
    },
    {
        'name': 'Weak password',
        'data': {
            'username': 'testuser456',
            'email': 'test456@example.com', 
            'password1': '123',
            'password2': '123',
        }
    }
]

for test in test_cases:
    print(f"\n--- Testing: {test['name']} ---")
    
    response = client.post('/signup/', test['data'])
    print(f"Status: {response.status_code}")
    
    if response.status_code == 302:
        print("✅ SUCCESS - Redirect received")
        # Check if user was created
        user_exists = User.objects.filter(username=test['data']['username']).exists()
        print(f"User created in DB: {user_exists}")
    else:
        print("❌ FAILED - Form returned with errors")
        
        # Try to extract form errors
        if hasattr(response, 'context') and 'form' in response.context:
            form = response.context['form']
            print("Form errors:")
            for field, errors in form.errors.items():
                print(f"  {field}: {list(errors)}")
        else:
            print("Could not extract form errors")
            print(f"Response content sample: {response.content.decode()[:500]}")

# Cleanup
User.objects.filter(username__in=['testuser123', 'testuser456']).delete()
print("\n✅ Cleanup completed")
