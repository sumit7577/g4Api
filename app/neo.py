from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable


class App:

    def __init__(self, uri: str, user: str, password: str) -> None:
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    @ staticmethod
    def _get_language(tx) -> []:
        query = (
            "MATCH (p:Language)"
            "RETURN p as Language"
        )
        result = tx.run(query)
        return [row["Language"]["name"] for row in result]

    @ staticmethod
    def _get_flavour(tx) -> []:
        query = (
            "MATCH (p:flavour)"
            "RETURN p as Flavour"
        )
        result = tx.run(query)
        flavour_data = [{"id": i["Flavour"]["flavourid"] or i["Flavour"]
                         ["flavourId"], "name": i["Flavour"]["name"]} for i in result]
        return flavour_data

    def get_api_data(self) -> []:
        result = []
        with self.driver.session(database="neo4j") as session:
            language_data = session.read_transaction(self._get_language)
            flavor_data = session.read_transaction(self._get_flavour)
            #ok = session.read_transaction(self.run_query)
        result.append({"Languages": language_data, "Flavour": flavor_data})
        return result

    def insert_data(self,id:str,language:str,flavour:str,fileName:str):
        with self.driver.session(database="neo4j") as session:
            session.read_transaction(self._run_query,id,language,flavour,fileName)


    @staticmethod
    def _run_query(tx, id="de403879-019d-43f4-bf29-fb32c470d177", language="English",flavour="something",fileName="test.mp4"):
        time_update_query = """MATCH (v:video {flavourId:$id,language: $language}),
                    (h:history{flavourId:$id}),
                    (f:flavour{flavourId:$id})
                    MERGE (h)-[:UPDATED_DATE]->(v)
                    RETURN *"""
        del_video_query = """MATCH (v:video {flavourId:$id,language: $language}),
                            (h:history{flavourId:$id}),
                            (f:flavour{flavourId:$id})
                            MATCH (f)-[r:HAS_VIDEO]->(v)
                            DELETE r
                            REMOVE v:video
                            SET v:video_history
                            RETURN *"""
        create_video_query = """CREATE f1= ( Fanta_Frozen_Blue_Raspberry_Landscape_EN : video { name:'Video', video_name:$filename,language:$language,
                                video_url:"https://cdn.shopify.com/s/files/1/0256/3247/3170/products/ROBINSONS_ALL_PRODUCTS_600x600px.png?v=1648696493",videoStatus:"CurrentVideo"
                                ,flavourId: $id})
                                RETURN *"""
        final_query = """MATCH (v:video {flavourId:$id,language: $language}),
                        (f:flavour{flavourId:$id}),
                        (l:Language{name: $language})
                        MERGE (f)-[:HAS_VIDEO]->(v)
                        MERGE (v)-[:HAS_LANGUAGE]->(l)
                        RETURN *"""
        result = tx.run(time_update_query, {"id": id, "language": language})
        result2 = tx.run(del_video_query, {"id": id, "language": language})
        result3 = tx.run(create_video_query, {"id": id, "language": language,"filename":fileName})
        result4 = tx.run(final_query, {"id": id, "language": language})
        return True

uri = "neo4j+s://2f0a4b5b.databases.neo4j.io"
user = "neo4j"
password = "Ur9KxrZHBmb4vt6fnVARljT3bPagQVl2McnoN6LgSWU"
client = App(uri, user, password)
