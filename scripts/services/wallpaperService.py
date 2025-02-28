class WallpaperService:
    def  __init__(self, repo):
        self.__repo = repo

    def get_wallpapers(self):
        '''
        Function that returns all the available wallpapers
        
        Raises:
            WallpapersRepoError: if there are no stored existing wallpapers yet
        '''

        return self.__repo.get__wallpapers()