import time

from typing import List
from bson import ObjectId


class UserInteraction:
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
        from db import DOCUMENT_USER_INTERACTION
        return DOCUMENT_USER_INTERACTION \
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
    voter: UserInteraction

    def __init__(self, poll_id: ObjectId, option_nr: int, voter: UserInteraction):
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
    options: List[Option]

    def __init__(self, title: str, publish_date: float, options: List[Option], desc: str = "",
                 create_date: float = time.time()):
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


class File:
    file_path: str
    hash: str
    uploader: UserInteraction
    create_date: int

    def __init__(self, file_path: str, uploader: UserInteraction, h: str, create_date: int = time.time()):
        self.file_path = file_path
        self.hash = h
        self.uploader = uploader
        self.create_date = create_date

    def __str__(self):
        from db import DOCUMENT_FILE
        return DOCUMENT_FILE\
            .replace("%create_date%", str(self.create_date)) \
            .replace("%file_path%", self.file_path) \
            .replace("%hash%", self.hash) \
            .replace("%uploader%", str(self.uploader))
