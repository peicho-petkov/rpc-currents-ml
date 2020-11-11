class dbTable:
    def __init__(self,tablename):
        self.tablename=str(tablename)
        self.colls={}
    def add_coll(self,colname,coltype):
        self.colls[str(colname)]=str(coltype)
    def del_coll(self,colname):
        del self.colls[str(colname)]
    def get_myqsl_create_query(self):
        query='CREATE TABLE {} ('.format(self.tablename)
        for colname, coltype in self.colls.items():
            query = "{} {} {},".format(query,colname,coltype)
        query=query+')'
        return query
