import django.dispatch


affiliate_post_reward = django.dispatch.Signal(
    providing_args=["affiliate", "amount"])
affiliate_post_withdraw = django.dispatch.Signal(
    providing_args=['payment_request'])
