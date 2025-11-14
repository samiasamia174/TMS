import os
import django
import sys

# Add current directory to Python path
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TMS_01.settings')

try:
    django.setup()
    print("✅ Django setup successful")
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    print("Trying alternative approach...")
    
    # Try to find the correct settings
    possible_settings = [
        'TMS_01.settings',
        'settings', 
        'TMS_01.TMS_01.settings',
        'project.settings'
    ]
    
    for setting in possible_settings:
        try:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting)
            django.setup()
            print(f"✅ Success with: {setting}")
            break
        except:
            continue
    else:
        print("❌ Could not find correct settings module")
        exit()

from django.test import Client
from django.contrib.auth.models import User

client = Client()

print("=== DEBUGGING SIGNUP ISSUE ===")

# Test with different data variations
test_cases = [
    {
        'name': 'Complete valid data',
        'data': {
            'username': 'testuser123',
            'email': 'test123@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        }
    }
]

for test in test_cases:
    print(f"\n--- Testing: {test['name']} ---")
    
    response = client.post('/signup/', test['data'])
    print(f"Status: {response.status_code}")
    
    if response.status_code == 302:
        print("✅ SUCCESS - Redirect received")
        user_exists = User.objects.filter(username=test['data']['username']).exists()
        print(f"User created in DB: {user_exists}")
    else:
        print("❌ FAILED - Form returned with errors")
        
        # Try multiple ways to get form errors
        if hasattr(response, 'context') and 'form' in response.context:
            form = response.context['form']
            print("Form errors found in context:")
            for field, errors in form.errors.items():
                print(f"  {field}: {list(errors)}")
        else:
            print("No form context found")
            # Check response content for clues
            content = response.content.decode()
            if 'error' in content.lower() or 'invalid' in content.lower():
                print("Error clues in content (first 500 chars):")
                print(content[:500])
            else:
                print("No obvious errors in content")

# Cleanup
User.objects.filter(username='testuser123').delete()
print("\n✅ Cleanup completed")
