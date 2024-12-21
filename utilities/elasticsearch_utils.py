from elasticsearch import Elasticsearch
from datetime import datetime

class ElasticSearchUtility:
    def __init__(self, host='172.18.0.1', port=9200, scheme='http', index_name='automation-logs'):
        self.es = Elasticsearch('https://localhost:9200',
                                basic_auth=('', ''),
                                verify_certs=False
                                )
        self.index_name = index_name

    def create_index(self, index_settings=None):
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name, body=index_settings)

    def ingest_log(self, log_data):
        log_data['timestamp'] = datetime.now()
        self.es.index(index=self.index_name, body=log_data)

    def search_logs(self, query):
        return self.es.search(index=self.index_name, body=query)

    def delete_index(self):
        if self.es.indices.exists(index=self.index_name):
            self.es.indices.delete(index=self.index_name)


# Example usage
'''if __name__ == "__main__":
    es_utility = ElasticSearchUtility()

    # Create index with settings
    index_mapping = {
        "mappings": {
            "properties": {
                "timestamp": {
                    "type": "date"
                },
                "test_case_name": {
                    "type": "keyword"
                },
                "status": {
                    "type": "keyword"
                },
                "message": {
                    "type": "text"
                },
                "error_type": {
                    "type": "keyword"
                }
            }
        }
    }
    es_utility.create_index(index_settings=index_mapping)

    log_data = {
        "message": "Login test passed",
        "level": "INFO"
    }
    es_utility.ingest_log(log_data)

    # Search logs
    query = {
        "query": {
            "match": {
                "message": "Login"
            }
        }
    }
    logs = es_utility.search_logs(query)
    print(logs)'''