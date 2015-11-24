"""
Mobile API views for badges
"""
from edxval.views import MultipleFieldLookupMixin
from opaque_keys.edx.keys import CourseKey
from rest_framework import generics

from badges.models import BadgeClass, BadgeAssertion
from mobile_api.badges.serializers import BadgeClassSerializer, BadgeAssertionSerializer
from mobile_api.utils import mobile_view
from xmodule_django.models import CourseKeyField


@mobile_view()
class BadgeClassDetail(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    """
    Get the details of a specific badge class.
    """
    serializer_class = BadgeClassSerializer
    lookup_fields = ('issuing_component', 'slug')

    def get_queryset(self):
        provided_id = self.kwargs.get('course_id')
        if provided_id:
            course_id = CourseKey.from_string(provided_id)
        else:
            course_id = CourseKeyField.Empty
        return BadgeClass.objects.filter(
            course_id=course_id,
        )


@mobile_view(is_user=True)
class UserBadgeAssertions(generics.ListAPIView):
    """
    Get all badge assertions for a user, optionally constrained to a course.
    """
    serializer_class = BadgeAssertionSerializer

    def get_queryset(self):
        """
        Get all badges for the username specified.
        """
        queryset = BadgeAssertion.objects.filter(user__username=self.kwargs['username'])
        provided_course_id = self.kwargs.get('course_id')
        if provided_course_id == '*':
            # We might want to get all the matching course scoped badges to see how many courses
            # a user managed to get a specific award on.
            course_id = None
        elif provided_course_id:
            course_id = CourseKey.from_string(provided_course_id)
        elif 'slug' not in self.kwargs:
            # Need to get all badges for the user.
            course_id = None
        else:
            course_id = CourseKeyField.Empty

        if course_id is not None:
            queryset = queryset.filter(badge_class__course_id=course_id)
        if self.kwargs.get('slug'):
            queryset = queryset.filter(
                badge_class__slug=self.kwargs['slug'],
                badge_class__issuing_component=self.kwargs.get('issuing_component', '')
            )
        return queryset
