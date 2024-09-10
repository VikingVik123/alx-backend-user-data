#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import Session

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session
    
    def add_user(self, email: str, hashed_password: str) -> User:
        """
        method to add user from User class
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        
        return user
    
    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user by arbitrary keyword arguments
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound
        except InvalidRequestError:
            raise InvalidRequestError
        
    def update_user(self, user_id: int, **kwargs) -> None:
        """
        update the user info
        """
        user = self.find_user_by(user_id)
        for key, value in kwargs.items:
            if not hasattr(user, key):
                raise ValueError(f"{key} is not an attribute of the User class.")
            setattr(user, key, value)
        self._session.commit()
