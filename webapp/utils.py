from django.utils import timezone
def upload_directory_path(instance, filename):
    today = timezone.now().date().strftime("%Y-%m-%d")
    return '{}/{}/{}'.format(instance.semester.__str__().replace(" ", "_"),today,filename)
