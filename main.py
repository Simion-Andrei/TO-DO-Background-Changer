from scripts.REPO.eventsRepo import EventsRepo
from scripts.REPO.wallpapersRepo import WallpapersRepo
from scripts.DOMAIN.event import Event
from scripts.DOMAIN.wallpaper import Wallpaper
from scripts.service import Service
from scripts.ui import UI
from scripts.DOMAIN.validator import Validator

ui = UI(Service(Validator(), EventsRepo("data/events.txt"), WallpapersRepo(), Event, Wallpaper))
ui.run()