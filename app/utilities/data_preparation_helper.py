class DataPreparationHelper():
    def prepare_response_for_data_store(self, response, number_of_response_fragments):
        prepared_response = ""

        if number_of_response_fragments > 1:
            for response_index in range(0, number_of_response_fragments):
                prepared_response = prepared_response + response[response_index]
        else:
            prepared_response = response
        
        return prepared_response