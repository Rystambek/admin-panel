import json
#Create Like counting class
class DB:
    def __init__(self, db_path):
        #Initialize the database
        #Open the database file if it exists, otherwise create a new database file
        self.db_path = db_path
        try:
            with open(db_path, 'r') as f:
                self.db = json.load(f)
        except FileNotFoundError:
            self.db = {}
            #Save the database to the database file
            with open(db_path, 'w') as f:
                json.dump(self.db, f, indent=4)
    
    def starting(self,chat_id,user_name):
        if  ("chat_id" not in self.db.get('Users').keys()):
            self.db['Users'][f"{chat_id}"] = {"lang":'Uz'}
            self.db['Users'][f"{chat_id}"]['fist_name']=user_name
        return None

    def save(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.db, f, indent=4)

    def db(self):
        return self.db
    
    def add_lang(self,chat_id,lang):
        self.db['Users'][chat_id]['lang']=lang

    def get_lang(self,chat_id):
        return self.db['Users'][f'{chat_id}']['lang']
    
    def obuna(self,chat_id):
        return self.db['Users'][chat_id]['obuna']
    
    def get_channel(self):
        return self.db['chanel']['1'],self.db['chanel']['2']
    
    def add_chan(self,chan1,chan2):
        self.db['chanel']['1']=chan1
        self.db['chanel']['2']=chan2
        return 'Ok'
    