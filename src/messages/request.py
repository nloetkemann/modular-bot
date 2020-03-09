class Request:
    all = {}  # a place to store all data
    type = 'text'  # the type of the request (text, voice, document)
    user = ''  # username
    chat_id = ''  # the id, important for answering

    def is_text(self):
        return self.type == 'text'

    def is_voice(self):
        return self.type == 'voice'

    def is_document(self):
        return self.type == 'document'

    def get_user(self):
        return self.user

    def get_chat_id(self):
        return self.chat_id

    def get_type(self):
        return self.type

    def get_text(self):
        raise NotImplementedError('The get_text method has not been implemented ' + str(self.__class__))

    def is_callback(self):
        raise NotImplementedError('The is_callback method has not been implemented ' + str(self.__class__))

    def get_file_id(self):
        raise NotImplementedError('The get_file_id method has not been implemented ' + str(self.__class__))

    def is_command(self):
        raise NotImplementedError('The is_command method has not been implemented ' + str(self.__class__))

    def get_attr(self, attribute, where=None):
        raise NotImplementedError('The get_attr method has not been implemented ' + str(self.__class__))
