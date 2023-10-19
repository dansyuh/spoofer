"""
Debug spoofer made for API,
this would not be used in a stable environment and is purely for debugging/testing.
"""
import asyncio
import time
from random import randint
from uuid import uuid4

import requests
from faker import Faker
from pymongo import MongoClient

client = MongoClient(uuidRepresentation='standard')
database = client.get_database(name='api')
collection = database.get_collection('notes')

faker = Faker('en_GB')


async def generate(url: str, amount: int):
    generated = 0
    started = time.time()

    for _ in range(0, amount):
        generated += 1
        requests.post(url, json={
            '_id': str(uuid4()),
            'superuser': False,
            'locked': False,
            'email': faker.free_email(),
            'reference': f'QS-{randint(100000, 999999)}',
            'password': faker.password(),
            'personal': {
                'title': 'Mr',
                'name': faker.first_name(),
                'surname': faker.last_name_nonbinary(),
                'gender': 'male',
                'birthdate': faker.date('%d/%m/%y')
            }
        })

        ended = time.time()
        print(f'Generated {generated} users in {round(ended - started)} seconds.')


def generate_type() -> bool:
    url = str(input('input the url.\n'))

    if len(url) == 0:
        url = 'http://localhost:8000/api/v1/user'

    if type(url) is not str:
        print('value presented is not a string.')
        return False

    amount = int(input('input the amount:\n'))

    if type(amount) is not int:
        print('value presented is not an integer.')
        print(type(amount))
        return False

    asyncio.run(generate(str(url), amount))
    return True


if __name__ == '__main__':
    generate_type()
