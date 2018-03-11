from chalice import Chalice
import os
import sys
import boto3

app = Chalice(app_name='setti')

def get_table(name):
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(os.environ[name])

@app.route('/')
def index():
    return {"hello": "world"}

@app.route('/number_settings/{number}')
def number_settings(number):
    try:
        request = app.current_request
        if request.method == 'GET':
            settings_table = get_table('SETTINGS_TABLE')
            t = get_table('SETTINGS_TABLE')
            results_dict = t.get_item(Key={
                'number': number
            })
            return {"response": results_dict['Item']}
    except:
        app.log.error("Unexpected error: " + str(sys.exc_info()))
        return {"error": "Something is wrong."}

@app.route('/numbers')
def numbers():
    try:
        request = app.current_request
        #print(request.query_params)
        if request.method == 'GET':
            settings_table = get_table('SETTINGS_TABLE')
            t = get_table('SETTINGS_TABLE')
            results_dict = t.scan(
                AttributesToGet=[
                    "number",
                    "proj",
            ])
            return {"response": results_dict['Items']}
    except:
        app.log.error("Unexpected error: " + str(sys.exc_info()))
        return {"error": "Something is wrong."}

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
