import datetime

from core.models import User

emergency_user = User.objects.create_user(
    username='emergency_user',
    email='emergency_user@example.com',
    password='12345678',
    first_name = 'Emergency',
    last_name = 'User',
    phone_number = '123-456-7890',
    date_of_birth = datetime.date(year=2000, month=1, day=1)
)

# Save the user
emergency_user.save()
