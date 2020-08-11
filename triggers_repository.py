import mysql.connector
from mysql.connector import errorcode

class TriggersRepository:
    def __init__(self, conversationId):
        self._connection = self.__get_connection()
        self._conversation_id = conversationId
        self._response_query = "select t.Response, t.TriggerId from `Trigger` t inner join Synonym s on t.TriggerId = s.TriggerId where s.SynonymPhrase like '%%%s%%' and not exists (select 1 from ResponseAlreadyUsed r where r.TriggerId = t.TriggerId and r.ConversationId = %s) LIMIT 1;"
        self._encouraging_noise_query = "test2"
        self._insert_response_already_used_query = "test3"


    def __get_connection(self):
        config = {'user': 'talkitoverchatbot', 'password': 'vFA68xqGFaJ4kvSK', 'host': 'talkitoverchatbot.mysql.pythonanywhere-services.com', 'database': 'talkitoverchatbot$TalkItOver', 'raise_on_warnings': True}

        try:
            connection = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your database configuration")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        
        return connection

    def handle_message(self, usersMessage):
        response = self.__get_response(usersMessage)
        if not response:
            response = self.__get_encouraging_noise()
        else:
            self.__insert_response_already_used_record(response[1])
        return response[0]

    def __get_response(self, usersMessage):
        cursor = self._connection.cursor(prepared=True)
        cursor.execute(self._response_query, (usersMessage, self._conversation_id))
        response = cursor.fetchone()
        return response

    def __get_encouraging_noise(self):
        cursor = self._connection.cursor()
        cursor.execute(self._encouraging_noise_query)
        response = cursor.fetchone()
        return response

    def __insert_response_already_used_record(self, triggerId):
        cursor = self._connection.cursor()
        cursor.execute(self._insert_response_already_used_query, (self._conversation_id, triggerId))   