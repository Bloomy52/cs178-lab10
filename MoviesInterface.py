# name: Louie Bloomberg
# date: 3/5/26
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 5 (out of 5) -- if I don't change this, I agree to get 0 points.

import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Movies')

def create_movie():
    title = input("Please enter a movie title: ")


    table.put_item(
        Item={
            "Title": title,
            "Ratings": []
        }
    )


def print_movie(movie):
    """Print a single movie's details in a readable format."""
    title = movie.get("Title", "Unknown Title")
    year = movie.get("Year", "Unknown Year")
    ratings = movie.get("Ratings", "No ratings")
    genres = movie.get("Genre", "No genres")
    runtime = movie.get("Runtime (min)", "Unknown Runtime")

    # Ratings is a nested map in the table — handle it gracefully
    # ratings = movie.get("Ratings", {})
    # rating_str = ", ".join(f"{k}: {v}" for k, v in ratings.items()) if ratings else "No ratings"

    print(f"  Title : {title}")
    print(f"  Year  : {year}")
    print(f"  Ratings: {ratings}")
    print(f"  Genres: {genres}")
    print(f"  Runtime: {runtime} min")
    print(f"                ")


def print_all_movies():
    """Scan the entire Movies table and print each item."""


    # scan() retrieves ALL items in the table.
    # For large tables you'd use query() instead — but for our small
    # dataset, scan() is fine.
    response = table.scan()
    items = response.get("Items", [])

    if not items:
        print("No movies found. Make sure your DynamoDB table has data.")
        return

    print(f"Found {len(items)} movie(s):\n")
    for movie in items:
        print_movie(movie)


def update_rating():
    title = input("Please enter a movie title: ")
    rating = int(input("Please enter the rating (out of 100) as an integer: "))

    try:
        response = table.get_item(Key={"Title": title})
        item = response.get("Item")
        if not item:
            print(f"Error in updating movie rating")
            return
    except Exception as e:
        print(f"Error in updating movie rating.")
        return

    table.update_item(
        Key={"Title": title},
        UpdateExpression="SET Ratings = list_append(Ratings, :r)",
        ExpressionAttributeValues={':r': [rating]}
    )



def delete_movie():
    title = input("Please enter a movie title: ")
    table.delete_item(
        Key={
            "Title": title
        }
    )

def query_movie():
    title = input("Please enter a movie title: ")
    response = table.get_item(
        Key={
            "Title": title
        }
    )
    movie = response.get("Item")

    ratings_list = movie["Ratings"]

    if movie == "None":
        print("Movie not found.")
        return

    if not ratings_list:
        print("Movie has no ratings.")
        return

    average_rating = sum(ratings_list) / len(ratings_list)
    print(f"Average rating for '{title}' is ", average_rating, " out of 100.")



def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new movie")
    print("Press R: to READ all movies")
    print("Press U: to UPDATE a movie (add a review)")
    print("Press D: to DELETE a movie")
    print("Press Q: to QUERY a movie's average rating")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_movie()
        elif input_char.upper() == "R":
            print_all_movies()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_movie()
        elif input_char.upper() == "Q":
            query_movie()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()
