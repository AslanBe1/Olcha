from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from olcha.models import Order, Comment, Product
from django.utils.timezone import now
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def order_created_handler(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New Order created: {instance.id} at {now()}")


@receiver(post_save, sender=Comment)
def update_product_rating_on_comment(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        comments = product.comment_set.all()
        avg_rating = sum([c.rating for c in comments]) / comments.count()
        product.rating = avg_rating
        product.save()
        logger.info(f"Updated product ({product.id}) average rating to {avg_rating}")


@receiver(post_delete, sender=Comment)
def update_product_rating_on_comment_delete(sender, instance, **kwargs):
    product = instance.product
    comments = product.comment_set.all()
    if comments.exists():
        avg_rating = sum([c.rating for c in comments]) / comments.count()
    else:
        avg_rating = 0
    product.rating = avg_rating
    product.save()
    logger.info(f"Updated product ({product.id}) rating after comment deleted to {avg_rating}")
