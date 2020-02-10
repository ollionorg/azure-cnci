import unittest

import azure.functions as func
from . import build_listener

class TestBuildListenerPositive(unittest.TestCase):

    def test_build_in_progress_listener(self):
        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/build_listener', 
            params={'name': 'Test'})

        # Call the function.
        resp = build_listener(req)

        # Check the output.
        self.assertEqual(
            resp.get_body(), 
            'Event successfully served!!',
        )