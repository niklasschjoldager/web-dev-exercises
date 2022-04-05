from bottle import default_app, delete, get, post, put, request, response, run, view
from g import REGEX_UUID4, TWEET_TEXT_MAX_LENGTH, TWEET_TEXT_MIN_LENGTH
import re
import time
import uuid


tweets = {
    "30bbfc87-47e9-43cc-91ef-ab97d04dc5a6": {
        "id": "30bbfc87-47e9-43cc-91ef-ab97d04dc5a6",
        "text": "cc",
        "created_at": 1645787430
    },
    "36119afd-1ad1-4de7-a021-fef72a13ab3f": {
        "id": "36119afd-1ad1-4de7-a021-fef72a13ab3f",
        "text": "Nice",
        "created_at": 1645787430
    },
    "55b792d5-2690-463f-95a5-e4cf1647dff8": {
        "id": "55b792d5-2690-463f-95a5-e4cf1647dff8",
        "text": "cc",
        "created_at": 1645787431
    }
}


############################################################
@post("/tweets")
def _():
    try:
        # Validate
        if not request.forms.get("tweet_text"):
            response.status = 400
            return "Tweet text is missing"

        tweet_text = request.forms.get("tweet_text").strip()

        if len(tweet_text) < TWEET_TEXT_MIN_LENGTH:
            response.status = 400
            return {
                "info": f"Tweets must be at least {TWEET_TEXT_MIN_LENGTH} character"
            }

        if len(tweet_text) > TWEET_TEXT_MAX_LENGTH:
            response.status = 400
            return {
                "info": f"Tweets can only have a maximum of {TWEET_TEXT_MAX_LENGTH} characters"
            }

        tweet_id = str(uuid.uuid4())
        tweet_created_at = int(time.time())
        tweet = {
            "id": tweet_id,
            "text": tweet_text,
            "created_at": tweet_created_at,
            "updated_at": 0
        }
        tweets[tweet_id] = tweet
        
        # Success
        response.status = 201
        return { "id": tweet_id }
    except Exception as ex:
        print(ex)
        response.status = 500
        return { 
            "info": "Ups, something went wrong" 
        }


############################################################
@get("/tweets")
def _():
    try:
        # Success
        return tweets
    except Exception as ex:
        print(ex)
        response.status = 500
        return { 
            "info": "Ups, something went wrong" 
        }


############################################################
@get("/tweets/<id>")
def _(id):
    try:
        # Validate
        if not re.match(REGEX_UUID4, id):
            response.status = 204
            return

        if id not in tweets:
            response.status = 204
            return

        # Success
        return tweets[id]
    except Exception as ex:
        print(ex)
        response.status = 500
        return  { "info": "Ups, something went wrong" }


############################################################
@put("/tweets/<id>")
def _(id):
    try:
        # Validate tweet ID
        if not re.match(REGEX_UUID4, id):
            response.status = 204
            return

        if id not in tweets:
            response.status = 204
            return

        if not request.forms.get("tweet_text"):
            response.status = 400
            return {
                "info": "Tweet text is missing"
            }

        # Validate tweet_text
        tweet_text = request.forms.get("tweet_text").strip()

        if len(tweet_text) < TWEET_TEXT_MIN_LENGTH:
            response.status = 400
            return {
                "info": f"Tweets must be at least {TWEET_TEXT_MIN_LENGTH} character"
            }

        if len(tweet_text) > TWEET_TEXT_MAX_LENGTH:
            response.status = 400
            return {
                "info": f"Tweets can only have a maximum of {TWEET_TEXT_MAX_LENGTH} characters"
            }

        # Update the tweet
        tweets[id]['text'] = tweet_text
        tweets[id]['updated_at'] = int(time.time())

        response.status = 201
        return tweets[id]
    except Exception as ex:
        print(ex)
        response.status = 500
        return  { "info": "Ups, something went wrong" }


############################################################
@delete("/tweets/<id>")
def _(id):
    try:
        # Validate
        if not re.match(REGEX_UUID4, id):
            response.status = 204
            return 

        # Check if tweet id is inside the tweets
        if id not in tweets:
            response.status = 204
            return
        
        # Delete the tweet
        tweets.pop(id)

        # Success
        return {
            "info": "Tweet deleted"
        }
    except Exception as ex:
        print(ex)
        response.status = 500
        return { 
            "info": "Ups, something went wrong" 
        }


############################################################
try:
    # Production
    import production

    application = default_app()
except:
    # Development
    run(host="127.0.0.1", port=3333, debug=True, reloader=True)
