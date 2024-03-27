from fastapi import FastAPI
import json
import urllib.request
from pydantic import BaseModel
from statistics import mean
import uvicorn

class Response(BaseModel):
    numbers : list = []
    windowPrevState: list = []
    windowCurrState: list = []
    avg: float

app = FastAPI()

def test_api_request(url):
        with urllib.request.urlopen(url) as response:
            message = json.load(response)
            if "numbers" in message:
                return message["numbers"]
            else:
                return []

windowPrevState = []
windowCurrState = []
windowSize = 10

def get_numbers_list(numberid):
    if numberid == 'p':
        numbers = test_api_request('http://20.244.56.144/test/primes')
    if numberid == 'f':
        numbers = test_api_request('http://20.244.56.144/test/fibo')
    if numberid == 'e':
        numbers = test_api_request('http://20.244.56.144/test/even')
    if numberid == 'e':
        numbers = test_api_request('http://20.244.56.144/test/rand')  

    while len(numbers) > windowSize:
        numbers.pop(0)

    return numbers

@app.get("numbers/{numberid}", response_model= Response)
def numbers(numberid, response:Response):
    numbers = list(set(get_numbers_list(numberid)))
    windowPrevState = windowCurrState
    windowCurrState = numbers
    response.numbers = numbers
    response.windowPrevState = windowPrevState
    response.windowCurrState = windowCurrState
    response.avg = mean(windowCurrState)
    return response.model_dump()


if __name__ == "__main__":
    uvicorn.run( host="0.0.0.0", port=9876)