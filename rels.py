from py2neo.data import Relationship
from py2neo.ogm import Property


class FOLLOWS(Relationship):
    """User follows User"""

    # Indexes
    # CREATE INDEX FollowsTS FOR () - [f:FOLLOWS] -> () on (f.ts) (used for pagination)

    ts = Property()


class CONTAINS_COMM(Relationship):
    """Interest contains Community"""


class INTRESTED_IN(Relationship):
    """User is interested in an Interest"""


class PART_OF_COMM(Relationship):
    """User is part of Community"""

    interest_uuid = Property()  # UUID of the interest, needed for unfollow interest


class POSTED_TEXT_POST(Relationship):
    """A user can post a text post"""

    ts = Property()


class TEXT_POST_POSTED(Relationship):
    """
    A text post is posted in a community
    """

    ts = Property()


class LIKED_TEXT_POST(Relationship):
    """A user can like a text post"""


class SAVED_TEXT_POST(Relationship):
    """A user can save a text post"""

class TAGGED_USER_IN_TEXT_POST(Relationship):
    """A user can tag a user in a text post"""

class COMMENTED_ON_TEXT_POST(Relationship):
    """A user can comment on a text post"""

class POSTED_IMAGE_POST(Relationship):
    """A user can post a IMAGE post"""

    ts = Property()


class IMAGE_POST_POSTED(Relationship):
    """
    A IMAGE post is posted in a community
    """

    ts = Property()


class LIKED_IMAGE_POST(Relationship):
    """A user can like a IMAGE post"""


class SAVED_IMAGE_POST(Relationship):
    """A user can save a IMAGE post"""

class TAGGED_USER_IN_IMAGE_POST(Relationship):
    """A user can tag a user in a IMAGE post"""

class COMMENTED_ON_IMAGE_POST(Relationship):
    """A user can comment on a IMAGE post"""

class POSTED_VIDEO(Relationship):
    """A user can post a IMAGE post"""

    ts = Property()


class VIDEO_POSTED(Relationship):
    """
    A IMAGE post is posted in a community
    """

    ts = Property()


class LIKED_VIDEO(Relationship):
    """A user can like a IMAGE post"""


class SAVED_VIDEO(Relationship):
    """A user can save a IMAGE post"""

class TAGGED_USER_IN_VIDEO(Relationship):
    """A user can tag a user in a IMAGE post"""

class COMMENTED_ON_VIDEO(Relationship):
    """A user can comment on a video"""

class DISLIKED_VIDEO(Relationship):
    """A user can dislike a video"""