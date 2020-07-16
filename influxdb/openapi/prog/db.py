from influxdb import InfluxDBClient


class Database:
    db: InfluxDBClient = None

    @classmethod
    def set_db(cls, db_a, db_n):
        if cls.db is not None:
            return
        cls.db = InfluxDBClient(host=db_a, database=db_n)


class DBRequest:
    _mes = None

    @classmethod
    def set_mes(cls, mes):
        cls._mes = mes

    @classmethod
    def _check_set(cls):
        if Database.db is None:
            raise Exception("Database not setted")
        if DBRequest._mes is None:
            raise Exception("Measure not setted")

    @classmethod
    def get_params(cls):
        cls._check_set()
        request_string = "SELECT * FROM " + cls._mes
        response = Database.db.query(request_string, epoch="ms")
        rs = []
        for a in response.get_points():
            rs.append(a)
        return rs

    @classmethod
    def set_fields(cls, fields):
        cls._check_set()
        ms = {
                "measurement": cls._mes,
                "fields": fields
        }
        Database.db.write_points([ms])
