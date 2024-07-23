import json
import urllib.request

def lambda_handler(event, context):
    try:
        API_key = "de61425c8f044398975130805242307"
        city = "London"
        url = f"https://api.weatherapi.com/v1/current.json?key={API_key}&q={city}&aqi=no"
        
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            weather_data = json.loads(data)
            
            return {
                'statusCode': 200,
                'body': json.dumps(weather_data)
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }