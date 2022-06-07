import sqlite3
from collections import Counter


class DbConnect:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()


def movie_by_title(query):
    db_connect = DbConnect('netflix.db')
    query_title = f"""
                    SELECT 
                        title, country, release_year, listed_in, description 
                    FROM
                        netflix
                    WHERE title LIKE :substring_pattern
                    ORDER BY
                        release_year desc
                    LIMIT 
                        1
    """
    db_connect.cursor.execute(query_title, {"substring_pattern": f"%{query}%"})
    result = db_connect.cursor.fetchone()
    return {
        "title": result[0],
        "country": result[1],
        "release_year": result[2],
        "genre": result[3],
        "description": result[4]
    }


def movie_between_years(year1, year2):
    db_connect = DbConnect('netflix.db')
    query_year = f"""
                    SELECT 
                        title, release_year
                    FROM
                        netflix
                    WHERE release_year BETWEEN ? AND ?
                    ORDER BY
                        release_year desc
                    LIMIT 
                        100
    """
    db_connect.cursor.execute(query_year, (year1, year2))
    result = db_connect.cursor.fetchall()
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0],
                            "release_year": movie[1]
                            })
    return result_list


def movie_by_rating(viewers):
    db_connect = DbConnect('netflix.db')
    groups_parameters = {"children": ("'G',"),
                         "family": ("'G', 'PG', 'PG-13'"),
                         "adult": ("'R', 'NC-17'")}
    if viewers not in groups_parameters:
        return "Just children/family/adult por favor"
    wrapper_parameters = groups_parameters[viewers]
    query_rating = f"""
                    SELECT
                        title, rating, description
                    FROM
                        netflix
                    WHERE 
                        rating IN ({", ".join('?' * len(wrapper_parameters))})
                    ORDER BY
                        title desc
    """
    db_connect.cursor.execute(query_rating, wrapper_parameters)
    result = db_connect.cursor.fetchall()
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0],
                            "rating": movie[1],
                            "description": movie[2]})
    return result


print(movie_by_rating('family'))


def movie_by_genre(genre):
    db_connect = DbConnect('netflix.db')
    query_genre = f"""
                    SELECT 
                        title, country, release_year, description 
                    FROM
                        netflix
                    WHERE listed_in LIKE :substring_pattern
                    ORDER BY
                        release_year desc
                    LIMIT 
                        10
    """
    db_connect.cursor.execute(query_genre, {"substring_pattern": f"%{genre}%"})
    result = db_connect.cursor.fetchall()
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0],
                            "description": movie[1]})
    return result_list


def actors_played_two_times(actor1, actor2):
    db_connect = DbConnect('netflix.db')

    couple_of_actors = {"first_actor": f"%{actor1}%",
                        "second_actor": f"%{actor2}%"}
    query_actors = f"""
                    SELECT
                        `cast`
                    FROM
                        netflix
                    WHERE
                        `cast` LIKE :first_actor AND `cast` LIKE :second_actor
                    ORDER BY
                        `cast` desc
    """
    db_connect.cursor.execute(query_actors, couple_of_actors)
    result = db_connect.cursor.fetchall()
    actors_list = []
    for cast_tuple in result:
        actors_list.extend(cast_tuple[0].split(', '))

    full_list = []
    actor_count = Counter(actors_list)
    for actor, actor_count in actor_count.items():
        if actor not in [actor1, actor2] and actor_count > 2:
            full_list.append(actor)
    return full_list


# print(actors_played_two_times('Jack Black', 'Dustin Hoffman'))

def movie_by_filter(type_movie, year, genre):
    db_connect = DbConnect('netflix.db')
    filtered_parameters = {"type_m": f"{type_movie}",
                           "release_y": f"{year}",
                           "movie_g": f"%{genre}%"}
    query = """
                SELECT 
                    title, description
                FROM 
                    netflix
                WHERE 
                    `type`=:type_m 
                    AND release_year=:release_y 
                    AND listed_in 
                    LIKE :movie_g
    """
    db_connect.cursor.execute(query, filtered_parameters)

    result = db_connect.cursor.fetchall()
    return {
        "title": result[0],
        "description": result[1]
    }
# print(movie_by_filter('Movie', 2010, 'Dramas'))
