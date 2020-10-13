# importing base64, json, requests and urllib.parse
import base64
import requests
import urllib.parse

# creating variables for client ID and Secret

clientId = input("Enter your clientId: ")
clientSecret = input("Enter your clientSecret: ")
while True:
    def AccessToken(clientId, clientSecret):
        # Authorizing to spotify
        TokenUrl = 'https://accounts.spotify.com/api/token'
        headers = {}
        data = {}
        # creating authorization string + encoding
        string = f"{clientId}:{clientSecret}"
        stringBytes = string.encode('ascii')
        base64Bytes = base64.b64encode(stringBytes)
        base64String = base64Bytes.decode('ascii')
        # this process was found on: https://stackabuse.com/encoding-and-decoding-base64-strings-in-python/

        # adding information to the headers and data.
        headers['Authorization'] = "Basic " + base64String
        data['grant_type'] = "client_credentials"

        # request authentication token
        r = requests.post(TokenUrl, headers=headers, data=data)

        # see whether the returning code is an error or not
        if r.status_code == 200:
            # get token out of request
            token = r.json()['access_token']
            return token
        else:
            # get error status
            print("Couldn't get Authtoken from Spotify")
            print("Error code: " + str(r.status_code))
            return r.status_code

    def Search(token, artist):
        # Searching on Spotify
        SearchUrl = 'https://api.spotify.com/v1/search'
        headers = {}
        params = {}
        headers['Authorization'] = "Bearer " + token
        hexquery = urllib.parse.quote_plus(artist)
        params['q'] = hexquery
        params['type'] = "artist"
        r = requests.get(SearchUrl, headers=headers, params=params)

        # see whether the returning code is an error or not
        if r.status_code == 200:
            # get searched data
            jsondata = r.json()
            return jsondata
        else:
            # get error status
            print("Couldn't search on Spotify")
            print("Error code: " + str(r.status_code))
            return r.status_code


    token = AccessToken(clientId, clientSecret)
    # to see what Authtoken you get use: "print(token)"

    # if the token returns an error code instead of an Authtoken stop the program
    if type(token) == int:
        break

    # input an artist to search for
    artist = input('Enter the artist you want to search (type exit or press enter to quit): ')
    # stop the program if exit is entered
    if artist == 'exit' or artist == '':
        print('Thank you for using my program!')
        break

    # input an amount of artists you want to seach, if this is a string or a number higher than 10 or below 1 set it to the default
    n_artists = input('How many results do you want to show? (Max 10) (Default 5): ')
    if n_artists.isdigit() == True:
        n_artists = int(n_artists)
        if n_artists > 10 or n_artists <= 0:
            n_artists = 5
    if type(n_artists) == str:
        n_artists = 5

    # input an amount of genres you want to see, if this is a string or a number higher than 5 or below 1 set it to the default
    n_genres = input('How many genres do you want to show? (Max 5) (Default 3): ')
    if n_genres.isdigit() == True:
        n_genres = int(n_genres)
        if n_genres > 5 or n_genres <= 0:
            n_genres = 3
    if type(n_genres) == str:
        n_genres = 3

    search = Search(token, artist)

    # stop the program if search gives an error code
    if type(search) == int:
        break

    # creating a sort of table to better show artist, genre and popularity
    print('{: <40} {: <80} {: <20}'.format('Artist', 'Top ' + str(n_genres) + ' genres', 'Popularity'))
    print('{: <40} {: <80} {: <20}'.format('------', '------------', '----------'))
    # every line there will be an artists name, a list of the genres and their popularity
    for each in search['artists']['items'][:n_artists]:
        name = each['name']
        genres = each['genres']
        joinedgenres = ', '.join(genres[:n_genres])
        popularity = each['popularity']
        print('{: <40} {: <80} {: <20}'.format(name, joinedgenres, popularity))
    print('{: <40} {: <80} {: <20}'.format('------', '------------', '----------'))
