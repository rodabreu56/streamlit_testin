import urllib.request

def download_image(url, file_name):
    full_file_name = file_name + ".png"
    urllib.request.urlretrieve(url, full_file_name)

download_image('https://flow.capeanalytics.com/api/v3/img/e8eb5a69-0675-4c82-b83e-29571c394a95/22','test_image01')