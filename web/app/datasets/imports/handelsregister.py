"""
Download per buurt alle vestigingen van dataselectie.
"""
import logging
# import argparse
import requests
from datasets.models import bag
from datasets.models.handelsregister import Handelsregister

from .datapunt_auth import auth

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


# setup auth tokens!
# log.debug(auth.token_employee_plus)

headers = {'Authorization': f'Bearer {auth.token_employee_plus}'}

url_hr = "https://acc.api.data.amsterdam.nl/dataselectie/hr/export/"

params = {
    'buurt_naam': 'AMC',
    'shape': [],
    # 'dataset'=ves
    # 'access_token=eyJhbGciOiJFUzI1NiIsImtpZCI6IjM4OWE5ZjY4LWUyNGUtNDcxNi1hMTFjLTFlZWY0NzgwNGNjNiJ9.eyJpc3MiOiJodHRwczovL2FwaS5kYXRhLmFtc3RlcmRhbS5ubC9vYXV0aDIvYXV0aG9yaXplIiwic3ViIjoiTWVkZXdlcmtlciIsImlhdCI6MTUxOTgxMDM1OSwibmJmIjoxNTE5ODEwMzQ5LCJleHAiOjE1MTk4NDYzNTksImp0aSI6IjRjZDRmZmQzLWRmZjctNDcwMy05NjZkLTJkNzI5ODA5MGNhNSIsInNjb3BlcyI6WyJIUi9SIiwiQlJLL1JTIiwiQlJLL1JPIiwiV0tQQi9SQkRVIiwiTU9OL1JCQyIsIk1PTi9SRE0iXX0.SXNkP3ujvKjYavNa6CC0jnkXGv-nVoXv9hbBbnDqEflXEmJZRLt3lxzgJ4A6XeIp3-DWWwLRk9ui6YsiQ5EPeQ'
}


def get_hr_for_all_buurten():

    Handelsregister.objects.all().delete()

    for b in bag.BagBuurt.objects.all().order_by('naam'): # .filter(naam='Amerikahaven'):
        params['buurt_naam'] = b.naam
        response = requests.get(url_hr, params=params, headers=headers)

        log.debug(response.status_code)
        csv = response.text
        inschrijvingen = csv.split('\n')

        csvheaders = inschrijvingen[0]
        data = {}
        # store every inscrhijving.
        for ves in inschrijvingen[1:]:
            data = dict(zip(csvheaders.split(';'), ves.split(';')))

            h = Handelsregister.objects.create(
                buurt_id=b.id,
                buurt_naam=b.naam,
                data=data,
            )

            h.save()

        log.debug(f'{b.naam}: {len(inschrijvingen)}')


# get_hr_for_all_buurten()
# return response
