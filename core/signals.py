from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Review, Summary, Problem, AI_Problem, Authority, Emergency, AI_Emergency
from Radary_AI import main as AI_Engine
import base64
from django.conf import settings
import os

BASE_DIR  = settings.BASE_DIR
BASE_DIR_MEDIA = os.path.join(BASE_DIR, 'media')
@receiver(post_save, sender=Review)
def track_reviews(sender, instance, created, **kwargs):
    if created:
        # Get current review count and IDs from the cache
        review_count = cache.get('review_count', 0)
        review_ids = cache.get('review_ids', [])

        # Add the new review ID to the list
        review_ids.append(instance.id)
        review_count += 1

        # Save updated review count and IDs to the cache
        cache.set('review_count', review_count)
        cache.set('review_ids', review_ids)

        # Check if count reached 20
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
        # Get current problem count and IDs from the cache
        problem_count = cache.get('problem_count', 0)
        problem_ids = cache.get('problem_ids', [])

        # Add the new problem ID to the list
        problem_ids.append(instance.id)
        problem_count += 1

        # Save updated problem count and IDs to the cache
        cache.set('problem_count', problem_count)
        cache.set('problem_ids', problem_ids)

        # Check if count reached 10
        if problem_count >= 10:
            process_problems_with_ai(problem_ids)
            # Reset cache
            cache.set('problem_count', 0)
            cache.set('problem_ids', [])

def process_problems_with_ai(problem_ids):
    # Fetch the 10 problems from the database
    problems = Problem.objects.filter(id__in=problem_ids)

    for problem in problems:
        # Send each problem's description to the AI engine and get the response
        UNI_PATH = os.path.join(BASE_DIR, 'media' , str(problem.photo))
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


# Helper function to read image data from a file and encode it in base64 format
def get_img_data_(IMG_PATH):
    uni_path = os.path.join(BASE_DIR, 'media' , str(IMG_PATH))
    with open(str(uni_path), "rb") as image_file:
        image_data = image_file.read()
    image_data_b64 = base64.b64encode(image_data).decode("utf-8")
    return image_data_b64


#-------------------------------------------------------------
# Generation of AI Reports for EMERGENCIES
@receiver(post_save, sender=Emergency)
def emergencies_ai_reports(sender, instance, created, **kwargs):
    if created:
        process_emergencies_with_ai(instance.id)

def process_emergencies_with_ai(emergency_ids):
    emergencies = Emergency.objects.filter(id__in=emergency_ids)

    for emergency in emergencies:
        UNI_PATH =  os.path.join(BASE_DIR, 'media' , str(emergency.photo))
        image = get_img_data_(emergency.photo)
        description, title, authority, level = AI_Engine.analyse_accident(image)
        if authority not in ['Fire_station', 'Hospital']:
            authority = 'Police'

        authority_object = Authority.objects.get(name=authority)
        ai_emergency = AI_Emergency.objects(
                report=emergency,
                description=description,
                title=title,
                authority_name=authority_object,
                danger_level=level
            )
