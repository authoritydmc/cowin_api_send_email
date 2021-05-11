import json


class State():
    def __init__(self, name, id):
        self.name = name
        self.id = id


class sessionsVaccine():

    def __init__(self, sid, cid, min_age, available, slots, date, vaccine_name):
        self.session_id = sid
        self.center_id = cid
        self.min_age = min_age
        self.available = available
        self.slots = slots
        self.date = date
        self.vaccine_name = vaccine_name

    def __repr__(self):
        return "{} has {} {} vaccine for {} ondate {} ".format(self.session_id, self.available, self.vaccine_name, self.min_age, self.date)


class Center():
    def __init__(self, cid, cname, caddr, cpin, fee, block_name):

        self.center_name = cname
        self.center_id = cid
        self.address = caddr
        self.pincode = cpin
        self.fee = fee
        self.block_name = block_name
