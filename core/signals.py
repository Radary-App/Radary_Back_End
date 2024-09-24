from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.conf import settings
from .models import Review, Summary, Problem, AI_Problem, Authority, Emergency, AI_Emergency, Authority_Locations, Problem_Authority_Location, Emergency_Authority_Location
from Radary_AI import main as AI_Engine
import os, base64
import math

BASE_DIR  = settings.BASE_DIR
BASE_DIR_MEDIA = os.path.join(BASE_DIR, 'media')
#-------------------------------------------------------------
# Generation of AI Summaries for REVIEWS
@receiver(post_save, sender=Review)
def track_reviews(sender, instance, created, **kwargs):
    if created:
        review_count = cache.get('review_count', 0)
        review_ids = cache.get('review_ids', [])

        review_ids.append(instance.id)
        review_count += 1

        cache.set('review_count', review_count)
        cache.set('review_ids', review_ids)

        if review_count >= 20:
            summary = trigger_summarization_model(review_ids)
            review_ids = ','.join(map(str, review_ids))
            Summary.objects.create(summary=summary, review_ids=review_ids)
            cache.set('review_count', 0)
            cache.set('review_ids', [])

def trigger_summarization_model(review_ids):
    reviews = Review.objects.filter(id__in=review_ids)
    comments = [review.comment for review in reviews if review.comment is not None]
    summary = AI_Engine.summarize(comments)
    return summary

#-------------------------------------------------------------
# Generation of AI Reports for PROBLEMS
@receiver(post_save, sender=Problem)
def track_problems(sender, instance, created, **kwargs):
    if created:
        problem = Problem.objects.get(id=instance.id)
        image = get_img_data_(problem.photo)
        description, title, authority, priority = AI_Engine.analyse_isuue(image)
        authority_name = 'City_council'
        subdivision = authority
        authority_object = Authority.objects.get(name=authority_name)
        ai_problem = AI_Problem.objects.create(
            report=problem,
            description=description,
            authority_name=authority_object,
            title=title,
            priority=priority,
            subdivision=subdivision if 'subdivision' in locals() else None,
        )
        nearest_location = find_nearest_authority_location(problem.coordinates, authority)
        Problem_Authority_Location.objects.create(problem=problem, authority_location=nearest_location)


#-------------------------------------------------------------
# Generation of AI Reports for EMERGENCIES
@receiver(post_save, sender=Emergency)
def emergencies_ai_reports(sender, instance, created, **kwargs):
    if created:
        emergency = Emergency.objects.get(id=instance.id)
        image = get_img_data_(emergency.photo)
        description, title, authority, level = AI_Engine.analyse_accident(image)
        if authority not in ['Fire_station', 'Hospital']:
            authority = 'Police'

        authority_object = Authority.objects.get(name=authority)
        ai_emergency = AI_Emergency.objects.create(
                report=emergency,
                description=description,
                title=title,
                authority_name=authority_object,
                danger_level=level
            )
        nearest_location = find_nearest_authority_location(emergency.coordinates, authority)
        Emergency_Authority_Location.objects.create(emergency=emergency, authority_location=nearest_location)


#-------------------------------------------------------------
# Helper functions
def euclidean_distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)

def find_nearest_authority_location(coordinates, authority):
    problem_lat, problem_lon = map(float, coordinates.split(','))
    authority_object = Authority.objects.get(name=authority)
    list_of_authorities = Authority_Locations.objects.filter(authority=authority_object)
    min_distance = float('inf')

    for authority in list_of_authorities:
        loc_lat, loc_lon = map(float, authority.coordinates.split(','))
        distance = euclidean_distance(problem_lat, problem_lon, loc_lat, loc_lon)
        if distance < min_distance:
            min_distance = distance
            nearest_authority = authority

    return nearest_authority

# Helper function to read image data from a file and encode it in base64 format
def get_img_data_(IMG_PATH):
    uni_path = os.path.join(BASE_DIR, 'media' , str(IMG_PATH))
    with open(str(uni_path), "rb") as image_file:
        image_data = image_file.read()
    image_data_b64 = base64.b64encode(image_data).decode("utf-8")
    return image_data_b64
