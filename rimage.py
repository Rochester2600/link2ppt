# antitree
# module to get a random related giphy image

import requests


class giphy():

    def __init__(self):
        self.GIPHYBASE = 'http://api.giphy.com/v1/gifs/search?q=%s&api_key=%s'
        self.GIPHYAPI = 'dc6zaTOxFJmzC'

    def get_image(self, terms):
        search = '+'.join(terms)
        image = ""
        url = self.GIPHYBASE % (search, self.GIPHYAPI)
        try:
            r = requests.get(url)
            images = r.json()
            image = str(images["data"][0]["images"]["original"]["url"])
        except Exception as e:
            print("Failed to get image %s:" % e)
            return None

        return image


if __name__ == '__main__':
  print("Classy...looking for balls")
  a = giphy()
  b = a.get_image(["balls","donkey","and","yup","ok"])
  print(b)
