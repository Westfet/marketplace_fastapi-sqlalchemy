from queries.database import engine, Base


class SyncORM:
    @staticmethod
    def create_tables():
        Base.metadata.drop_all(engine)
        print("таблицы дропнуты")
        Base.metadata.create_all(engine)
        print("таблицы созданы")


