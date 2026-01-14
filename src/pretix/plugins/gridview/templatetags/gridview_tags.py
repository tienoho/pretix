from django import template
from django.db.models import Min
from pretix.base.models import Item

register = template.Library()

@register.simple_tag
def get_event_min_price(event):
    """Returns the minimum price for an event based on its active items."""
    # We filter by active items that have a default_price set
    qs = Item.objects.filter(
        event=event, 
        active=True,
        default_price__isnull=False
    )
    # Check if there are any items before aggregating
    if not qs.exists():
        # Fallback to variations if no top-level price
        # This is a bit more complex, but for MVP we might stick to simple items or expand logic
        return None
        
    result = qs.aggregate(min_price=Min('default_price'))
    return result['min_price']

@register.simple_tag
def get_event_logo(event):
    """Returns the logo URL for an event, compatible with how template tags should work."""
    # event.settings is a hierarchical settings object
    try:
        logo = event.settings.get('logo_image', as_type=str, default='')
        if logo and logo.startswith('file://'):
            return logo[7:]  # Remove 'file://' prefix
        return logo or ''
    except Exception:
        return ''

@register.simple_tag
def get_event_currency(event):
    """Returns the currency code for an event."""
    return event.currency
