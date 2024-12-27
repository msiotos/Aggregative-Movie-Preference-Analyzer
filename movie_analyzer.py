import sys
import random

"""
Functions that execute the commands requested
"""
def get_avg_ratings(trimmed_ratings_data):
    movie_ratings = {}
    for _, movie_id, rating, _ in trimmed_ratings_data:
        movie_ratings.setdefault(movie_id, []).append(rating)
    return {movie_id: sum(ratings) / len(ratings) for movie_id, ratings in movie_ratings.items()}


def link_movieID_to_title(movies_data):
    return {movie_id: title for movie_id, title, _ in movies_data}

def rating(trimmed_ratings_data, movies_data, t1, t2):

    avg_ratings = get_avg_ratings(trimmed_ratings_data)
    movies_names = link_movieID_to_title(movies_data)


    result = {}
    for movie_id, avg_rating in avg_ratings.items():
        if t1 < avg_rating <= t2:
            result[movies_names[movie_id]] = avg_rating
    return result



"""
Printing of the results is done in a seperate function (as adviced)
"""

def print_rating(results):
    if not results:
        print("No movies found with average rating between the given values.")
    else:
        print(f"\n{'Τίτλος Ταινίας':<80} {'Μέσο Rating':<15}")
        print("_" * 95)
        print("\n")
        for movie_name, avg_rating in results.items():
            print(f"{movie_name:<80} {avg_rating:<.2f}")


def top_movies(trimmed_ratings_data, movies_data, k):


    avg_ratings = get_avg_ratings(trimmed_ratings_data)
    movies_names = link_movieID_to_title(movies_data)


    """
    Creating a dictionary to sort the movies in descending order and picking the K number of them
    """

    sorted_movies = {}
    for movieID, avg_rating in sorted(avg_ratings.items(), key=lambda item: item[1], reverse=True)[:k]:
            sorted_movies[movieID] = avg_rating


    """
    Creating the final dictionary to return the top movies with their avg ratings
    """

    result = {}
    for movieID, avg_rating in sorted_movies.items():
        if movieID in movies_names:
            result[movies_names[movieID]] = avg_rating
    return result

"""
Printing of the results is done in a seperate function (as adviced)
"""

def print_top_movies(results):
    if not results:
        print("You asked for 0 movies...")
    else:
        print(f"\n{'Τίτλος Ταινίας':<80} {'Μέσο Rating':<15}")
        print("_" * 95)
        print("\n")
        for movie_name, avg_rating in results.items():
            print(f"{movie_name:<80} {avg_rating:<.2f}")

def user_pairs(trimmed_ratings_data, movies_data, k):
    """
    Creating an empty dictionary to store all users that have rated movies.(Grouped by moviesID)
    If there is no entry for a movieID inside the dictionary (first time reading it),
    we use the .setdefault and add an empty list as the default value
    """

    movies_with_users = {}
    for userID, movieID, _, _ in trimmed_ratings_data:
        movies_with_users.setdefault(movieID, []).append(userID)

    """
    Initializing an empty list that will store the tuples we want
    Using a for loop to parse all movies
    Using an if statement to check the movies that have more than 1 rating since we want pairs
    We then use two loops to parse the user list for each movie (j starts at i+1 in order to have unique pairs)
    We check twice if we have reached the k number of pairs asked, the first check is to stop processing
    more users for a movie and the second check to stop processing more movies
    """
    user_pairs_list = []
    for movieID, users in movies_with_users.items():
        if len(users) > 1:
            for i in range(len(users)):
                for j in range(i + 1, len(users)):
                    user_pairs_list.append((users[i], users[j], movieID))
                    if len(user_pairs_list) >= k:
                        break
        if len(user_pairs_list) >= k:
            break


    movies_names = link_movieID_to_title(movies_data)


    """
    Creating the list that will store the results.
    It breaks when it reaches the number of pairs the user asked for
    """
    result = []
    for userID1, userID2, movieID in user_pairs_list:
        if movieID in movies_names:
            result.append((userID1, userID2, movies_names[movieID]))
            if len(result) >= k:
                break
    return result

