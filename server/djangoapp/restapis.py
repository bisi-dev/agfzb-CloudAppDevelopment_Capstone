import requests
import json
from requests.auth import HTTPBasicAuth
import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        print("Network exception occurred")
    
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def post_request(url, json_payload, **kwargs):
    response = requests.post(url, params=kwargs, json=json_payload)
    return response.status_code


def get_dealers_from_cf(url, **kwargs):
    results = []

    json_result = get_request(url)

    
    if json_result:
        dealers = json_result['body']['dealerships']

        for dealer_doc in dealers:
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


def get_dealer_reviews_from_cf(url, dealer_Id):
    results = []

    json_result = get_request(url, dealerId=dealer_Id)

    if json_result['statusCode'] == 200:
        reviews = json_result['body']['data']

        for review in reviews:
            print("------------------------")
            print(review)
            print("------------------------")
            review_obj = DealerReview(car_make=review["car_make"], car_model=review["car_model"], car_year=review["car_year"],
                                   dealership=review["dealership"], #id=review["id"], 
                                   name=review["name"],
                                   purchase=review["purchase"], purchase_date=review["purchase_date"],
                                   review=review["review"], sentiment="positive")
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    return results


def get_dealer_by_state_from_cf(url, st):
    results = []

    json_result = get_request(url, state=st)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result['body']['dealerships']

        for dealer_doc in dealers:
            # Get its content in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


def get_dealer_by_id_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url, id = dealer_id)

    if json_result:
        dealers = json_result['body']['dealerships']

        for dealer_doc in dealers:
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


def analyze_review_sentiments(text):
    print("Running review sentiment analyzer")
    params = dict()
    params["text"] = text
    params["version"] = "2021-08-01"
    params["features"] = "sentiment"
    #params["return_analyzed_text"] = kwargs["return_analyzed_text"]
    url_nlu = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/3989d100-73f9-4a68-abad-cbdef6909f55/v1/analyze"
    api_key = "Rf3Aa5q1LOMYI2H7wp5qAcU0z-3fm60fzfdpNe6Gn0wN"
    response = requests.get(url_nlu, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
    
    json_data = json.loads(response.text)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    print(json_data)

    if status_code == 200:
        sentiment = json_data["sentiment"]["document"]["label"]
        return sentiment
    else:
        return "No sentiment found. Reason: " + str(json_data["error"])



