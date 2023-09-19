class Dict_to_SQL:
    def __init__(self, table_name, mapper : dict) -> None:
        self.table_name = table_name
        self.mapper = mapper
        
        self.__first_segment, self.__func_other_segment = self.__make_insert_query()
    
    def __get_key_name(self, dictionary, colum_name):
        if colum_name not in dictionary: return ""
        return dictionary[colum_name]
    
    def __partial_get_key_name(self, key):
        def get_key_name_without_json(json):
            return self.__get_key_name(json, key)
        return get_key_name_without_json

    def __factory_inject_param(self, param):
        def inject_param(func : callable):
            return func(param)
        return inject_param

    # 1. 쿼리의 첫 문장과 - "Insert Into `table_name` (...column_name) Values"
    # 2. 그 이외 문자의 Unit을 - "(...column_data)"
    # 생성하는 함수를 
    # 출력함.  
    def __make_insert_query(self):
        query_insert, query_data = [], []
        
        for key, val in self.mapper.items():
            query_insert.append(key)
            query_data.append(val)
        
        first_sentence = ', '.join(query_insert)
        other_sentence = lambda json : ', '.join(map(self.__wrap, map(self.__factory_inject_param(json), map(self.__partial_get_key_name, query_data))))
        
        return (
            f"INSERT INTO `{self.table_name}` ({first_sentence}) VALUES",
            lambda json : f"({other_sentence(json)})"
        )
    
    def __wrap(self, data):
        return f"'{str(data)}'"
    
    
    def __first_query(self):
        return self.__first_segment
    
    def __second_query(self, query):
        return f" {query}"

    def __other_query(self, query):
        return f" ,{query}"

    def iter_query(self, iter_dict):
        yield self.__first_query()
        yield self.__second_query(self.__func_other_segment(next(iter_dict)))
        yield from map(self.__other_query, map(self.__func_other_segment, iter_dict))
        yield ";"
    
    def make_query(self, iter_dict):
        return "".join(self.iter_query(iter_dict))
    

if __name__ == "__main__":
    member_mapper = {
        "id": "id",
        "email": "email",
        "nickname": "nickname",
        "password": "password",
    }
    
    member = [
        {
        "nickname": "nick",
        "id": 1,
        "email": "rladydqls99@naver.com",
        "password": 1234
        },
        {
        "nickname": "rasd",
        "email": "rlaydld@asd.com",
        "password": "1234",
        "id": 2
        }
    ]
    
    reduce_to_sql = Dict_to_SQL("member", member_mapper)

    it = iter(member)
    sql = reduce_to_sql.make_query(it)

    sql = """
        INSERT INTO `member` (id, email, nickname, password) VALUES (1, rladydqls99@naver.com, nick, 1234) ,(2, rlaydld@asd.com, rasd, 1234);
    """
    
    print(sql)
    