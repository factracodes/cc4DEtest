# Import required libraries
import json
import csv
from datetime import datetime

# load data from json file
with open('restaurant_data.json', 'r', encoding="utf8") as json_file: # encoding is used to decode the raw data file
    data = json.load(json_file)

# initialise country codes into a dictionary
with open('Country-Code.csv', 'r') as country_file:
    country_codes = {}
    country_reader = csv.DictReader(country_file)
    for row in country_reader:
        country_codes.update({row['Country Code']:row['Country']})

# initialize dictionary with each rating being a list, for question 3
ratings = {'Excellent': [], 'Very Good': [], 'Good': [], 'Average': [], 'Poor': []}

# write to the csv with similar encoding
with open('restaurant_data.csv', 'w', newline='', encoding="utf8") as rest_data, open('restaurant_events.csv', 'w', newline='', encoding="utf8") as event_data:
    # specify columns required for restaurant header
    rest_fieldnames = ['id','name', 'country', 'city', 'user_votes', 'user_agr_rating', 'cuisines']
    rest_writer = csv.DictWriter(rest_data, fieldnames=rest_fieldnames)
    rest_writer.writeheader() # write header to csv file

    # specify columns required for header
    event_fieldnames = ['event_id','rest_id', 'rest_name', 'photo_url', 'title', 'start_date', 'end_date']
    event_writer = csv.DictWriter(event_data, fieldnames=event_fieldnames)
    event_writer.writeheader()


    # loop through each dictionary object to obtain data of all restaurants
    for d in data:
        restaurants = d['restaurants']

        # loop through each restaurant to obtain required values (QUESTION 1)
        for rest in restaurants:
            rest = rest['restaurant']
            id = rest['id']
            name = rest['name']
            country_id = str(rest['location']['country_id'])
            
            # filter out unknown country id
            if country_id not in country_codes.keys():
                country = "Dummy"
            else:
                country = country_codes[country_id]

            city = rest['location']['city']
            user_votes= rest['user_rating']['votes']
            user_agr_rating = float(rest['user_rating']['aggregate_rating'])
            cuisines = rest['cuisines']

            # save all required values into a dictionary object
            row = {'id': id, 'name': name, 'country': country, 'city': city, 'user_votes': user_votes, 'user_agr_rating' : user_agr_rating, 'cuisines': cuisines}
            # write values of each restaurant into a row of the csv file
            rest_writer.writerow(row)


            # if events are recorded by zomato for that restaurant (QUESTION 2)
            if 'zomato_events' in rest.keys():
                events = rest['zomato_events']
                
                # loop through each event that happened in the restaurant
                for event in events:
                    event = event['event']
                    start_date = datetime.strptime(event['start_date'], "%Y-%m-%d")
                    
                    # assume that "past event in the month of April 2019" starts in the month of April
                    if start_date.year == 2019 and start_date.month == 4:
                        row = dict.fromkeys(event_fieldnames, "NA") # populate rows as 'NA' first

                        # obtain required values for each event
                        row['event_id'] = event['event_id']
                        row['rest_id']= rest['R']['res_id']
                        row['rest_name'] = rest['name']
                        row['title'] = event['title']
                        row['start_date'] = event['start_date']
                        row['end_date'] = event['end_date']

                        # concatenate each url together
                        url = ''
                        for photo in event['photos']:
                            photo = photo['photo']
                            url += photo['url']
                            url += " "
                        
                        # if photo url for the event exists, replace the original NA string
                        if len(url) > 0:
                            row['photo_url'] = url

                        # write values of each restaurant into a row of the csv file
                        event_writer.writerow(row)


            # extract the rating information from each restaurant (QUESTION 3)
            rating_text = rest['user_rating']['rating_text']
            agr_rating = rest['user_rating']['aggregate_rating']

            # keep only the values for those ratings we are concerned about
            if rating_text in ratings.keys():
                ratings[rating_text].append(agr_rating) # add each rating to the list



# calculate the lowest and highest value for each rating to find its threshold
for k,v in ratings.items():
    lowest_val = min(v)
    highest_val = max(v)
    print(f'{k} Rating: {lowest_val} - {highest_val}')