"""
Printing of the results is done in a seperate function (as adviced)
"""

def print_user_pairs(results):
    if not results:
        print("No user pairs were found! ")
    else:
        print(f"\n{'Χρήστης 1':<10} {'Χρήστης 2':<10} {'Τίτλος Ταινίας':<40}")
        print("_" * 60)
        print("\n")
        for userID1, userID2, movie_name in results:
            print(f"{userID1:<10} {userID2:<10} {movie_name:<40}")



def dominance (ratings_data, movies_data):
    """
    Creating an empty dictionary to store movie ratings grouped by their IDs.
    If there is no entry for a movieID inside the dictionary (first time reading it),
    we use the .setdefault and add an empty list as the default value
    """

    movie_ratings = {}
    for _, movieID, rating, _ in ratings_data:
        movie_ratings.setdefault(movieID, []).append(rating)


    """
    Creating a dictionary for the average rating of each movie
    and the total ratings counts of each one
    """

    avg_rating_and_count = {}
    for movieID, ratings in movie_ratings.items():
        average_ratings = sum(ratings) / len(ratings)
        ratings_count = len(ratings)
        avg_rating_and_count[movieID] = (average_ratings, ratings_count)


    """
    Creating a list to hold the non-dominated movies
    """

    dominant_movies = []
    for movieID1, (movieID1_avg_ratings, movieID1_ratings_count) in avg_rating_and_count.items():
        dominated = False
        for movieID2, (movieID2_avg_ratings, movieID2_ratings_count) in avg_rating_and_count.items():
            if movieID1 == movieID2:
                continue
            if movieID1_avg_ratings <= movieID2_avg_ratings and movieID1_ratings_count <= movieID2_ratings_count:
                dominated = True
                break
        if not dominated:
            dominant_movies.append((movieID1, movieID1_avg_ratings, movieID1_ratings_count))


    movie_titles = link_movieID_to_title(movies_data)


    """
    Creating the final result list to return the non dominated movies
    with their avg ratings and ratings count
    """

    result = []
    for movieID, avg_rating, ratings_count in dominant_movies:
        if movieID in movie_titles:
            result.append((movie_titles[movieID], avg_rating, ratings_count))
    return result

"""
Printing of the results is done in a seperate function (as adviced)
"""
def print_dominance(results):
    if not results:
        print("No movies found that are not dominated by others.")
    else:
        print(f"\n{'Τίτλος Ταινίας':<40} {'Μέσο Rating':<15} {'Αριθμός Κριτικών':<15}")
        print("_" * 70)
        for movie_name, avg_rating, ratings_count in results:
            print(f"{movie_name:<40} {avg_rating:<15.2f} {ratings_count:<15}")


def iceberg(trimmed_ratings_data, movies_data, k, t):
    """
    Creating an empty dictionary to store movie ratings grouped by their IDs.
    If there is no entry for a movieID inside the dictionary (first time reading it),
    we use the .setdefault and add an empty list as the default value
    """

    movie_ratings = {}
    for _, movieID, rating, _ in trimmed_ratings_data:
        movie_ratings.setdefault(movieID, []).append(rating)
    """
    Creating a dictionary for the average rating of each movie
    and the total ratings counts of each one
    """

    avg_rating_and_count = {}
    for movieID, ratings in movie_ratings.items():
        average_ratings = sum(ratings) / len(ratings)
        ratings_count = len(ratings)
        avg_rating_and_count[movieID] = (average_ratings, ratings_count)

    """
    Creating a list for the movies that match the criteria given
    """

    iceberg_movies = []
    for movieID, (movieID_avg_ratings, movieID_ratings_count) in avg_rating_and_count.items():
        if movieID_avg_ratings > t and movieID_ratings_count >= k:
            iceberg_movies.append((movieID, movieID_avg_ratings, movieID_ratings_count))

    movie_titles = link_movieID_to_title(movies_data)


    """
    Creating the final result list to return the movies that match the criteria given
    """

    result = []
    for movieID, avg_rating, ratings_count in iceberg_movies:
        if movieID in movie_titles:
            result.append((movie_titles[movieID], avg_rating, ratings_count))
    return result

