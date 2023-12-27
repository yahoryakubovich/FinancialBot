from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    balance = Column(Float, default=0.0)

class Database:
    def __init__(self, db_file):
        self.engine = create_engine(f'sqlite:///{db_file}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def user_exists(self, user_id):
        session = self.Session()
        user = session.query(User).filter_by(user_id=user_id).first()
        session.close()
        return user is not None

    def create_user(self, user_id):
        session = self.Session()
        new_user = User(user_id=user_id)
        session.add(new_user)
        session.commit()
        session.close()

    def update_balance(self, user_id, amount):
        session = self.Session()
        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            user.balance += amount
            session.commit()
        session.close()

    def get_balance(self, user_id):
        session = self.Session()
        user = session.query(User).filter_by(user_id=user_id).first()
        balance = user.balance if user else 0.0
        session.close()
        return balance
