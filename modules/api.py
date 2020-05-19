import requests

def get_api():
    resp = requests.get('https://api.openweathermap.org/data/2.5/weather?id=3118594&appid=97652d6130c871e828dd201730ec6f06')
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('Error GET /tasks/ {}'.format(resp.status_code))
    # for item in resp.json():
        # print('{} {}'.format(item['id'], item['summary']))
    print(resp.json())

if __name__ == "__main__":
    get_api()