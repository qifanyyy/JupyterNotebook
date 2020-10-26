import tornado
from tornado.escape import json_encode
from tornado.options import define, options
import tornado.web
import tornado.httpserver
import tornado.ioloop
import os.path
from models import User, Ratings
from recommender import Recommender

__author__ = 'dolel'

define("port", default=8500, help="Run the App on the Given Port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('index.html', title="GeekNight Recommendation Engine", users=User().retrieve_users())


class AddUserHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        if User(user_name=self.get_argument('user_name')).save_user():
            self.write(json_encode(self.get_argument('user_name')))


class ViewUsersHandler(tornado.web.RequestHandler):
    def get(self, user_id):
        user_information = User(user_id=user_id).retrieve_user_information()
        if user_information.__len__() < 1:
            self.write(json_encode("No Users Exist"))
        else:
            users = {}
            for user in user_information:
                users = {'user_id': user.user_id, 'user_name': user.user_name}
            self.write(json_encode(users.values()))
            self.render("user_details.html", title="View User", user_id=users['user_id'])


class DeleteUserHandler(tornado.web.RequestHandler):
    def get(self, user_id):
        if User(user_id=user_id).delete_user():
            self.write(json_encode("User successfully deleted from Database"))
            self.redirect('/')


class RateMoviesHandler(tornado.web.RequestHandler):
    def get(self, user_id):
        self.render('rate_movies.html', title="Rate Movies", user_id=user_id)


class RateMovieByUserHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        movie_ratings = Ratings(user_id=self.get_argument('user_id'),
                                olympus_has_fallen=self.get_argument('olympus_has_fallen'),
                                m300=self.get_argument('m300'),
                                expendables=self.get_argument('expendables'),
                                lord_of_the_rings=self.get_argument('lord_of_the_rings'),
                                pirates_of_the_carribbean=self.get_argument('pirates_of_the_caribbean'),
                                harry_potter=self.get_argument('harry_potter'),
                                grown_ups=self.get_argument('grown_ups'),
                                hangover=self.get_argument('hangover'),
                                pacific_rim=self.get_argument('pacific_rim'),
                                transformers=self.get_argument('transformers'),
                                man_of_steel=self.get_argument('man_of_steel'),
                                now_you_see_me=self.get_argument('now_you_see_me'),
                                django_unchained=self.get_argument('django_unchained'),
                                pain_and_gain=self.get_argument('pain_and_gain'),
                                madagascar=self.get_argument('madagascar'),
                                despicable_me=self.get_argument('despicable_me'),
                                smurfs=self.get_argument('smurfs'))
        if movie_ratings.save_ratings():
            self.write(json_encode("User's Movie Ratings successfully saved"))
        else:
            self.write(json_encode("User already rated movies"))


class GetUserRatingsHandler(tornado.web.RequestHandler):
    def get(self, user_id):
        user_data = {}
        for user_rating in Ratings(user_id=user_id).retrieve_user_ratings():
            user_data = {
                'olympus_has_fallen': user_rating.olympus_has_fallen,
                'm300': user_rating.m300,
                'expendables': user_rating.expendables,
                'lord_of_the_rings': user_rating.lord_of_the_rings,
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
        self.write(json_encode(user_data))
        self.render("user_ratings.html", title="User Ratings", user_id=user_id, user_ratings=user_data)


class GetNearestNeighborsHandler(tornado.web.RequestHandler):
    def get(self, user_id):
        user_ratings = Ratings().retrieve_all_user_ratings()
        neighbors = Recommender(user_ratings).compute_nearest_neighbor(int(user_id))
        neighbors_list = []

        for nearest_neighbor in neighbors:
            for user in User(user_id=nearest_neighbor[0]).retrieve_user_information():
                neighbors_list.append((str(user.user_name).capitalize(), (nearest_neighbor[1] * 100)))

        self.render('view_neighbors.html',
                    user_id=user_id,
                    title="View User Neighbors",
                    neighbors=neighbors_list,
                    user_name=User(user_id=user_id).retrieve_user_name())


class GetRecommendationsHandler(tornado.web.RequestHandler):
    def get(self, user_id):
        self.render('view_recommendations.html',
                    title="View Recommendations",
                    user_id=user_id,
                    user_name=User(user_id=user_id).retrieve_user_name(),
                    recommendations=Recommender(Ratings().retrieve_all_user_ratings()).recommend(int(user_id)))


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/users/add", AddUserHandler),
            (r"/users/([0-9]+)", ViewUsersHandler),
            (r"/movies/rate/([0-9]+)", RateMoviesHandler),
            (r"/movies/rate/", RateMovieByUserHandler),
            (r"/users/ratings/([0-9)]+)", GetUserRatingsHandler),
            (r"/users/delete/([0-9)]+)", DeleteUserHandler),
            (r"/users/neighbors/([0-9)]+)", GetNearestNeighborsHandler),
            (r"/users/recommendations/show/([0-9]+)", GetRecommendationsHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    tornado.httpserver.HTTPServer(app).listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
