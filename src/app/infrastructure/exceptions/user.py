from sqlalchemy.exc import NoResultFound


class UserNotFound(NoResultFound):
    pass