"""
Printing of the results is done in a seperate function (as adviced)
"""
def print_iceberg(results):
    if not results:
        print("No movies found that match these criteria. ")
    else:
        print(f"\n{'Τίτλος Ταινίας':<80} {'Μέσο Rating':<15} {'Αριθμός Κριτικών':<15}")
        print("_" * 110)
        for movie_name, avg_rating, ratings_count in results:
            print(f"{movie_name:<80} {avg_rating:<15.2f} {ratings_count:<15}")

def top_user(trimmed_ratings_data, k):
    """
    Creating an empty dictionary to store ratings, grouped by each userID
    If there is no entry for a userID inside the dictionary (first time reading it),
    we use the .setdefault and add an empty list as the default value
    """

    user_ratings = {}
    for userID, movieID, _, _ in trimmed_ratings_data:
        user_ratings.setdefault(userID, []).append(movieID)

    """
    Creating a dictionary to calculate the total amount of ratings for each user
    """

    total_ratings_count = {}
    for userID, movie_count in user_ratings.items():
        get_count= len(movie_count)
        total_ratings_count[userID] = get_count

    """
    Sorting the users in descending order based on their ratings count and returning a list of tuples
    """
    sorted_users = sorted(total_ratings_count.items(), key=lambda item: item[1], reverse=True)[:k]
    return sorted_users

"""
Printing of the results is done in a seperate function (as adviced)
"""

def print_top_user(results):
    if not results:
        print("No users found that match these criteria. ")
    else:
        print(f"\n{'Χρήστης':<30}{'Αριθμός Ταινιών':<30}")
        print("_" * 60)
        for userID, movie_count in results:
            print(f"{userID:<30} {movie_count:<30} ")



def movie_sample(movies_data, s):

    """
    Creating an empty dictionary to store movie titles grouped by their category.
    If there is no entry for a category inside the dictionary (first time reading it),
    we use the .setdefault and add an empty list as the default value
    We use <<for category in categories>> to parse all categories for a movie
    """

    movie_genres = {}
    for _, movie_name, categories in movies_data:
        for category in categories:
            movie_genres.setdefault(category, []).append(movie_name)
    """
    Creating the dictionary for the sampled movies for each category
    We calculate the sample size to be equal to the user entry and then
    we sample randomly the movies from the list
    """
    genre_sample = {}
    for category, movies in movie_genres.items():
        size_of_sample = int(len(movies) * (s / 100))
        genre_sample[category] = random.sample(movies, min(size_of_sample, len(movies)))
    return genre_sample

"""
Printing of the results is done in a seperate function (as adviced)
"""

def print_sample(results):
    """
    We print each movie below of the other
    """
    if not results:
        print("No movies found for the given sample percentage.")
    else:
        print(f"\n{'Είδος':<15} {'Τίτλος Ταινίας':<40}")
        print("_" * 60)
        for category, movies in results.items():
            print(f"{category:<15}")
            for movie in movies:
                print(f"{'':<15} {movie}")

