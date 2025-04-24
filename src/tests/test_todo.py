import pytest
from fastapi import status

from src import base_url


def test_get_todos(test_client, test_data):
    response = test_client.get(f'{base_url}')
    response_data = response.json()
    expected_data = [todo.model_dump() for todo in test_data]

    assert response.status_code == status.HTTP_200_OK
    assert len(response_data) == len(test_data)
    assert response_data == expected_data


def test_get_todo_item(test_client, test_data):
    response = test_client.get(f'{base_url}/1')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_data[0].model_dump()


def test_get_todo_item_nonexistent_id(test_client, test_data):
    nonexistent_id = len(test_data) + 1
    response = test_client.get(f'{base_url}/{nonexistent_id}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Item not found'}


def test_create_todo_item(test_client, test_data, test_todo_item_payload):
    next_id = len(test_data) + 1
    response = test_client.post(f'{base_url}', json=test_todo_item_payload)
    expected_response_cont = {**test_todo_item_payload, 'id': next_id}

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response_cont


def test_create_todo_item_invalid_payload(test_client, test_todo_item_payload):
    invalid_payload = {'some_field': 'some_value'}
    response = test_client.post(f'{base_url}', json=invalid_payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize('update_data, expected_response', [
    ({'description': 'Go outside NEW'}, {'id': 1, 'description': 'Go outside NEW', 'priority': 1}),
    ({'priority': 2}, {'id': 1, 'description': 'Go outside', 'priority': 2}),
    ({'description': 'Go outside NEW 2', 'priority': 3}, {'id': 1, 'description': 'Go outside NEW 2', 'priority': 3}),
    ({}, {'id': 1, 'description': 'Go outside', 'priority': 1})
], ids=[
    'update description',
    'update priority',
    'update description & priority',
    'no data for update (stayed as is, data was not updated to None!)'
])
def test_update_todo_item_update_one_field(test_client, update_data, expected_response):
    response = test_client.put(f'{base_url}/1', json=update_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


def test_update_todo_item_nonexistent_id(test_client, test_data):
    nonexistent_id = len(test_data) + 1
    update_data = {'description': 'Go outside NEW'}
    response = test_client.put(f'{base_url}/{nonexistent_id}', json=update_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Item not found'}


def test_delete_todo_item(test_client, test_data):
    len_before = len(test_data)
    response = test_client.delete(f'{base_url}/1')
    len_after = len(test_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Item with id 1 is removed'}
    assert len_before - len_after == 1
    assert not [x for x in test_data if x.id == 1]


def test_delete_todo_item_nonexistent_id(test_client, test_data):
    nonexistent_id = len(test_data) + 1
    response = test_client.delete(f'{base_url}/{nonexistent_id}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Item not found'}