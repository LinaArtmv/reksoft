import psycopg2

from reksoft.request import Request
from reksoft.response import Response

db_host = 'db'
db_port = 5432
db_name = 'reksoft'
db_user = 'linaart'
db_password = 123456


class View:

    def __init__(self, db_name):
        self.conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS resource_types (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                max_speed NUMERIC NOT NULL)''')

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS resources (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                current_speed NUMERIC NOT NULL,
                type_id INTEGER,
                FOREIGN KEY (type_id) REFERENCES resource_types(id))''')

        self.conn.commit()

    def get(self, request: Request, *args, **kwargs) -> Response:
        pass

    def post(self, request: Request, *args, **kwargs) -> Response:
        pass

    def put(self, request: Request, *args, **kwargs) -> Response:
        pass

    def delete(self, request: Request, *args, **kwargs) -> Response:
        pass

    def create_resource_type(self, name, max_speed):
        self.cursor.execute(
            '''INSERT INTO resource_types (name, max_speed)
                VALUES (%s, %s)''', (name, max_speed))
        self.conn.commit()
        return self.get_one_type(name, max_speed)

    def create_resource(self, name, current_speed, type_id):
        self.cursor.execute(
            '''INSERT INTO resources (name, current_speed, type_id)
                VALUES (%s, %s, %s)''', (name, current_speed, type_id))
        self.conn.commit()
        return self.get_one_resource(name, current_speed, type_id)

    def get_one_type(self, name, max_speed):
        self.cursor.execute(
            '''SELECT * FROM resource_types
                WHERE name=%s AND max_speed=%s''', (name, max_speed))
        result = self.cursor.fetchone()
        if result is None:
            return None
        type_result = {
            "id": result[0],
            "name": result[1],
            "max_speed": result[2]
        }
        self.close()
        return type_result

    def get_one_resource(self, name, current_speed, type_id):
        self.cursor.execute(
            '''SELECT resources.id, resources.name,
                resources.current_speed, resource_types.name,
                resources.type_id, resource_types.max_speed,
                ROUND((resources.current_speed / resource_types.max_speed
                 * 100 - 100)::numeric, 0) AS over_speed
                FROM resources
                INNER JOIN resource_types ON
                resources.type_id = resource_types.id
                WHERE resources.name=%s AND current_speed=%s
                AND type_id=%s''', (name, current_speed, type_id))
        result = self.cursor.fetchone()
        if result is None:
            return None
        type_result = {
            "id": result[0],
            "name": result[1],
            "current_speed": result[2],
            "type": result[3],
            "over_speed": result[6]
        }
        self.close()
        return type_result

    def get_id_type(self, id: int):
        self.cursor.execute(
            '''SELECT * FROM resource_types WHERE id=%s''', (id))
        result = self.cursor.fetchone()
        if result is None:
            return None
        type_result = {
            "id": result[0],
            "name": result[1],
            "max_speed": result[2]
        }
        self.close()
        return type_result

    def get_id_resource(self, id: int):
        self.cursor.execute(
            '''SELECT resources.id, resources.name, resources.current_speed,
                resource_types.name, resources.type_id,
                resource_types.max_speed,
                ROUND((resources.current_speed / resource_types.max_speed
                * 100 - 100)::numeric, 0) AS over_speed
                FROM resources
                INNER JOIN resource_types ON
                resources.type_id = resource_types.id
                WHERE resources.id=%s''', (id, ))
        result = self.cursor.fetchone()
        if result is None:
            return None
        type_result = {
            "id": result[0],
            "name": result[1],
            "current_speed": result[2],
            "type": result[3],
            "over_speed": result[6]
        }
        self.close()
        return type_result

    def get_all_type(self):
        self.cursor.execute(
            '''SELECT * FROM resource_types''')
        results = self.cursor.fetchall()
        if results is None:
            return None
        resource_types = []
        for result in results:
            type = {
                "id": result[0],
                "name": result[1],
                "max_speed": result[2]
            }
            resource_types.append(type)
        self.close()
        return resource_types

    def update_resource_type(self, id, name, max_speed):
        self.cursor.execute(
            '''UPDATE resource_types SET name=%s, max_speed=%s
                WHERE id=%s''', (name, max_speed, id))
        self.conn.commit()
        return self.get_one_type(name, max_speed)

    def update_resource(self, id, name, current_speed, type_id):
        self.cursor.execute(
            '''UPDATE resources SET name=%s, current_speed=%s, type_id=%s
                WHERE id=%s''', (name, current_speed, type_id, id))
        self.conn.commit()
        return self.get_one_resource(name, current_speed, type_id)

    def delete_resource_type(self, id):
        self.cursor.execute(
            '''DELETE FROM resource_types WHERE id=%s''', (id))
        self.conn.commit()
        self.close()
        return 'Успешное удаление'

    def delete_resource(self, id):
        self.cursor.execute(
            '''DELETE FROM resources WHERE id=%s''', (id))
        self.conn.commit()
        self.close()
        return 'Успешное удаление'

    def mass_delete_resources(self, array):
        query = '''DELETE FROM resources
                    WHERE id IN ({})'''.format(','.join(['%s'] * len(array)))
        self.cursor.execute(query, array)
        self.conn.commit()
        self.close()
        return 'Успешное удаление'

    def mass_delete_types(self, array):
        query = '''DELETE FROM resource_types
                    WHERE id IN ({})'''.format(','.join(['%s'] * len(array)))
        self.cursor.execute(query, array)
        self.conn.commit()
        self.close()
        return 'Успешное удаление'

    def get_all_resources(self):
        self.cursor.execute(
            '''SELECT resources.id, resources.name, resources.current_speed,
                resource_types.name, resources.type_id,
                resource_types.max_speed,
                ROUND((resources.current_speed / resource_types.max_speed
                * 100 - 100)::numeric, 0) AS over_speed
                FROM resources
                INNER JOIN resource_types
                ON resources.type_id = resource_types.id''')
        results = self.cursor.fetchall()
        if results is None:
            return None
        resources = []
        for result in results:
            resource = {
                "id": result[0],
                "name": result[1],
                "current_speed": result[2],
                "type": result[3],
                "over_speed": result[6]
            }
            resources.append(resource)
        self.close()
        return resources

    def get_all_resources_type(self, type):
        self.cursor.execute(
            '''SELECT resources.id, resources.name, resources.current_speed,
                resource_types.name, resources.type_id,
                resource_types.max_speed,
                ROUND((resources.current_speed / resource_types.max_speed
                * 100 - 100)::numeric, 0) AS over_speed
                FROM resources
                INNER JOIN resource_types
                ON resources.type_id = resource_types.id
                WHERE resources.type_id=%s''', (type, ))
        results = self.cursor.fetchall()
        if results is None:
            return None
        resources = []
        for result in results:
            resource = {
                "id": result[0],
                "name": result[1],
                "current_speed": result[2],
                "type": result[3],
                "over_speed": result[6]
            }
            resources.append(resource)
        self.close()
        return resources

    def close(self):
        self.conn.close()
