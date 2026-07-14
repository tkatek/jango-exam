from core.models import Alert


def notifications_context(request):
    context = {}
    if request.user.is_authenticated:
        unread_alerts = Alert.objects.filter(is_read=False)
        context['unread_alerts_count'] = unread_alerts.count()
        context['unread_alerts'] = unread_alerts[:5]
    return context
