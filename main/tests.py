from django.test import TestCase
from myapp.models import Animal


# class AnimalTestCase(TestCase):
#     def setUp(self):
#         Animal.objects.create(name="lion", sound="roar")
#         Animal.objects.create(name="cat", sound="meow")

#     def test_animals_can_speak(self):
#         """Animals that can speak are correctly identified"""
#         lion = Animal.objects.get(name="lion")
#         cat = Animal.objects.get(name="cat")
#         self.assertEqual(lion.speak(), 'The lion says "roar"')
#         self.assertEqual(cat.speak(), 'The cat says "meow"')


class MovieTestCase(TestCase):

    def setUp(self):
        pass

    # Any person can add a movie
    def test_movie_submission(self):
        pass

    # When a movie is added, a truncated title is automatically created for it
    def test_truncated_title_creation(self):
        pass

    # An authenticated user can vote for a movie
    # An anonymous user can't vote for a movie
    def test_movie_voting(self):
        pass


class GroupTestCase(TestCase):

    def setUp(self):
        pass

    # An authenticated user can create a group
    # An anonymous user can't create a group
    def test_group_creation(self):
        pass

    # An authenticated user can join a group
    # An anonymous user can't join a group
    def test_group_joining(self):
        pass

    # All of the movies that members of a groups have voted for
    #   are shown in the group
    def test_group_movie_list(self):
        pass

    # Only the votes for movies of members of a group are counted within the
    #   group
    def test_group_vote_count(self):
        pass


class EventTestCase(TestCase):

    def setUp(self):
        pass

    # An event must be associated with a group
    def test_event_group_parent(self):
        pass

    # An authenticated user can create an event
    # An anonymous user can't create an event
    def test_event_creation(self):
        pass

    # event IS_ACTIVE attribute can be toggled by the creator
    # event IS_ACTIVE attribute can't be toggled by other users
    def test_event_creator_toggle_active(self):
        pass

    # event IS_ACTIVE attribute = True - Users can join the event
    # event IS_ACTIVE attribute = False - Users can't join the event
    def test_event_active_join(self):
        pass

    # An authenticated group member can join an event
    # An authenticated non group member can join an event
    # An anonymous user can't join an event
    def test_event_join(self):
        pass

    # Only the votes for the people who have joined the event are
    #   counted for the movies in an event
    def test_event_vote_count(self):
        pass

    # Only the event creator can lock in or remove a movie from an event
    # Non-event creators can't lock in or remove a movie from an event
    def test_event_creator_lockin(self):
        pass

    # When an event creator locks in a movie, a movie viewing is assigned to
    #   the members of that event
    def test_event_lockin_creates_views(self):
        pass

    # When a user joins an event, a movie viewing is assigned to them for every
    # movie already locked in to that event
    def test_event_join_creates_views(self):
        pass
