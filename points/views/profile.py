from django.shortcuts import render #type: ignore

import cloudinary #type: ignore

from points.models import Camper #type: ignore
from points.utils import create_profile #type: ignore


def profile(request, id):
    try:
        id, c = id.split('x', 1)
        camper = Camper.objects.get(pk=id)
    except:
        return render(request, 'points/profile.html', {
            'error': 'Error: Invalid Camper Id',
        })
    if not camper.last_name.startswith(c.upper()):
        return render(request, 'points/profile.html', {
            'error': 'Error: Camper not found',
        })
    if request.method == 'POST':
        # Configur Cloudinary
        cloudinary.config(
            cloud_name = "hujlg567i",
            api_key = "164342761484187",
            api_secret = "mbHeZXU3P6XHgf1WIQ1QuGuHJ0k",
            secure = True
        )
        pic = request.FILES['profile-pic-upload']
        cloudinary.uploader.upload(pic,
            public_id=f'camper-{camper.id}',
            folder='camper-pics',
            overwrite=True,
            invalidate=True,
            resource_type='image',
        )
        # get the url of uploaded image
        camper.profile_pic = cloudinary.CloudinaryImage(f'camper-pics/camper-{camper.id}').build_url()
        camper.save()
        
    c = create_profile(camper)

    return render(request, 'points/profile.html', {
        'camper': camper,
        'c': c,
        'id_str': f'{camper.id}x{camper.last_name[0]}',
    })
