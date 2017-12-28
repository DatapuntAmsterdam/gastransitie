"""
Download the CBS and Amsterdam buurt codes, so that datasets can be linked.
"""
import json
import requests


BUURT_API_URL = 'https://api.data.amsterdam.nl/gebieden/buurt/'


def _get_buurt_codes(uri):
    """
    Given a buurt URI, return the Amsterdam buurt code and CBS buurt code.
    """
    result = requests.get(uri)
    data = json.loads(result.text)

    return data['volledige_code'], data['buurtidentificatie']


def _get_buurt_uris(uri):
    """
    Iterate over buurten yielding buurt URIs in the data.amsterdam.nl API.
    """
    next_page_uri = uri

    while next_page_uri is not None:
        result = requests.get(next_page_uri)
        data = json.loads(result.text)

        for r in data['results']:
            yield r['_links']['self']['href']
        next_page_uri = data['_links']['next']['href']

    raise StopIteration


def get_buurt_mapping():
    """
    Return iterator that yields Amsterdam and CBS buurt code tuples.
    """
    return (_get_buurt_codes(uri) for uri in _get_buurt_uris(BUURT_API_URL))


def main():
    """
    Write Amsterdam buurt code to CBS buurtcode mapping to standard out.
    """
    print('buurtcode,cbscode')
    for buurtcode, cbscode in get_buurt_mapping():
        print('{},{}'.format(buurtcode, cbscode))


if __name__ == '__main__':
    main()
