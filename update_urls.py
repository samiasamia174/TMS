import re

# Read the settings file
with open('uap_tms/settings.py', 'r') as f:
    content = f.read()

# Update ROOT_URLCONF
content = re.sub(r"ROOT_URLCONF\s*=\s*['\"].*['\"]", "ROOT_URLCONF = 'urls'", content)

# Write back
with open('uap_tms/settings.py', 'w') as f:
    f.write(content)

print("✅ Updated ROOT_URLCONF to use 'urls'")
