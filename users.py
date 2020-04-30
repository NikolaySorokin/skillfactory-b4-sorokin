import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///sochi_athletes.sqlite3"
MALE = ("Male", "M", "m", "М", "м")
FEMALE = ("Female", "F", "f", "Ж", "ж")

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

def connect_db():
    """
    Подключаемся к базе данных,создаем и возвращаем сессию
    """
    engine = sa.create_engine(DB_PATH)
    Sessions = sessionmaker(engine)
    session = Sessions()
    return session

def request_data():
    print("Введите свои данные")
    first_name = input("Ваше имя: ")
    last_name = input("Ваша фамилия: ")
    gender = input("Ваш пол (M/F): ")
    if gender in MALE:
        gender = "Male"
    elif gender in FEMALE:
        gender = "Female"
    email = input("Ваша электронная почта: ")
    birthdate = input("Ваша дата рождения: ")
    height = input("Ваш рост (в метрах): ")

    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    return user

def main():
    session = connect_db()

    user = request_data()
    session.add(user)
    session.commit()
    print("Пользователь сохранен!")


if __name__ == "__main__":
    main()