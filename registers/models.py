import random

from django.contrib.auth.models import User

from registers.utils.constants import COUNTRIES
from .utils.language_codes import LANGUAGES
from django.db import models
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from .utils.constants import PlanType, PLAN_CHOICES


class Shop(models.Model):
    SCRIPT_TAG = 'ST'
    THEME = 'T'
    RECEIVE_REQUEST = 'RR'
    SHOW_REQUEST = 'SR'
    EMOJI_FEEDBACK = 'EF'
    GOTO_REVIEW = 'GR'
    WRITE_REVIEW = 'WR'
    COMPLETE = 'C'
    ACTIVE = 'A'
    LOCKED = 'L'
    FROZEN = 'FR'
    FORBIDDEN = 'FO'  # scope approval needed

    SCOPE_VERSION_CHOICES = [
        (1, 'v1'),
        (2, 'v2'),
        (3, 'v3'),
    ]
    INJECTION_METHOD_CHOICES = [
        (SCRIPT_TAG, 'ScriptTag'),
        (THEME, 'Theme'),
    ]
    REVIEW_STEP_CHOICES = [
        (RECEIVE_REQUEST, _('Receive Request')),
        (SHOW_REQUEST, _('Show Request')),
        (EMOJI_FEEDBACK, _('Emoji Feedback')),
        (GOTO_REVIEW, _('Goto Review')),
        (WRITE_REVIEW, _('Write Review')),
        (COMPLETE, _('Complete')),
    ]
    STATUS_CHOICES = [
        (ACTIVE, _('Active')),
        (LOCKED, _('Locked')),
        (FROZEN, _('Frozen')),
        (FORBIDDEN, _('Forbidden')),
    ]

    shopify_id = models.BigIntegerField(null=True, blank=True)
    shopify_domain = models.CharField(null=True, blank=True, max_length=200, unique=True)
    token = models.CharField(null=True, blank=True, max_length=200)
    script_id = models.BigIntegerField(null=True, blank=True)
    scope_version = models.SmallIntegerField(choices=SCOPE_VERSION_CHOICES, default=1)
    is_scope_approved = models.BooleanField(default=False)
    injection_method = models.CharField(max_length=3, choices=INJECTION_METHOD_CHOICES, default=SCRIPT_TAG)
    is_test = models.BooleanField(default=False)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=ACTIVE)

    name = models.CharField(max_length=256, null=True)
    owner = models.CharField(max_length=256, null=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    contact_email = models.EmailField(null=True)
    domain = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=2, choices=list(COUNTRIES.items()), null=True)
    city = models.CharField(max_length=50, null=True)
    timezone = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(null=True)
    cookie_consent_level = models.CharField(max_length=64, null=True)
    visitor_tracking_consent_preference = models.CharField(max_length=64, null=True)
    shopify_plan = models.CharField(max_length=60, null=True, blank=True)
    theme = models.CharField(max_length=200, null=True, blank=True)
    theme_id = models.IntegerField(null=True, blank=True)

    primary_locale = models.CharField(max_length=20, null=True, blank=True)
    custom_locale = models.CharField(max_length=20, null=True, blank=True, choices=LANGUAGES)

    currency = models.CharField(max_length=64, null=True)
    currency_format = models.CharField(max_length=1024, default='$%s')

    icon = models.URLField(null=True, blank=True)
    logo = models.URLField(null=True, blank=True)
    custom_logo = models.ImageField(_('Custom logo'), upload_to='shop_logo/', null=True, blank=True)

    # application = models.OneToOneField(Application, on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    plan = models.CharField(max_length=5, choices=PLAN_CHOICES, default=PlanType.FREE.value)
    send_locked = models.BooleanField(default=False)

    templates_added = models.BooleanField(default=False)
    hengam_orders_update_time = models.DateTimeField(null=True, blank=True)
    review_step = models.CharField(max_length=3, choices=REVIEW_STEP_CHOICES, null=True, blank=True)
    has_button_injection_issue = models.BooleanField(default=False)
    has_seen_wizard = models.BooleanField(default=False)
    has_seen_welcome_box = models.BooleanField(default=False)

    from_email = models.CharField(max_length=200, null=True, blank=True,
                                  help_text=escape('e.g. Back in Stock Notification <notify@backin.store>'))
    report_email = models.EmailField(null=True, blank=True)
    is_from_email_verified = models.BooleanField(null=True, blank=True)
    reply_email = models.CharField(max_length=200, null=True, blank=True,
                                   help_text=escape('e.g. Back in Stock Notification <notify@backin.store>'))
    contact_list_enable = models.BooleanField(default=False)
    accept_subscription_admin_decision = models.BooleanField(null=True, blank=True, default=True)

    hubspot_company_id = models.BigIntegerField(null=True, blank=True)
    hubspot_contact_id = models.BigIntegerField(null=True, blank=True)

    automatic_injection = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.shopify_domain}'