def similar_users(trimmed_ratings_data, theta):

    """
    Creating a dictionary to store ratings, grouped by each userID
    If there is no entry for a userID inside the dictionary (first time reading it),
    we use the .setdefault and add an empty list as the default value
    UserID is the key and the value is each movie with its ratings
    """
    user_ratings = {}
    for userID, movieID, rating, _ in trimmed_ratings_data:
        user_ratings.setdefault(userID, {})[movieID] = rating

    """
    Creating a dictionary to store rated movies, grouped by each movieID
    If there is no entry for a movieID inside the dictionary (first time reading it),
    we use the .setdefault and add an empty list as the default value
    movieID is the key and the value is all the userIDs that have rated it
    """

    rated_movies = {}
    for userID, movieID, _, _ in trimmed_ratings_data:
        rated_movies.setdefault(movieID, []).append(userID)

    """
    We create a list that will be appended with the movies that match the criteria
    We consider only movies that are rated by multiple users
    We use a set to hold the already processed pairs so that we find them once
    and we ensure user1<user2 to avoid duplicates
    We find the common movies rated by users and add them to the list
    We calculate the cosine similarity and filter by the given theta
    We sort the similar users list based on the cosine similarity in descending order

    """
    processed_pairs = {}
    users_list = []

    for movieID, users in rated_movies.items():
        if len(users) > 1:
            for i in range(0,len(users)):
                for j in range(i + 1, len(users)):
                    user1, user2 = users[i], users[j]
                    if user1 > user2:
                        user1, user2 = user2, user1


                    if (user1, user2) not in processed_pairs:
                        processed_pairs[(user1, user2)] = True
                    else:
                        continue

                    common_movies = []
                    for movie in user_ratings[user1]:
                        if movie in user_ratings[user2]:
                            common_movies.append(movie)

                    if len(common_movies) >= 1:

                        numerator = sum(user_ratings[user1][movie] * user_ratings[user2][movie] for movie in common_movies)
                        denominator = (sum(user_ratings[user1][movie] ** 2 for movie in common_movies) ** 0.5) * (sum(user_ratings[user2][movie] ** 2 for movie in common_movies) ** 0.5)
                        cosine_similarity = numerator / denominator

                        if cosine_similarity >= theta:
                            users_list.append((user1, user2, cosine_similarity))

    users_list.sort(key=lambda item: item[2], reverse=True)
    return users_list


"""
Printing of the results is done in a seperate function (as adviced)
"""
def print_similar_users(results):
    if not results:
        print("No similar users found.")
    else:
        print(f"\n{'Χρήστης 1':<15}{'Χρήστης 2':<15}{'Cosine Similarity':<20}")
        print("_" * 50)
        for user1, user2, similarity in results:
            print(f"{user1:<15}{user2:<15}{similarity:<20.2f}")

"""
Functions that access data from the data-sets
"""


def read_movies():
    """
    Create empty list to store ratings data
    """
    movies_data = []
    """
    Open and read the ratings file
    """
    try:
        with open('/content/drive/My Drive/movies.dat', 'r', encoding='utf-8') as file:
            for line in file:
                movieID, title, genres = line.strip().split('::')
                movies_data.append([int(movieID), title, genres.split('|')])
        return movies_data
    except FileNotFoundError:
        print("Movies file couldn't be found. Terminating...")
        sys.exit(1)


def read_trimmed_ratings(sample_size=100000):
    """
    Create empty list to store ratings data
    """
    trimmed_ratings_data = []
    """
    Open and read the ratings file
    """
    try:
        with open('/content/drive/My Drive/ratings.dat', 'r', encoding='utf-8') as file:
            all_lines = file.readlines()
            sampled_lines = random.sample(all_lines, min(sample_size, len(all_lines)))
            for line in sampled_lines:
                userID, movieID, rating, timestamp = line.strip().split('::')
                trimmed_ratings_data.append([int(userID), int(movieID), float(rating), int(timestamp)])
        return trimmed_ratings_data
    except FileNotFoundError:
        print("Ratings file couldn't be found. Terminating...")
        sys.exit(1)

##############################################################################################################################################################################################

