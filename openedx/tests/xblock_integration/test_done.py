"""
This tests that the completion XBlock correctly stores state. This
is a fairly simple XBlock, and a correspondingly simple test suite.
"""

import json
import unittest

from django.conf import settings
from django.core.urlresolvers import reverse

from xmodule.modulestore.tests.factories import CourseFactory, ItemFactory
from xmodule.modulestore.tests.django_utils import SharedModuleStoreTestCase

from lms.djangoapps.courseware.tests.helpers import LoginEnrollmentTestCase
from lms.djangoapps.courseware.tests.factories import GlobalStaffFactory
from lms.djangoapps.lms_xblock.runtime import quote_slashes


class TestDone(SharedModuleStoreTestCase, LoginEnrollmentTestCase):
    """
    Simple tests for the completion XBlock. We set up a page with two
    of the block, make sure the page renders, toggle them a few times,
    make sure they've toggled, and reconfirm the page renders.
    """
    STUDENTS = [
        {'email': 'view@test.com', 'password': 'foo'},
        {'email': 'view2@test.com', 'password': 'foo'}
    ]

    @classmethod
    def setUpClass(cls):
        """
        Create a page with two of the XBlock on it
        """
        # Nose runs setUpClass methods even if a class decorator says to skip
        # the class: https://github.com/nose-devs/nose/issues/946
        # So, skip the test class here if we are not in the LMS.
        if settings.ROOT_URLCONF != 'lms.urls':
            raise unittest.SkipTest('Test only valid in lms')

        super(TestDone, cls).setUpClass()
        cls.course = CourseFactory.create(
            display_name='Done_Test_Course'
        )
        with cls.store.bulk_operations(cls.course.id, emit_signals=False):
            cls.chapter = ItemFactory.create(
                parent=cls.course, display_name='Overview'
            )
            cls.section = ItemFactory.create(
                parent=cls.chapter, display_name='Welcome'
            )
            cls.unit = ItemFactory.create(
                parent=cls.section, display_name='New Unit'
            )
            cls.xblock1 = ItemFactory.create(
                parent=cls.unit,
                category='done',
                display_name='done_0'
            )
            cls.xblock2 = ItemFactory.create(
                parent=cls.unit,
                category='done',
                display_name='done_1'
            )

        cls.course_url = reverse(
            'courseware_section',
            kwargs={
                'course_id': cls.course.id.to_deprecated_string(),
                'chapter': 'Overview',
                'section': 'Welcome',
            }
        )

    def setUp(self):
        """
        Create users
        """
        super(TestDone, self).setUp()
        for idx, student in enumerate(self.STUDENTS):
            username = "u{}".format(idx)
            self.create_account(username, student['email'], student['password'])
            self.activate_user(student['email'])

        self.staff_user = GlobalStaffFactory()

    def get_handler_url(self, handler, xblock_name=None):
        """
        Get url for the specified xblock handler
        """
        return reverse('xblock_handler', kwargs={
            'course_id': self.course.id.to_deprecated_string(),
            'usage_id': quote_slashes(self.course.id.make_usage_key('done', xblock_name).to_deprecated_string()),
            'handler': handler,
            'suffix': ''
        })

    def enroll_student(self, email, password):
        """
        Student login and enroll for the course
        """
        self.login(email, password)
        self.enroll(self.course, verify=True)

    def check_ajax(self, block, data, desired_state):
        """
        Make an AJAX call to the XBlock, and assert the state is as
        desired.
        """
        url = self.get_handler_url('toggle_button', 'done_' + str(block))
        resp = self.client.post(url, json.dumps(data), '')
        resp_data = json.loads(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_data, {"state": desired_state})
        return resp_data

    def test_done(self):
        """
        Walk through a few toggles. Make sure the blocks don't mix up
        state between them, initial state is correct, and final state
        is correct.
        """
        self.enroll_student(self.STUDENTS[0]['email'], self.STUDENTS[0]['password'])
        # We confirm we don't have errors rendering the student view
        self.assert_request_status_code(200, self.course_url)
        # We confirm the block is initially false
        self.check_ajax(0, {}, False)
        self.check_ajax(1, {}, False)
        # We confirm we can toggle state both ways
        self.check_ajax(0, {'done': True}, True)
        self.check_ajax(1, {'done': False}, False)
        self.check_ajax(0, {'done': False}, False)
        self.check_ajax(1, {'done': True}, True)
        # We confirm state sticks around
        self.check_ajax(0, {}, False)
        self.check_ajax(1, {}, True)
        # We reconfirm we don't have errors rendering the student view
        self.assert_request_status_code(200, self.course_url)
