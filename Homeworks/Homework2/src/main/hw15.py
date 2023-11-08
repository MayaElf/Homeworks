# Please, complete the following task.
#
# You will work with this endpoint - https://api.punkapi.com/v2/beers/8
#  Need to write 2 tests:
# 1. Using requests method GET need to check that:
# * status code - 200
# * name - Fake Lager
# * abv - 4.7
# 2. Using requests method DELETE need to check that:
# * status code - 404
# * message - No endpoint found that matches '/v2/beers/8'
### Don't forget about requests library
# To install requests use this command - pip install requests
# PSS: I would like to recommend to use page #15 from slides from this lecture;
# small clue - correct using for 1st task will be - .json()[0]['your_key']
### Review
# Put me as reviewer please (@VAlexandrov911)

import requests


class TestAPI:
     url = "https://api.punkapi.com/v2/beers/8"

     def test_get_request(self):
         response = requests.get(self.url)
         expected_status_code = 200
         expected_name = "Fake Lager"
         expected_abv = 4.7

         for my_dict in response.json():
             if my_dict.get("name"):
                 actual_name = my_dict.get("name")
             if my_dict.get("abv"):
                 actual_abv = my_dict.get("abv")

         assert response.status_code == expected_status_code
         assert actual_name == expected_name
         assert actual_abv == expected_abv

     def test_delete_request(self):
         response = requests.delete(self.url)
         expected_status_code = 404
         expected_message = "No endpoint found that matches '/v2/beers/8'"

         assert response.status_code == expected_status_code
         assert response.json()['message'] == expected_message
