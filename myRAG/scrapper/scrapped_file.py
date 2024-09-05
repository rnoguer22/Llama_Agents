class ScrappedFile:

    def __init__(self, path) -> None:
        self.name = self.get_name(path)

    def get_name(self, path):
        name = path[8:].replace('.', '_')
        name = name.replace('/', '_')
        if name.endswith('_'):
            name = name[:-1]
        return name + '.txt'
    

scrap = ScrappedFile('https://www.techwithtim.net/')
print(scrap.name)