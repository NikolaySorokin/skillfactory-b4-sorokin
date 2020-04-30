import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///sochi_athletes.sqlite3"

Base = declarative_base()

class User(Base):
    """
    Определяем класс для отображения в таблицу user
    """
    __tablename__ = 'user'
    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)

class Athelete(Base):
    """
        Определяем класс для отображения в таблицу athelete
    """
    __tablename__ = "athelete"
    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    age = sa.Column(sa.INTEGER)
    birthdate = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.TEXT)
    weight = sa.Column(sa.INTEGER)
    gold_medals = sa.Column(sa.INTEGER)
    silver_medals = sa.Column(sa.INTEGER)
    bronze_medals = sa.Column(sa.INTEGER)
    total_medals = sa.Column(sa.INTEGER)
    sport = sa.Column(sa.TEXT)
    country = sa.Column(sa.TEXT)

def connect_db():
    """
    Подключаемся к базе данных,создаем и возвращаем сессию
    """
    engine = sa.create_engine(DB_PATH)
    Sessions = sessionmaker(engine)
    session = Sessions()
    return session

def find_user(user_id, session):
    """
    Поиск пользователя в базе по его id.
    """
    user_query = session.query(User).filter(User.id == user_id).first()
    return (user_query)

def bd_to_datetime(bd_str):
    """
    Функция преобразования строки с датой рождения в datetime
    """
    # Используемый в таблице формат
    bd_format = "%Y-%m-%d"
    bd_datetime = datetime.datetime.strptime(bd_str, bd_format)
    return bd_datetime


def nearest_height(user_height, session):
    """
    Поиск ближайшего по росту атлета (или атлетов, если рост одинаковый).
    Возвращает список атлетов
    """
    athelete_query = session.query(Athelete).filter(Athelete.height > 0).all()
    athelete_heights = [athelete.height for athelete in athelete_query]
    near_h = min(athelete_heights, key=lambda x: abs(x - user_height))
    nearest_height_atheletes = session.query(Athelete).filter(Athelete.height == near_h).all()
    return nearest_height_atheletes

def nearest_birthdate(user_birthdate, session):
    """
    Поиск ближайшего по дате рождения атлета (или нескольких с одной датой).
    Возвращает список атлетов
    """
    athelete_query = session.query(Athelete).filter(Athelete.birthdate).all()
    athelete_birthdates = [athelete.birthdate for athelete in athelete_query]
    near_bd = min(athelete_birthdates,
                  key=lambda x: abs(bd_to_datetime(x) - bd_to_datetime(user_birthdate)))
    nearest_birthdate_atheletes = session.query(Athelete).filter(Athelete.birthdate == near_bd).all()
    return nearest_birthdate_atheletes


def main():
    session = connect_db()
    mode = input("Введите id пользователя: ")
    user = find_user(mode, session)
    if user:
        print("Пользователь с введенным id:\n"
              "{} {} - {} - {} метров".format(user.first_name, user.last_name, user.birthdate, user.height))
        nearest_birthdate_atheletes = nearest_birthdate(user.birthdate, session)
        print("Ближайший атлет по дате рождения (или несколько атлетов): ")
        for athelete in nearest_birthdate_atheletes:
            print("{} - {}".format(athelete.name, athelete.birthdate))
        nearest_height_atheletes = nearest_height(user.height, session)
        print("Ближайший атлет по росу (или несколько атлетов): ")
        for athelete in nearest_height_atheletes:
            print("{} - {} метров".format(athelete.name, athelete.height))
    else:
        print("Пользователя с данным id не найдено!")


if __name__ == "__main__":
    main()