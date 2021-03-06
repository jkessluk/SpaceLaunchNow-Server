from api.v340.agencies.views import AgencyViewSet
from api.v340.astronaut.views import AstronautViewSet
from api.v340.config.launcher.views import LauncherConfigViewSet
from api.v340.config.spacecraft.views import SpacecraftConfigViewSet
from api.v340.docking_event.views import DockingEventViewSet
from api.v340.events.views import EventViewSet, PreviousEventViewSet, UpcomingEventViewSet
from api.v340.expedition.views import ExpeditionViewSet
from api.v340.launch.views import PreviousLaunchViewSet, UpcomingLaunchViewSet, LaunchViewSet
from api.v340.launcher.views import LauncherViewSet
from api.v340.spacecraft.flight.views import SpaceflightFlightViewSet
from api.v340.spacecraft.views import SpacecraftViewSet
from api.v340.spacestation.views import SpaceStationViewSet
from ..utils.base_router import Router


router = Router()
router.register(r'agencies', AgencyViewSet, base_name='agency')
router.register(r'astronaut', AstronautViewSet, base_name='astronaut')
router.register(r'config/launcher', LauncherConfigViewSet)
router.register(r'config/spacecraft', SpacecraftConfigViewSet)
router.register(r'docking_event', DockingEventViewSet)
router.register(r'event/previous', PreviousEventViewSet, base_name='events/previous')
router.register(r'event/upcoming', UpcomingEventViewSet, base_name='events/upcoming')
router.register(r'event', EventViewSet, base_name='events')
router.register(r'expedition', ExpeditionViewSet, base_name='expedition')
router.register(r'launch/previous', PreviousLaunchViewSet, base_name='launch/previous')
router.register(r'launch/upcoming', UpcomingLaunchViewSet,  base_name='launch/upcoming')
router.register(r'launch', LaunchViewSet, base_name='launch')
router.register(r'launcher', LauncherViewSet, base_name='launcher')
router.register(r'spacestation', SpaceStationViewSet, base_name='spacestation')
router.register(r'spacecraft/flight', SpaceflightFlightViewSet, base_name='spacecraftflight')
router.register(r'spacecraft', SpacecraftViewSet, base_name='spacecraft')

api_urlpatterns = router.urls
