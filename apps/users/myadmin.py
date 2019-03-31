from myadmin.service.myadmin import site
from users import models

site.register(models.UserProfile)
