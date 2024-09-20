from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache  # Using cache to store the review count
from .models import Review, Summary

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Review
from Radary_AI import summarizer




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

        # Check if count reached 15
        if review_count >= 10:
            summary = trigger_summarization_model(review_ids)
            review_ids = ','.join(map(str, review_ids))
            Summary.objects.create(summary=summary, review_ids=review_ids)
            cache.set('review_count', 0)
            cache.set('review_ids', [])

def trigger_summarization_model(review_ids):
    reviews = Review.objects.filter(id__in=review_ids)

    comments = [review.comment for review in reviews if review.comment is not None]
    summary = summarizer.summarize(comments)
    return summary




