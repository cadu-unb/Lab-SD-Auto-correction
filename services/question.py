import warnings

class question:
    def __init__(self, id, body, entries, image_path = ''): 
        self.id = id
        self.body = body.format(entries)
        self.image_path = image_path    
    def __eq__(self, otherQuestion):
        if type(otherQuestion) != question:
            warnings.warn('Objects need to be of type <question> to be compared.')
            return False
        if self.body == otherQuestion.body:
            warnings.warn('Objects need to be of type <question> to be compared.')
            
if __name__ == "__main__":
    