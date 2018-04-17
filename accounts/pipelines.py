from django.contrib.auth.models import User


# Setting avatar after OAuth Login
def saveAvatar(backend, strategy, details, response,
        user=None, *args, **kwargs):
    url = None
    if backend.name == 'google-oauth2':
        url = response['image'].get('url')
        ext = url.split('.')[-1]
    if url:
        user = User.objects.get(username=details['username'])
        user.profile.avatar = url
        user.save()