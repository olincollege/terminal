from PIL import Image

class Model:
    
    def __init__(self):
        self._player_name = "____"
    
class File:
    
    def __init__(self, name):
        self._name = name
        
    @property
    def name(self):
        return self._name
    
    def __repr__(self):
        pass
    
class TextFile(File):
    
    def __init__(self, filename):
        super().__init__(filename)
        with open(filename, "r") as f:
            self._contents = f.read()
        
    def __repr__(self):
        return self._contents

class ImageFile(File):
    
    def __init__(self, filename):
        super().__init__(filename)
        self._contents = Image.open(filename)
    
    def __repr__(self):
        self._contents.show()
