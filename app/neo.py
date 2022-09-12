from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
import logging
import sys

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logging.getLogger("neo4j").addHandler(handler)
logging.getLogger("neo4j").setLevel(logging.DEBUG)


class App:

    def __init__(self, uri:str, user:str, password:str)->None:
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    @staticmethod
    def _get_language(tx)->[]:
        query = (
            "MATCH (p:Language)"
            "RETURN p as Language"
        )
        result = tx.run(query)
        return [row["Language"]["name"] for row in result]

    @staticmethod
    def _get_flavour(tx)->[]:
        query = (
            "MATCH (p:flavour)"
            "RETURN p as Flavour"
        )
        result = tx.run(query)
        flavour_data = []
        for i in result:
            id = i["Flavour"]["flavourid"]
            flavour_data.append({"id":id,"name":i["Flavour"]["name"]})
        return flavour_data

    def get_api_data(self)->[]:
        result = []
        with self.driver.session(database="neo4j") as session:
            language_data = session.read_transaction(self._get_language)
            flavor_data = session.read_transaction(self._get_flavour)
        result.append({"Languages":language_data,"Flavour":flavor_data})
        return result




uri = "neo4j+s://2f0a4b5b.databases.neo4j.io"
user = "neo4j"
password = "Ur9KxrZHBmb4vt6fnVARljT3bPagQVl2McnoN6LgSWU"
client = App(uri, user, password)
