# -*- coding: utf-8 -*-
from genologics.lims import Lims as LimsBase
from genologics.config import BASEURI, USERNAME, PASSWORD


class Lims(LimsBase):
    def __init__(self):
        """Postpone connection to server."""
        pass

    def init_app(self, app):
        """Initialize database connection from app object."""
        super(Lims, self).__init__(BASEURI, USERNAME, PASSWORD)
        self.check_version()


lims = Lims()
