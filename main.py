import os
import uuid

from sanic import Sanic
from sanic.response import json, empty
from pony.orm import *
from dotenv import load_dotenv

# configuration --------------
load_dotenv()

# DB_LOCATION=contacts.db
# ENVIRONMENT=development
environment = os.getenv("ENVIRONMENT")
db_location = os.getenv("DB_LOCATION")

# database --------------
if environment != 'production':
    set_sql_debug(True)

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
        try:
            contact_payload = request.json
        except:
            raise ValueError
        if contact_payload is None:
            raise ValueError

        id = str(uuid.uuid4())

        Contact(id=id, firstName=contact_payload['firstName'], lastName=contact_payload['lastName'],
                phoneNumber=contact_payload['phoneNumber'])

        return empty(201, {'Location': f"/{id}"})
    except ValueError:
        return empty(400)


@app.get('/contacts/')
@db_session
def get_all_contacts(_):
    """Gets all contacts"""
    contacts_payload = []

    contacts = select(c for c in Contact)
    for c in contacts:
        contacts_payload.append(c.to_dict())

    return json(contacts_payload)


@app.get('/contacts/<id>')
@db_session
def get_contact(_, id):
    """Gets a specific contact"""
    try:
        contact = Contact[id]
    except ObjectNotFound:
        return empty(404)

    return json(contact.to_dict())


@app.put('/contacts/<id>')
@db_session
def update_contact(request, id):
    """Updates a contact"""
    try:
        contact = Contact[id]
    except ObjectNotFound:
        return empty(404)

    try:
        try:
            contact_payload = request.json
        except:
            raise ValueError
        if contact_payload is None:
            raise ValueError

        contact.firstName = contact_payload['firstName']
        contact.lastName = contact_payload['lastName']
        contact.phoneNumber = contact_payload['phoneNumber']

        return empty(204)
    except ValueError:
        return empty(400)


@app.delete('/contacts/<id>')
@db_session
def delete_contact(_, id):
    """Deletes a contact"""
    try:
        contact = Contact[id]
    except ObjectNotFound:
        return empty(404)

    contact.delete()

    return empty(204)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8010)
