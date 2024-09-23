from core.models import Authority, Authority_Locations
from django.utils import timezone
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

authorities_data = [
    {"name": "Police", "email": "police@radary.com", "phone_number": "123456789"},
    {"name": "Fire_station", "email": "fire_station@radary.com", "phone_number": "987654321"},
    {"name": "Hospital", "email": "hospital@radary.com", "phone_number": "112233445"},
    {"name": "City_council", "email": "city_council@radary.com", "phone_number": "556677889"},
]

# Dummy data for governorates, markaz, and coordinates
locations_data = [
    {"governorate": "Cairo", "markaz": "Nasr City", "coordinates": "30.0444,31.2357", "phone_number": "0112233445"},
    {"governorate": "Alexandria", "markaz": "Sidi Gaber", "coordinates": "31.2001,29.9187", "phone_number": "0112233446"},
    {"governorate": "Giza", "markaz": "Dokki", "coordinates": "30.0131,31.2089", "phone_number": "0112233447"},
    {"governorate": "Mansoura", "markaz": "Talkha", "coordinates": "31.0364,31.3807", "phone_number": "0112233448"},
    {"governorate": "Luxor", "markaz": "Esna", "coordinates": "25.6949,32.6396", "phone_number": "0112233449"},
]

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

# Function to populate Authority_Locations
def populate_authority_locations():
    for authority_data in authorities_data:
        try:
            authority = Authority.objects.get(name=authority_data["name"])
            
            # Create at least 3 locations for each authority
            for i in range(3):
                location_data = locations_data[i % len(locations_data)]  # Rotate through the locations_data
                
                Authority_Locations.objects.create(
                    authority=authority,
                    governorate=location_data["governorate"],
                    markaz=location_data["markaz"],
                    coordinates=location_data["coordinates"],
                    phone_number=location_data["phone_number"]
                )
                print(f"Created location for {authority.name} in {location_data['governorate']} - {location_data['markaz']}")
        
        except Authority.DoesNotExist:
            print(f"Authority {authority_data['name']} does not exist in the database.")

if __name__ == "__main__":
    create_authorities()
    populate_authority_locations()
