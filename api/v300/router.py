from ..utils.base_router import Router
from . import views


router = Router()
router.register(r'orbiters', views.OrbiterViewSet)
router.register(r'agencies', views.AgencyViewSet)
router.register(r'launchers', views.LaunchersViewSet)
router.register(r'events', views.EventViewSet)
router.register(r'launch/previous', views.PreviousLaunchViewSet, base_name='launch/previous')
router.register(r'launch/upcoming', views.UpcomingLaunchViewSet,  base_name='launch/upcoming')
router.register(r'launch', views.LaunchViewSet, base_name='launch')

api_urlpatterns = router.urls
