# name: Louie Bloomberg
# date:
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 5 (out of 5) -- if I don't change this, I agree to get 0 points.

import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('BeatlesMusic')

def create_song():
    song = input("Please the song's name: ")


    table.put_item(
        Item={
            "Song": song,
            "Album(s)": []
        }
    )


def print_music(music):
    """Print a single movie's details in a readable format.
    song is replaced by music to prevent errors"""
    song = music.get("Song", "Unknown Title")
    year = music.get("Year", "Unknown Year")
    albums = music.get("Album(s)", "No Album(s)")
    length = music.get("Length", "Unknown Length")

    print(f"  Song Name : {song}")
    print(f"  Year Released : {year}")
    print(f"  Album(s): {albums}")
    print(f"  Length: {length} sec")
    print(f"                ")


def print_all_songs():
    """Scan the entire Movies table and print each item."""


    # scan() retrieves ALL items in the table.
    # For large tables you'd use query() instead — but for our small
    # dataset, scan() is fine.
    response = table.scan()
    items = response.get("Items", [])

    if not items:
        print("No songs found. Make sure your DynamoDB table has data.")
        return

    print(f"Found {len(items)} song(s):\n")
    for song in items:
        print_music(song)


def update_album():
    song = input("Please enter the song name: ")
    album = input("Please enter the album for which the song belongs to: ")

    try:
        response = table.get_item(Key={"Song": song})
        item = response.get("Item")
        if not item:
            print(f"Error in updating song's album")
            return
    except Exception as e:
        print(f"Error in updating song's album.")
        return

    table.update_item(
        Key={"Song": song},
        UpdateExpression="SET #albums = list_append(#albums, :a)",
        ExpressionAttributeNames={"#albums": "Album(s)"},
        ExpressionAttributeValues={':a': [album]}
    )



def delete_song():
    song = input("Please enter the song's name: ")
    table.delete_item(
        Key={
            "Song": song
        }
    )

def query_song():
    song = input("Please enter the song's name: ")
    response = table.get_item(
        Key={
            "Song": song
        }
    )
    song = response.get("Item")

    albums_list = song["Album(s)"]

    if song == "None":
        print("Song not found.")
        return

    if not albums_list:
        print("Song is in no albums.")
        return

    num_albums = len(albums_list)

    if num_albums == 1:
        print(f"'{song}' is in 1 album.")
    else:
        print(f"'{song}' is in {num_albums} albums.")



def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new song")
    print("Press R: to READ all songs")
    print("Press U: to UPDATE a song (add an album)")
    print("Press D: to DELETE a song")
    print("Press Q: to QUERY the number of albums a song is in")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_song()
        elif input_char.upper() == "R":
            print_all_songs()
        elif input_char.upper() == "U":
            update_album()
        elif input_char.upper() == "D":
            delete_song()
        elif input_char.upper() == "Q":
            query_song()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()
