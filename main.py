from scripts.REPO.eventsRepo import EventsRepo
from scripts.REPO.wallpapersRepo import WallpapersRepo
from scripts.DOMAIN.event import Event
from scripts.DOMAIN.wallpaper import Wallpaper
from scripts.service import Service
from scripts.ui import UI
from scripts.DOMAIN.validator import Validator
from scripts.renderer.textRenderer import TextRenderer
from scripts.system.wallpaperSys import WallpaperSys
from scripts.services.eventsService import EventService
from scripts.services.wallpaperService import WallpaperService
import os

ui = UI(Service(EventService(EventsRepo(os.path.join("data", "events.txt")), Validator(), Event), WallpaperService(WallpapersRepo()), WallpaperSys(), TextRenderer()))
ui.run()