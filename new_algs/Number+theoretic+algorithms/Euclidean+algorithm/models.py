from sqlalchemy import create_engine, MetaData, Column, Table, Integer, String, Float
from sqlalchemy.orm import sessionmaker, mapper

__author__ = 'dolel'

SQLALCHEMY_DATABASE_URI = 'mysql://root:FdtWeb2013@localhost/geeknight_recommender'
#Engine, which the Session will use for connection resources
database_engine = create_engine(SQLALCHEMY_DATABASE_URI)
#Creating the Configured Session Class
Session = sessionmaker(bind=database_engine)
session = Session()


class User(object):
    def __init__(self, user_name=None, user_id=None):
        self.user_name = user_name
        self.user_id = user_id

    def save_user(self):
        session.add(self)
        session.commit()
        return True

    def retrieve_users(self):
        return session.query(User).all()

    def retrieve_user_information(self):
        return session.query(User).filter(User.user_id == self.user_id).all()

    def delete_user(self):
        session.query(User).filter(User.user_id == self.user_id).delete()
        session.commit()
        return True

    def retrieve_user_name(self):
        user_name = None
        for user in session.query(User).filter(User.user_id == self.user_id):
            user_name = user.user_name
        return user_name


metadata = MetaData()
user_table = Table('users', metadata,
                   Column('user_id', Integer, primary_key=True, autoincrement=True),
                   Column('user_name', String(20), nullable=False))
mapper(User, user_table)


class Ratings(object):
    def __init__(self, user_id=None, olympus_has_fallen=None, m300=None, expendables=None, lord_of_the_rings=None,
                 pirates_of_the_carribbean=None, harry_potter=None, grown_ups=None, hangover=None, pacific_rim=None,
                 transformers=None, man_of_steel=None, now_you_see_me=None,
                 django_unchained=None, pain_and_gain=None, madagascar=None, despicable_me=None, smurfs=None):
        self.user_id = user_id
        self.olympus_has_fallen = olympus_has_fallen
        self.m300 = m300
        self.expendables = expendables
        self.lord_of_the_rings = lord_of_the_rings
        self.pirates_of_the_carribbean = pirates_of_the_carribbean
        self.harry_potter = harry_potter
        self.grown_ups = grown_ups
        self.hangover = hangover
        self.pacific_rim = pacific_rim
        self.transformers = transformers
        self.man_of_steel = man_of_steel
        self.now_you_see_me = now_you_see_me
        self.django_unchained = django_unchained
        self.pain_and_gain = pain_and_gain
        self.madagascar = madagascar
        self.despicable_me = despicable_me
        self.smurfs = smurfs

    def save_ratings(self):
        if session.query(Ratings).filter(Ratings.user_id == self.user_id).all().__len__() == 0:
            session.add(self)
            session.commit()
            return True
        else:
            return False

    def retrieve_user_ratings(self):
        return session.query(Ratings).filter(Ratings.user_id == self.user_id).all()

    def retrieve_all_user_ratings(self):
        user_ratings = {}
        new_user_ratings = {}
        movies_to_remove = []
        for user_rating in session.query(Ratings).all():
            user_ratings[user_rating.user_id] = {'olympus_has_fallen': user_rating.olympus_has_fallen,
                                                 'm300': user_rating.m300,
                                                 'lord_of_the_rings': user_rating.lord_of_the_rings,
                                                 'expendables': user_rating.expendables,
                                                 'pirates_of_the_carribbean': user_rating.pirates_of_the_carribbean,
                                                 'harry_potter': user_rating.harry_potter,
                                                 'grown_ups': user_rating.grown_ups,
                                                 'hangover': user_rating.hangover,
                                                 'pacific_rim': user_rating.pacific_rim,
                                                 'transformers': user_rating.transformers,
                                                 'man_of_steel': user_rating.man_of_steel,
                                                 'now_you_see_me': user_rating.now_you_see_me,
                                                 'django_unchained': user_rating.django_unchained,
                                                 'pain_and_gain': user_rating.pain_and_gain,
                                                 'madagascar': user_rating.madagascar,
                                                 'despicable_me': user_rating.despicable_me,
                                                 'smurfs': user_rating.smurfs}

        for user_id in user_ratings:
            for movie_name, movie_rating in user_ratings[user_id].items():
                if movie_rating < 1.0:
                    del user_ratings[user_id][movie_name]
        return user_ratings


metadata = MetaData()
ratings_table = Table('ratings', metadata,
                      Column('user_id', Integer, primary_key=True, autoincrement=True),
                      Column('olympus_has_fallen', Float, nullable=True),
                      Column('m300', Float, nullable=True),
                      Column('expendables', Float, nullable=True),
                      Column('lord_of_the_rings', Float, nullable=True),
                      Column('pirates_of_the_carribbean', Float, nullable=True),
                      Column('harry_potter', Float, nullable=True),
                      Column('grown_ups', Float, nullable=True),
                      Column('hangover', Float, nullable=True),
                      Column('pacific_rim', Float, nullable=True),
                      Column('transformers', Float, nullable=True),
                      Column('man_of_steel', Float, nullable=True),
                      Column('now_you_see_me', Float, nullable=True),
                      Column('django_unchained', Float, nullable=True),
                      Column('pain_and_gain', Float, nullable=True),
                      Column('madagascar', Float, nullable=True),
                      Column('despicable_me', Float, nullable=True),
                      Column('smurfs', Float, nullable=True))
mapper(Ratings, ratings_table)
