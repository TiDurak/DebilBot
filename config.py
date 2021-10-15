import os

try:
    os.environ['token']
except KeyError:
    print('Config variable "token" is unreachable. Please, add this!')
    exit()

settings = {
    'token': os.environ['token'],
    'prefix': 'd.'
}