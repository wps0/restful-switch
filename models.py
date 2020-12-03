import time

from typing import List

from bson import ObjectId


class Voter:
    user_id: ObjectId
    create_date: int
    ip_addr: str
    conn_details: str

    def __init__(self, ip_addr: str, conn_details: str, user_id: ObjectId = ObjectId("000000000000000000000000"),
                 create_date: int = time.time()):
        """
            :arg user_id The id of the voting user. 0 - anonymous user
        """
        self.create_date = create_date
        self.ip_addr = ip_addr
        self.conn_details = conn_details
        self.user_id = user_id

    def __str__(self):
        from db import DOCUMENT_VOTER
        return DOCUMENT_VOTER \
            .replace("%user_id%", str(self.user_id)) \
            .replace("%create_date%", str(self.create_date)) \
            .replace("%ip_addr%", self.ip_addr) \
            .replace("%conn_details%", self.conn_details)


class Option:
    content: str

    def __init__(self, content: str):
        self.content = content

    def __str__(self):
        from db import DOCUMENT_VOTE_OPTION
        return DOCUMENT_VOTE_OPTION \
            .replace("%content%", self.content)


class Vote:
    poll_id: ObjectId
    content: int
    voter: Voter

    def __init__(self, poll_id: ObjectId, option_nr: int, voter: Voter):
        self.option_nr = option_nr
        self.poll_id = poll_id
        self.voter = voter

    def __str__(self):
        from db import DOCUMENT_VOTE
        return DOCUMENT_VOTE.replace("%poll_id%", str(self.poll_id)) \
            .replace("%option_nr%", str(self.option_nr)) \
            .replace("%voter%", str(self.voter))


class Poll:
    _id: ObjectId
    title: str
    desc: str
    publish_date: float
    create_date: float
    options: List[Vote]

    def __init__(self, title: str, publish_date: float, options: List[Vote], desc: str = "", create_date: float = time.time()):
        self.title = title
        self.desc = desc
        self.publish_date = publish_date
        self.create_date = create_date
        self.options = options

    def __str__(self):
        from db import DOCUMENT_POLL
        return DOCUMENT_POLL.replace("%title%", self.title) \
            .replace("%desc%", self.desc) \
            .replace("%publish_date%", str(self.publish_date)) \
            .replace("%create_date%", str(self.create_date)) \
            .replace("%options%", "[" + "".join((str(el) + "," for el in self.options)).rsplit(",", 1)[0] + "]")
