from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(user, user_type):
    subject = f"Welcome to LandMarket, {user.first_name}!"
    message = f"""
Hi {user.first_name},

Welcome to LandMarket! Your {user_type} account has been created successfully.

{"You can now start listing your lands for sale." if user_type == "vendor" else "You can now browse and save land listings."}

Visit us at: http://127.0.0.1:8000

Best regards,
LandMarket Team
"""
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    except:
        pass  # Don't crash if email fails


def send_wishlist_notification(vendor_user, buyer_user, land):
    subject = f"Someone saved your listing: {land.title}"
    message = f"""
Hi {vendor_user.first_name},

Good news! {buyer_user.get_full_name() or buyer_user.username} just saved your land listing to their wishlist.

Listing: {land.title}
Location: {land.city}, {land.state}
Price: ₹{land.price}

They may contact you soon!

Best regards,
LandMarket Team
"""
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [vendor_user.email])
    except:
        from django.core.mail import send_mail
        from django.conf import settings


def send_welcome_email(user, user_type):
    subject = f"Welcome to LandMarket, {user.first_name}!"
    message = f"""
Hi {user.first_name},

Welcome to LandMarket! Your {user_type} account has been created successfully.

{"You can now start listing your lands for sale." if user_type == "vendor" else "You can now browse and save land listings."}

Visit us at: http://127.0.0.1:8000

Best regards,
LandMarket Team
"""
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    except:
        pass  # Don't crash if email fails


def send_wishlist_notification(vendor_user, buyer_user, land):
    subject = f"Someone saved your listing: {land.title}"
    message = f"""
Hi {vendor_user.first_name},

Good news! {buyer_user.get_full_name() or buyer_user.username} just saved your land listing to their wishlist.

Listing: {land.title}
Location: {land.city}, {land.state}
Price: ₹{land.price}

They may contact you soon!

Best regards,
LandMarket Team
"""
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [vendor_user.email])
    except:
        pass