import requests
import json
import os
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview
from dotenv import load_dotenv


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if 'apikey' in kwargs:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["language"] = kwargs["language"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', kwargs['apikey']),
                                    params=params)
            if json.loads(response.text)['code'] == 422:
                return {'sentiment': {'document':{'label':'none'}}}
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except Exception as err:
        # If any error occurs
        print("Network exception occurred")
        print(err)
    
    status_code = response.status_code
    print("With status {} ".format(status_code))
    
    json_data = json.loads(response.text)
    
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]["docs"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []

    # print (kwargs['dealerId'])
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=kwargs['dealerId'])

    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # print(json_result)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    if 'status' in json_result:
        if json_result['status'] == 404:
            return({'status':404})

    if json_result:
        reviews = json_result["reviews"]["docs"]
        # print(reviews)

        for review in reviews:
            if review['purchase'] == 'true':
                review_obj = DealerReview(name=review["name"], dealership=review["dealership"], review=review["review"],
                                    purchase=review["purchase"], purchase_date=review["purchase_date"], car_make=review["car_make"],
                                    car_model=review["car_model"], car_year=review["car_year"], sentiment=analyze_review_sentiments(review))
                results.append(review_obj)
            else:
                review_obj = DealerReview(name=review["name"], dealership=review["dealership"], review=review["review"], 
                                        purchase=review["purchase"], sentiment=analyze_review_sentiments(review))
                results.append(review_obj) 

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerReview):
    load_dotenv()

    apikey = os.environ['NLU_apikey']
    url = os.environ['NLU_url']

    text = dealerReview['review']
    version = '2022-04-07'
    feature = "sentiment"
    language = 'en'
    return_analyzed_text = True
    
    json_result = get_request(url, apikey=apikey, text=text, language=language, version=version, features=feature, return_analyzed_text=return_analyzed_text)
    return (json_result['sentiment']['document']['label'])
