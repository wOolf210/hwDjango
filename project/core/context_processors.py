from .models import Post


def posts(request):
    return {'posts': Post.objects.all()}

def site_info(request):
    return {
        'site_name': 'My Awesome Site',
        'site_description': 'This is a sample site for demonstration purposes.',
        'site_version': '1.0.0',
    }