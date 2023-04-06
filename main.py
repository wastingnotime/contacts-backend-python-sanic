import os
import uuid

from sanic import Sanic
from sanic.exceptions import BadRequest
from sanic.response import json, empty
from pony.orm import *
from dotenv import load_dotenv

# configuration --------------
load_dotenv()
environment = os.getenv("ENVIRONMENT")
db_location = os.getenv("DB_LOCATION")
is_debug = (environment != 'production')

# database --------------
set_sql_debug(is_debug)
db = Database()


class Contact(db.Entity):
    id = PrimaryKey(str)
    firstName = Required(str)
    lastName = Required(str)
    phoneNumber = Required(str)


db.bind(provider='sqlite', filename=db_location, create_db=True)
db.generate_mapping(create_tables=True)

# api --------------
app = Sanic("contacts")


@app.post('/contacts')
@db_session
def create_contact(request):
    """Creates a contact"""
    try:
        contact_payload = request.json
    except BadRequest:
        return json({"error": "bad formatted json payload"}, status=400)

    if contact_payload is None or contact_payload == {}:
        return json({"error": "bad formatted json payload"}, status=400)
    if contact_payload.get('firstName') is None:
        return json({"error": "firstName must be informed"}, status=400)
    if contact_payload.get('lastName') is None:
        return json({"error": "lastName must be informed"}, status=400)
    if contact_payload.get('phoneNumber') is None:
        return json({"error": "phoneNumber must be informed"}, status=400)

    try:
        contact_id = str(uuid.uuid4())

        Contact(id=contact_id,
                firstName=contact_payload['firstName'],
                lastName=contact_payload['lastName'],
                phoneNumber=contact_payload['phoneNumber'])

        return empty(201, {'Location': f"{request.path}/{contact_id}"})
    except ValueError:
        return empty(500)


@app.get('/contacts')
@db_session
def get_all_contacts(_):
    """Gets all contacts"""
    contacts_payload = []

    contacts = select(c for c in Contact)
    for c in contacts:
        contacts_payload.append(c.to_dict())

    return json(contacts_payload)


@app.get('/contacts/<contact_id>')
@db_session
def get_contact(_, contact_id):
    """Gets a specific contact"""
    try:
        contact = Contact[contact_id]
    except ObjectNotFound:
        return empty(404)

    return json(contact.to_dict())


@app.put('/contacts/<contact_id>')
@db_session
def update_contact(request, contact_id):
    """Updates a contact"""
    try:
        contact = Contact[contact_id]
    except ObjectNotFound:
        return empty(404)

    try:
        contact_payload = request.json
    except BadRequest:
        return json({"error": "bad formatted json payload"}, status=400)

    if contact_payload is None or contact_payload == {}:
        return json({"error": "bad formatted json payload"}, status=400)
    if contact_payload.get('firstName') is None:
        return json({"error": "firstName must be informed"}, status=400)
    if contact_payload.get('lastName') is None:
        return json({"error": "lastName must be informed"}, status=400)
    if contact_payload.get('phoneNumber') is None:
        return json({"error": "phoneNumber must be informed"}, status=400)

    try:
        contact.firstName = contact_payload['firstName']
        contact.lastName = contact_payload['lastName']
        contact.phoneNumber = contact_payload['phoneNumber']

        return empty(204)
    except ValueError:
        return empty(500)


@app.delete('/contacts/<contact_id>')
@db_session
def delete_contact(_, contact_id):
    """Deletes a contact"""
    try:
        contact = Contact[contact_id]
    except ObjectNotFound:
        return empty(404)

    contact.delete()

    return empty(204)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8010, debug=is_debug, auto_reload=is_debug)