def main():
    print("Loading data from files. Please wait a few seconds...")
    movies_data = read_movies()
    trimmed_ratings_data = read_trimmed_ratings(sample_size=100000)

    print("Data loaded successfully! Now showing the menu:")

    while True:

        print("\n|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Aggregative Movie Preference Analyzer~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|")
        print("|                                                                                                        |")
        print("|[rating T1 T2]    Print all movies with an average rating greater than T1 and less than or equal to T2  |")
        print("|[top_movies K]    Print the K number of movies with the highest average rating score                    |")
        print("|[user_pairs K]    Print K number of user pairs that have rated the same movie                           |")
        print("|[dominance]       Print the movies that are not dominated by other movies                               |")
        print("|[iceberg K T]     Print movies with at least K number of reviews and average rating greater than T      |")
        print("|[top_user K]      Print the K number of users with the highest number of movie ratings                  |")
        print("|[movie_sample S]  Print a S% sample of movies from each category                                        |")
        print("|[similar_users Θ] Print users with similar movie taste based on their Cosine Similarity(greater than Θ) |")
        print("|[exit]            Exit the program                                                                      |")
        print("|________________________________________________________________________________________________________|\n")

        """
        Get user input
        Remove extra whitespace and split the input into the command part and the arguments part
        """
        user_input = input("Enter your option: ").strip().split()

        command = user_input[0]
        args = user_input[1:]

        if command == 'rating':
            if len(args) == 2:
                try:
                    t1, t2 = float(args[0]), float(args[1])
                    result = rating(trimmed_ratings_data,movies_data, t1, t2)
                    print_rating(result)
                except ValueError:
                    print("Invalid value type. Please enter float numbers only. ")
            else:
                print("Please enter 2 arguments for this command. ")
        elif command == 'top_movies':
            if len(args) == 1:
                try:
                    k = int(args[0])
                    result = top_movies(trimmed_ratings_data, movies_data, k)
                    print_top_movies(result)
                except ValueError:
                    print("Invalid value type. Please enter an integer number. ")
            else:
                print("Please enter 1 argument for this command. ")
        elif command == 'user_pairs':
            if len(args) == 1:
                try:
                    k = int(args[0])
                    if k <= 0:
                        print("Please enter a positive integer. ")
                        continue
                    result = user_pairs(trimmed_ratings_data, movies_data, k)
                    print_user_pairs(result)
                except ValueError:
                    print("Invalid value type. Please enter an integer number. ")
            else:
                print("Please enter 1 argument for this command. ")
        elif command == 'dominance':
            if len(args) == 0:
                result = dominance(trimmed_ratings_data, movies_data)
                print_dominance(result)
            else:
                print("Please don't enter arguments for this command. ")
        elif command == 'iceberg':
            if len(args) == 2:
                try:
                    k, t = int(args[0]), float(args[1])
                    result = iceberg(trimmed_ratings_data, movies_data, k, t)
                    print_iceberg(result)
                except ValueError:
                    print("Invalid value types. Please enter an integer and a float number in that order. ")
            else:
                print("Please enter 2 arguments for this command. ")
        elif command == 'top_user':
            if len(args) == 1:
                try:
                    k = int(args[0])
                    result = top_user(trimmed_ratings_data, k)
                    print_top_user(result)
                except ValueError:
                    print("Invalid value type. Please enter an integer.")
            else:
                print("Please enter 1 argument for this command. ")
        elif command == 'movie_sample':
            if len(args) == 1:
                try:
                    s = float(args[0])
                    if not (1 <= s <= 100):
                        print("Please enter a value between 1 and 100.")
                        continue
                    result = movie_sample(movies_data, s)
                    print_sample(result)
                except ValueError:
                    print("Invalid value type. Please enter a float number.")
            else:
                print("Please enter 1 argument for this command. ")
        elif command == 'similar_users':
            if len(args) == 1:
                try:
                    theta = float(args[0])
                    if not (-1 <= theta <= 1):
                        print("Please enter a value between -1 and 1.")
                        continue
                    result = similar_users(trimmed_ratings_data, theta)
                    print_similar_users(result)
                except ValueError:
                    print("Invalid value type. Please enter a float number.")
            else:
                print("Please enter 1 argument for this command. ")
        elif command == 'exit':
                print("Exiting the program.")
                break
        else:
                print("\nInvalid option! Try again.\n")

if __name__ == "__main__":
    main()