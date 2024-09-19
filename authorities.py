from core.models import Authority
from django.utils import timezone

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')  # Replace 'your_project_name'
django.setup()

# Data for the four authorities
authorities_data = [
    {"name": "Police", "email": "police@radary.com", "phone_number": "123456789"},
    {"name": "Fire_station", "email": "fire_station@radary.com", "phone_number": "987654321"},
    {"name": "Hospital", "email": "hospital@radary.com", "phone_number": "112233445"},
    {"name": "City_council", "email": "city_council@radary.com", "phone_number": "556677889"},
]

# Function to create authorities
def create_authorities():
    for authority_data in authorities_data:
        Authority.objects.create(
            name=authority_data["name"],
            email=authority_data["email"],
            phone_number=authority_data["phone_number"],
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
    print("Authorities created successfully!")

if __name__ == "__main__":
    create_authorities()