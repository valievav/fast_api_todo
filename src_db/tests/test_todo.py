import uuid

import pytest
from fastapi import status

from src_db import base_url


def test_get_todos_db_has_no_data(test_client, test_todo_item_payload):
    response = test_client.get(f'{base_url}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_todos_db_has_data(test_client, test_todo_item_payload, existing_todo_entry):
    response = test_client.get(f'{base_url}')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]['description'] == test_todo_item_payload['description']


def test_get_todo_item(test_client, test_todo_item_payload, existing_todo_entry):
    existing_uid = existing_todo_entry['uid']
    response = test_client.get(f'{base_url}/{existing_uid}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['description'] == test_todo_item_payload['description']


def test_get_todo_item_nonexistent_uid(test_client, test_todo_item_payload, existing_todo_entry):
    nonexistent_uid = uuid.uuid4()
    response = test_client.get(f'{base_url}/{nonexistent_uid}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Item not found'}


def test_create_todo_item(test_client, test_todo_item_payload):
    response = test_client.post(f'{base_url}', json=test_todo_item_payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['description'] == test_todo_item_payload['description']
    assert set(test_todo_item_payload.items()).issubset(set(response.json().items()))


def test_create_todo_item_invalid_payload(test_client):
    invalid_payload = {'some_field': 'some_value'}
    response = test_client.post(f'{base_url}', json=invalid_payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize('update_data, expected_response', [
    ({'description': 'Write tests NEW'}, {'description': 'Write tests NEW', 'priority': 2}),
    ({'priority': 3}, {'description': 'Write tests', 'priority': 3}),
    ({'description': 'Write tests NEW 2', 'priority': 1}, {'description': 'Write tests NEW 2', 'priority': 1}),
    ({}, {'description': 'Write tests', 'priority': 2})
], ids=[
    'update description',
    'update priority',
    'update description & priority',
    'no data for update (stayed as is, data was not updated to None!)'
])
def test_update_todo_item_update_one_field(test_client, update_data, expected_response, existing_todo_entry):
    existing_uid = existing_todo_entry['uid']
    response = test_client.put(f'{base_url}/{existing_uid}', json=update_data)

    assert response.status_code == status.HTTP_200_OK
    assert set(expected_response.items()).issubset(response.json().items())




def test_update_todo_item_nonexistent_uid(test_client, existing_todo_entry):
    nonexistent_uid = uuid.uuid4()
    update_data = {'description': 'Go outside NEW'}
    response = test_client.put(f'{base_url}/{nonexistent_uid}', json=update_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Item not found'}


def test_delete_todo_item(test_client, existing_todo_entry):
    existing_uid = existing_todo_entry['uid']
    response = test_client.delete(f'{base_url}/{existing_uid}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': f'Item with id {existing_uid} is removed'}


def test_delete_todo_item_nonexistent_id(test_client, existing_todo_entry):
    nonexistent_uid = uuid.uuid4()
    response = test_client.delete(f'{base_url}/{nonexistent_uid}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Item not found'}
