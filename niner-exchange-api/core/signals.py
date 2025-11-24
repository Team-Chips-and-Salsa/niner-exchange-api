from django.db.models import Avg, F
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from .models import Listing

from .models.review import Review
from .models.user import CustomUser


# Used AI to build the signal workflow for updating user ratings and sold items count
def update_user_ratings(reviewee_id):
    try:
        user = CustomUser.objects.get(id=reviewee_id)

        user_reviews = user.reviews_received.filter(status="ACTIVE")

        new_count = user_reviews.count()
        new_avg = user_reviews.aggregate(Avg("rating"))["rating__avg"]

        user.review_count = new_count
        user.avg_rating = new_avg

        user.save(update_fields=["review_count", "avg_rating"])

    except CustomUser.DoesNotExist:
        pass


@receiver(post_save, sender=Review)
def on_review_save(sender, instance, **kwargs):
    update_user_ratings(instance.reviewee.id)


@receiver(post_delete, sender=Review)
def on_review_delete(sender, instance, **kwargs):
    update_user_ratings(instance.reviewee.id)


@receiver(pre_save, sender=Listing)
def store_old_listing_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_status = Listing.objects.get(pk=instance.pk).status
        except Listing.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = "NEW"


@receiver(post_save, sender=Listing)
def on_listing_sold(sender, instance, created, **kwargs):
    if not created:
        old_status = getattr(instance, "_old_status", None)

        if old_status != "SOLD" and instance.status == "SOLD":

            seller = instance.seller
            if seller:
                seller.items_sold_count = F("items_sold_count") + 1
                seller.save(update_fields=["items_sold_count"])
