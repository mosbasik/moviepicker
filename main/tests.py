from django.test import TestCase

# Events model tests

# Feature - IS_ACTIVE
# When an event is active, users can join,
# Lockins can be created, Viewings can be assigned

# When an event is NOT active, users cannot join,
# Lockins can't be created, Viewings can't be assigned

# Only the event creator can toggle IS_ACTIVE


# TESTS

# IS_ACTIVE can be toggled by the creator

# IS_ACTIVE can't be toggled by other users

# IS_ACTIVE = True - Users can join the event

# IS_ACTIVE = False - Users can't join the event

# Any person can add a movie

# When a movie is added, a truncated title is automatically created for it

# An authenticated user can vote for a movie

# An anonymous user can't vote for a movie

# An authenticated user can create a group

# An anonymous user can't create a group

# An authenticated user can join a group

# An anonymous user can't join a group

# All of the movies that members of a groups have voted for
# are shown in the group

# Only the votes for movies of members of a group are counted within the group

# An authenticated user can create an event

# An anonymous user can't create an event

# An event must be associated with a group

# An authenticated user can join an event

# An anonymous user can't join an event

# Only the votes for the people who have joined the event are
# counted for the movies in an event

# Only the event creator can lock in a movie

# Non-event creators can't lockin a movie

# When an event creator locks in a movie, a movie viewing is assigned to
# the members of that event

# A lockin 
