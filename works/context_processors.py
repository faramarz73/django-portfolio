from .models import Profile, SocialLink


def site_info(request):
    return {"profile": Profile.objects.first(), "socials": SocialLink.objects.all()}
