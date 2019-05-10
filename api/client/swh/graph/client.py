# Copyright (C) 2019  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from swh.core.api import SWHRemoteAPI


class GraphAPIError(Exception):
    """Graph API Error"""
    def __str__(self):
        return ('An unexpected error occurred in the Graph backend: {}'
                .format(self.args))


class RemoteGraphClient(SWHRemoteAPI):
    """Client to the Software Heritage Graph."""

    def __init__(self, url, timeout=None):
        super().__init__(
            api_exception=GraphAPIError, url=url, timeout=timeout)

    # Web API endpoints

    def get_nb_nodes(self):
        return self.get('nb_nodes')