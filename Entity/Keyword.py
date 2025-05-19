class Keyword(): 
    def __init__(self, keyword_id, keyword, manager_id):
        self.keyword_id = keyword_id
        self.keyword = keyword
        self.manager_id = manager_id
    
    def __repr__(self):
        return f"Keyword(id={self.keyword_id}, keyword={self.keyword}, manager_id= {self.manager_id})"
    
    
    