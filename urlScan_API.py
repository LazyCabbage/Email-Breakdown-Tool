import json
import time

import requests

CONTENT_TYPE = 'application/json'
SECONDS_TO_GENERATE_A_RESULT = 60
SECONDS_TO_WAIT_BETWEEN_REQUESTS_TO_AVOID_429_ERRORS = 5


def scan_link(link_to_check: str, API_KEY: str = '2c036869-fcd7-41e3-848e-d41edab47e57') -> str:
    # setup the request
    headers = {'API-Key': API_KEY, 'Content-Type': CONTENT_TYPE}
    data = {"url": link_to_check, "visibility": "public"}

    # avoid breaking the
    time.sleep(SECONDS_TO_WAIT_BETWEEN_REQUESTS_TO_AVOID_429_ERRORS)

    #let the user know where we are at
    print('Checking URL: ', link_to_check)

    # send the request and store what we get back into a variable called "response" note that this response
    # does not tell us whether or not the link is malicious, it just confirms that urlscan.io got the data
    # and that it also sends back a link to a page where it will store the result.
    response = requests.post('https://urlscan.io/api/v1/scan/', headers=headers, data=json.dumps(data))

    print(response)

    # now, if there was some error, we need to capture that and cease further processing on it.
    if response.status_code >= 400:
        print('[ERROR] urlscanner choked on this URL: ', link_to_check)
        return 'NOT ABLE TO SUBMIT'

    # put the "response" into JSON  format (easier to work with) and get the entry inside the response labelled "api".
    # this contains the URL that contains the result in machine-readable format
    result_URL = response.json()['api']

    # now, if we query the above URL too quickly, the website will not have enough time to search its DB and build the
    # results page, so we need to give it some time before we try to get a result.
    time.sleep(SECONDS_TO_GENERATE_A_RESULT)

    # now go get the result from the URL provided.
    result = requests.get(result_URL)

    # again, check to see if we got an error first
    if result.status_code >= 400:
        print('[ERROR] urlscanner was able to submit this URL, but there was not response: ', link_to_check)
        return 'ABLE TO SUBMIT BUT NO RESULT PROVIDED'

    # if re got this far, then there was a result. Report accordingly.
    if result.json()['verdicts']['urlscan']['malicious']:
        return 'MALICIOUS'

    if not result.json()['verdicts']['urlscan']['malicious']:
        return 'NON-MALICIOUS'

    # if we still haven't hit a return statement, then there is something wrong
    return 'CONFUSED'

# ##############################################################################################
