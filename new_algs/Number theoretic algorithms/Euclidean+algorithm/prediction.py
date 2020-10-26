from src.mymathhelper import *
import pprint

class Prediction:
    def __init__(self, training_set):
        self.training_set = training_set.training_set
        self.training_set_iuf = training_set.training_set_iuf
        self.movie_variance = training_set.movie_variance
        self.movie_popularity = training_set.movie_popularity
        self.movie_ratings_count = training_set.movie_ratings_count  # todo why is this a tuple?
        self.movie_movie_similarity_matrix = training_set.movie_movie_similarity_matrix
        self.user_average_rating = training_set.user_average_rating

    def custom_all_static_weighted_average(self, user_cf_weight, movie_cf_weight, movie_popularity_weight,
                                           user_cf_value, movie_cf_value, movie_popularity):
        value = user_cf_weight * user_cf_value + movie_cf_value * movie_cf_weight + movie_popularity * movie_popularity_weight
        value /= (user_cf_weight + movie_cf_weight + movie_popularity_weight)
        return value

    ###############################################################################################################
    #                                               Movie Avg                                                     #
    ###############################################################################################################
    def movie_average(self, movie_index):
        """Assumptions:
            - If there is a lot of user ratings, the average movie rating is more reliable
            - If there is a low variance, the average movie rating is more reliable
            - If there is lot of user rating and low rating, the movie rating is very reliable
        This is a rating Independent of what the user history and preferences - more on Trust Computing"""
        percent_users_watched = self.movie_ratings_count[movie_index] / len(self.training_set)
        movie_variance = self.movie_variance[movie_index]
        # Idea - Dynamically adjust weight based on variance? If variance is low
        return percent_users_watched * movie_variance

    ###############################################################################################################
    #                                                 Cosine                                                      #
    ###############################################################################################################

    def find_closest_users_cosine(self, user_vector, movie_index, k):
        """
        This is the Kth- nearest neighbor algorithm
        """
        closest_users = [(0, 0, 0, 0, 0)] * k
        for i in range(0, len(self.training_set)):
            # print 'i:',i
            # print movie
            if self.training_set[i][movie_index] != 0:  # Makes sure the user has that movie rating
                v1 = self.training_set[i]
                v2 = user_vector

                v1 = self.training_set_iuf[i]
                v2 = MyMathHelper.scale_list_by_iuf(v2, len(self.training_set), self.movie_ratings_count)

                # Reduces to common dimensions
                temp = MyMathHelper.common_dimensions(v1, v2)
                v1 = temp[0]
                v2 = temp[1]
                print 'v1:', v1
                print 'v2:', v2
                # Scales by IUF
                # v1 = MyMathHelper.iuf(len(self.training_set), self.movie_ratings_count)
                value = MyMathHelper.custom_cosine_similarity(v1, v2)
                # print value
                # print closest_users
                if abs(value) > closest_users[0][1]:  # Absolute Value
                    del closest_users[0]  # Delete smallest value
                    closest_users.append((i, value, self.training_set[i][movie_index], v1, v2))  # Add new value to end
                    # print closest_users
                    closest_users = sorted(closest_users, key=lambda tup: tup[1])  # sort in increasing order
        return closest_users

    def user_user_cosine_similarity(self, user_vector, movie_index, k):
        """
        Calculates the Weighted Average
        k = top k for nearest neighbor algorithm
        movie - movie index to only include close users that rated that specific movie
        """
        closest_users = self.find_closest_users_cosine(user_vector, movie_index, k)
        print 'Closest users:', closest_users
        prediction = 0
        denominator = 0
        for u in closest_users:
            if u == (0, 0, 0, 0, 0):
                continue
            weight = MyMathHelper.custom_case_amplification(u[1])
            movie_rating = u[2]
            prediction += (weight * movie_rating)
            denominator += weight
        try:
            prediction /= denominator
        except Exception, e:
            print 'Error in user_user_cosine_similarity:', e
            return 3
        print prediction
        return prediction

    ###############################################################################################################
    #                                                 PEARSON                                                     #
    ###############################################################################################################

    def find_closest_users_pearson(self, user_vector, movie_index, k):
        """
        This is the Kth- nearest neighbor algorithm
        """
        closest_users = [(0, 0, 0, 0, 0, 0, 0,0,0,0)] * k  # top K user
        avg_test_user_common_dimension = None
        for i in range(0, len(self.training_set)):
            if self.training_set[i][movie_index] != 0:  # Makes sure the user has that movie rating
                # Scales by IUF
                v1 = self.training_set[i]
                v2 = user_vector
                # v1 = MyMathHelper.scale_list_by_iuf(v1, len(self.training_set), self.movie_ratings_count)
                # v2 = MyMathHelper.scale_list_by_iuf(v2, len(self.training_set), self.movie_ratings_count)

                # Reduces to common dimensions
                temp = MyMathHelper.common_dimensions(v1, v2)
                v1 = temp[0]
                v2 = temp[1]

                if(len(v1)) == 0 or len(v1)==1:
                    continue
                avg_train_user_common_dimension = MyMathHelper.average(v1)
                avg_test_user_common_dimension = MyMathHelper.average(v2)
                print '--------------------------------------------------'
                print 'v1:', v1, '\nv2:', v2

                # Finds Net List
                v1 = MyMathHelper.net_list(v1,self.user_average_rating[i])
                user_vector_avg = sum(user_vector) / MyMathHelper.nonzero_count(user_vector)
                v2 = MyMathHelper.net_list(v2, user_vector_avg)
                print 'AFTER\nv1:', v1, '\nv2:', v2

                value = MyMathHelper.custom_cosine_similarity(v1, v2)

                if abs(value) > abs(closest_users[0][1]):  # Absolute Value
                    del closest_users[0]  # Delete smallest value
                    training_set_user_avg = self.user_average_rating[i]
                    testing_user_avg = float(sum(user_vector))/float(MyMathHelper.nonzero_count(user_vector))
                    training_set_user_movie_score = self.training_set[i][movie_index]
                    compare_value = abs(value)
                    closest_users.append((i, value, training_set_user_movie_score,
                                                   training_set_user_avg,
                                                   testing_user_avg,
                                                   v1, v2, compare_value,
                                                    avg_train_user_common_dimension,
                                                    avg_test_user_common_dimension))  # Add new value to end
                    # print closest_users
                    closest_users = sorted(closest_users, key=lambda tup: tup[7])  # sort in increasing order

                    print ' value:',value
                    print ' training_set_user_movie_score:',training_set_user_movie_score
                    print ' avg_train_user_common_dimension:',avg_train_user_common_dimension
                    print ' avg_test_user_common_dimension:',avg_test_user_common_dimension
        return closest_users, avg_test_user_common_dimension

    def user_user_pearson(self, user_vector, movie, k):
        """
        Calculates the Weighted Average
        k = top k for nearest neighbor algorithm
        movie - movie index to only include close users that rated that specific movie
        """
        temp= self.find_closest_users_pearson(user_vector, movie, k)
        closest_users = temp[0]
        testing_user_avg = None
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(closest_users)
        # print closest_users
        prediction = 0
        denominator = 0
        for u in closest_users:
            weight = u[1]
            # weight = MyMathHelper.custom_case_amplification(weight)
            training_set_user_movie_score = u[2]
            # training_set_user_avg = u[8]
            # testing_user_avg = u[9]
            training_set_user_avg = u[3]
            testing_user_avg = u[4]
            if weight != 0:
                denominator += abs(weight)
                prediction += ((weight * (training_set_user_movie_score - training_set_user_avg)))
        if denominator == 0:
            p = float(sum(user_vector)) / float(MyMathHelper.nonzero_count(user_vector))
            return p
        prediction /= denominator
        prediction += testing_user_avg
        return prediction


    ###############################################################################################################
    #                                  TOP K PER DIMENSION (Custom Algorithm) w/ Cosine                           #
    ###############################################################################################################
    def find_closest_users_top_k_per_dimension(self, user_vector, movie_index, k):
        """
        This is the Kth- nearest neighbor algorithm
        """
        closest_users = {}
        for i in range(0, len(self.training_set)):
            # print 'i:',i
            # print movie
            if self.training_set[i][movie_index] != 0:  # Makes sure the user has that movie rating
                # Scales by IUF
                v1 = self.training_set[i]
                v2 = user_vector

                # v1 = self.training_set_iuf[i]
                # v2 = MyMathHelper.scale_list_by_iuf(v2, len(self.training_set), self.movie_ratings_count)

                # Reduces to common dimensions
                temp = MyMathHelper.common_dimensions(v1, v2)
                v1 = temp[0]
                v2 = temp[1]
                print 'v1:', v1, '\nv2:', v2

                # Finds Net List

                value = MyMathHelper.custom_cosine_similarity(v1, v2)
                if len(v1) == 0:
                    continue
                if len(v1) not in closest_users:
                    closest_users[len(v1)] = [(0, 0, 0, 0, 0)] * k
                print closest_users
                if abs(value) > closest_users[len(v1)][0][1]:  # Absolute Value
                    del closest_users[len(v1)][0]  # Delete smallest value
                    closest_users[len(v1)].append(
                        (i, value, self.training_set[i][movie_index], v1, v2))  # Add new value to end
                    # print closest_users
                    closest_users[len(v1)] = sorted(closest_users[len(v1)],
                                                    key=lambda tup: tup[1])  # sort in increasing order
        return closest_users

    def top_k_per_dimension_similarity(self, user_vector, movie_index, k):
        """
        Calculates the Weighted Average
        k = top k for nearest neighbor algorithm
        movie - movie index to only include close users that rated that specific movie
        """
        closest_users = self.find_closest_users_top_k_per_dimension(user_vector, movie_index, k)
        print 'Closest users:', closest_users
        prediction = {}
        denominator = {}
        for dimension in closest_users:
            prediction[dimension] = 0
            denominator[dimension] = 0
            for u in closest_users[dimension]:
                if u == (0, 0, 0, 0, 0):
                    continue
                # weight = MyMathHelper.custom_case_deamplification(u[1])
                weight =u[1]
                # weight = MyMathHelper.custom_case_amplification(u[1])
                movie_rating = u[2]
                prediction[dimension] = prediction[dimension] + (weight * movie_rating)
                denominator[dimension] = denominator[dimension] + weight
            try:
                prediction[dimension] = prediction[dimension] / denominator[dimension]
            except Exception, e:
                print 'Error in user_user_cosine_similarity:', e
                prediction[dimension] = 3
        print 'Prediction Per Dimension:', prediction
        print 'Total Weight Per Dimension:', denominator

        total_weight = 0
        final_prediction = 0
        for dimension in prediction:
            final_prediction += prediction[dimension] * denominator[dimension]
            total_weight += denominator[dimension]
        try:
            final_prediction /= total_weight
        except Exception, e:
            return 3  # todo cold start problem! Movie never been rated
        return final_prediction

    ###############################################################################################################
    #                                  TOP K PER DIMENSION (Custom Algorithm) w/ Pearson                          #
    ###############################################################################################################
    def pearson_find_closest_users_top_k_per_dimension(self, user_vector, movie_index, k):
        """
        This is the Kth- nearest neighbor algorithm
        """
        closest_users = {}
        for i in range(0, len(self.training_set)):
            # print 'i:',i
            # print movie
            if self.training_set[i][movie_index] != 0:  # Makes sure the user has that movie rating
                # Scales by IUF
                v1 = self.training_set[i]
                v2 = user_vector
                # v1 = MyMathHelper.scale_list_by_iuf(v1, len(self.training_set), self.movie_ratings_count)
                # v2 = MyMathHelper.scale_list_by_iuf(v2, len(self.training_set), self.movie_ratings_count)

                # Reduces to common dimensions
                temp = MyMathHelper.common_dimensions(v1, v2)
                v1 = temp[0]
                v2 = temp[1]

                if(len(v1)) == 0 or len(v1)==1:
                    continue
                avg_train_user_common_dimension = MyMathHelper.average(v1)
                avg_test_user_common_dimension = MyMathHelper.average(v2)
                print '--------------------------------------------------'
                print 'v1:', v1, '\nv2:', v2

                # Finds Net List
                v1 = MyMathHelper.net_list(v1,self.user_average_rating[i])
                user_vector_avg = sum(user_vector) / MyMathHelper.nonzero_count(user_vector)
                v2 = MyMathHelper.net_list(v2, user_vector_avg)
                print 'AFTER\nv1:', v1, '\nv2:', v2

                value = MyMathHelper.custom_cosine_similarity(v1, v2)

                if len(v1) == 0:  # todo Skipping vector length 1 cases
                    continue
                if len(v1) not in closest_users:
                    closest_users[len(v1)] = [(0, 0, 0, 0, 0, 0, 0,0,0,0)] * k
                print closest_users
                if abs(value) > abs(closest_users[len(v1)][0][1]):  # Absolute Value
                    del closest_users[len(v1)][0]  # Delete smallest value
                    training_set_user_avg = self.user_average_rating[i]
                    testing_user_avg = float(sum(user_vector))/float(MyMathHelper.nonzero_count(user_vector))
                    training_set_user_movie_score = self.training_set[i][movie_index]
                    compare_value = abs(value)
                    closest_users[len(v1)].append((i, value, training_set_user_movie_score,
                                                   training_set_user_avg,
                                                   testing_user_avg,
                                                   v1, v2, compare_value,
                                                    avg_train_user_common_dimension,
                                                    avg_test_user_common_dimension))  # Add new value to end
                    # print closest_users
                    closest_users[len(v1)] = sorted(closest_users[len(v1)],
                                                    key=lambda tup: tup[7])  # sort in increasing order
                    print ' value:',value
                    print ' training_set_user_movie_score:',training_set_user_movie_score
                    print ' avg_train_user_common_dimension:',avg_train_user_common_dimension
                    print ' avg_test_user_common_dimension:',avg_test_user_common_dimension
        return closest_users

    def pearson_top_k_per_dimension_similarity(self, user_vector, movie_index, k):
        """
        Calculates the Weighted Average
        k = top k for nearest neighbor algorithm
        movie - movie index to only include close users that rated that specific movie
        """
        closest_users = self.pearson_find_closest_users_top_k_per_dimension(user_vector, movie_index, k)
        print 'Closest users:', closest_users
        prediction = {}
        denominator = {}
        testing_user_avg = None
        for dimension in closest_users:
            prediction[dimension] = 0
            denominator[dimension] = 0
            for u in closest_users[dimension]:
                if u == (0, 0, 0, 0, 0, 0, 0,0,0,0):
                    continue
                weight = u[1]
                weight = MyMathHelper.custom_case_amplification(weight)
                training_set_user_movie_score = u[2]
                # training_set_user_avg = u[8]
                # testing_user_avg = u[9]
                training_set_user_avg = u[3]
                testing_user_avg = u[4]

                if weight != 0:
                    denominator[dimension] += abs(weight)
                    prediction[dimension] += ((weight * (training_set_user_movie_score - training_set_user_avg)))

            try:
                prediction[dimension] /= denominator[dimension]
                prediction[dimension] += testing_user_avg
            except Exception, e:
                print 'Error in user_user_cosine_similarity:', e
                prediction[dimension] = 3
        print 'Prediction Per Dimension:', prediction
        print 'Total Weight Per Dimension:', denominator

        total_weight = 0
        final_prediction = 0
        for dimension in prediction:
            final_prediction += prediction[dimension] * denominator[dimension]
            total_weight += denominator[dimension]
        try:
            final_prediction /= total_weight
        except Exception, e:
            value = float(sum(user_vector)) / float(MyMathHelper.nonzero_count(user_vector))
            print 'Prediction (from user avg):',value
            return value
        return final_prediction

    ###############################################################################################################
    #                                  Item Based Collaborative Filtering - Cosine Similarity                     #
    ###############################################################################################################

    def item_based_cosine_similarity(self,user_vector, movie_index):
        user_rated_movie_index = []
        for i in range(0, len(user_vector)):
            if user_vector[i] != 0:
                user_rated_movie_index.append(i)

        # do adjusted cosine
        similarities = []
        for known_movie in user_rated_movie_index:
            similarities.append(abs(self.movie_movie_similarity_matrix[known_movie][movie_index]))

        total_value = 0
        denominator = 0
        for i in range(0,len(similarities)):
            total_value += similarities[i] * self.movie_popularity[user_rated_movie_index[i]]
            denominator += similarities[i]

        prediction = total_value/denominator
        return prediction


    ###############################################################################################################
    #                                                 Manhattan Distance Similarity                               #
    ###############################################################################################################

    def user_user_manhattan(self, user_vector, movie, k):
        """
        Calculates the Weighted Average
        k = top k for nearest neighbor algorithm
        movie - movie index to only include close users that rated that specific movie
        """
        closest_users = self.find_closest_users_manhattan(user_vector, movie, k)
        print closest_users
        prediction = 0
        denominator = 0
        for u in closest_users:
            weight = u[1]
            movie_rating = u[2]
            # weight = MyMathHelper.custom_case_amplification(weight)
            if weight != 0:
                prediction += (weight * movie_rating)
                denominator += weight
        if denominator == 0:
            value = float(sum(user_vector)) / float(MyMathHelper.nonzero_count(user_vector))
            print 'Prediction (from user avg):',value
            return value
        prediction /= denominator
        return prediction

    def find_closest_users_manhattan(self, user_vector, movie_index, k):
        """
        This is the Kth- nearest neighbor algorithm
        """
        closest_users = []
        for i in range(0, len(self.training_set)):
            if self.training_set[i][movie_index] != 0:  # Makes sure the user has that movie rating
                # Scales by IUF
                v1 = self.training_set[i]
                v2 = user_vector

                # Reduces to common dimensions
                temp = MyMathHelper.common_dimensions(v1, v2)
                v1 = temp[0]
                v2 = temp[1]
                print 'v1:', v1, '\nv2:', v2

                # # Finds Net List
                # v1 = MyMathHelper.net_list(v1,self.user_average_rating[i])
                # user_vector_avg = sum(user_vector) / MyMathHelper.nonzero_count(user_vector)
                # v2 = MyMathHelper.net_list(v2, user_vector_avg)

                if(len(v1)) == 0:
                    continue
                value = MyMathHelper.manhattan_distance(v1, v2) / len(v1)
                value = 1/ (value + 1)
                training_set_user_movie_score = self.training_set[i][movie_index]

                if len(closest_users) < k:
                    closest_users.append((i, value, training_set_user_movie_score,v1, v2))  # Add new value to end

                if value < closest_users[0][1] or (value == closest_users[0][1] and len(v1) > len(closest_users[0][3])):  # Absolute Value
                    del closest_users[0]  # Delete smallest value
                    closest_users.append((i, value, training_set_user_movie_score,v1, v2))  # Add new value to end
                    # print closest_users
                closest_users = sorted(closest_users, key=lambda tup: tup[1])  # sort in increasing order
        return closest_users

