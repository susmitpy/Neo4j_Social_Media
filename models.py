from typing import Optional
from py2neo.ogm import Model, Property, RelatedFrom, RelatedTo
from rels import (
    FOLLOWS,
    CONTAINS_COMM,
    PART_OF_COMM,
    INTRESTED_IN,
    POSTED_TEXT_POST,
    TEXT_POST_POSTED,
    LIKED_TEXT_POST,
    SAVED_TEXT_POST,
    TAGGED_USER_IN_TEXT_POST,
    POSTED_IMAGE_POST,
    IMAGE_POST_POSTED,
    LIKED_IMAGE_POST,
    SAVED_IMAGE_POST,
    TAGGED_USER_IN_IMAGE_POST,
    POSTED_VIDEO,
    VIDEO_POSTED,
    LIKED_VIDEO,
    SAVED_VIDEO,
    TAGGED_USER_IN_VIDEO,
    COMMENTED_ON_TEXT_POST,
    COMMENTED_ON_IMAGE_POST,
    COMMENTED_ON_VIDEO,
    DISLIKED_VIDEO
)
from datetime import datetime, date

class Content(Model):
    """ Super class for TextPost, ImagePost and Video """

    # Indexes
    # CREATE INDEX ContentUUID FOR (c:Content) on (c.uuid)

class Post(Content):
    """ Super class for TextPost, ImagePost """

class User(Model):
    __primarykey__ = "uuid"

    # Indexes
    # CREATE INDEX UserUUID FOR (u:User) on (u.uuid)
    # CREATE INDEX UserUsername FOR (u:User) on (u.username)
    # CREATE INDEX UserMobile FOR (u:User) on (u.mobile)
    # CREATE INDEX UserEmail FOR (u:User) on (u.email)

    uuid: str = Property()

    username: str = Property()
    full_name: str = Property()
    bio: Optional[str] = Property()
    gender: Optional[str] = Property()
    email: Optional[str] = Property()
    date_of_birth: Optional[date] = Property()
    mobile: Optional[str] = Property()
    profile_pic_url: Optional[str] = Property()
    token: Optional[str] = Property()
    created_at: datetime = Property()
    updated_at: datetime = Property()
    verified: Optional[bool] = Property()
    is_staff: Optional[bool] = Property()
    is_superuser: Optional[bool] = Property()
    coins: int = Property()

    profile_views_counts: int = Property()

    followers_count: int = Property()
    following_count: int = Property()
    follows = RelatedTo("User", relationship_type=FOLLOWS.__name__)

    interests = RelatedTo("Interest", relationship_type=INTRESTED_IN.__name__)
    communities = RelatedTo("Community", relationship_type=PART_OF_COMM.__name__)

    text_posts = RelatedTo("Content:Post:TextPost", relationship_type=POSTED_TEXT_POST.__name__)
    text_posts_liked = RelatedTo("Content:Post:TextPost", relationship_type=LIKED_TEXT_POST.__name__)
    text_posts_saved = RelatedTo("Content:Post:TextPost", relationship_type=SAVED_TEXT_POST.__name__)

    image_posts = RelatedTo("Content:Post:ImagePost", relationship_type=POSTED_TEXT_POST.__name__)
    image_posts_liked = RelatedTo("Content:Post:ImagePost", relationship_type=LIKED_TEXT_POST.__name__)
    image_posts_saved = RelatedTo("Content:Post:ImagePost", relationship_type=SAVED_TEXT_POST.__name__)

    videos = RelatedTo("Content:Video", relationship_type=POSTED_VIDEO.__name__)
    videos_liked = RelatedTo("Content:Video", relationship_type=LIKED_VIDEO.__name__)
    videos_saved = RelatedTo("Content:Video", relationship_type=SAVED_VIDEO.__name__)
    videos_disliked = RelatedTo("Content:Video", relationship_type=DISLIKED_VIDEO.__name__)

    text_posts_comments = RelatedTo("Content:Post:TextPost", relationship_type=COMMENTED_ON_TEXT_POST.__name__)
    image_posts_comments = RelatedTo("Content:Post:ImagePost", relationship_type=COMMENTED_ON_IMAGE_POST.__name__)
    video_comments = RelatedTo("Content:Video", relationship_type=COMMENTED_ON_VIDEO.__name__)

    # No point in including reported users since everything has to be searched

    followed_by = RelatedFrom("User", relationship_type=FOLLOWS.__name__)
    posts_tagged_in = RelatedFrom("Content:Post", relationship_type=TAGGED_USER_IN_TEXT_POST.__name__)
    videos_tagged_in = RelatedFrom("Content:Video", relationship_type=TAGGED_USER_IN_VIDEO.__name__)


class Interest(Model):
    __primarykey__ = "uuid"
    # Indexes
    # CREATE INDEX InterestUUID FOR (i:Interest) on (i.uuid)

    # Constraints
    # CREATE CONSTRAINT ON (i:Interest) ASSERT i.name IS UNIQUE

    uuid: int = Property()
    name: str = Property()
    url: str = Property()

    communities = RelatedTo("Community", relationship_type=CONTAINS_COMM.__name__)

    interested_users = RelatedFrom("User", relationship_type=INTRESTED_IN.__name__)

class Community(Model):
    __primarykey__ = "uuid"

    # Indexes
    # CREATE INDEX CommunityUUID FOR (c:Community) on (c.uuid)

    # Constraints
    # CREATE CONSTRAINT ON (c:Community) ASSERT c.name IS UNIQUE

    uuid: int = Property()
    name: str = Property()
    url: str = Property()

    text_posts = RelatedTo("Post", relationship_type=TEXT_POST_POSTED.__name__)
    image_posts = RelatedTo("Post", relationship_type=IMAGE_POST_POSTED.__name__)
    videos = RelatedTo("Video", relationship_type=VIDEO_POSTED.__name__)
    

    interest = RelatedFrom("Interest", relationship_type=CONTAINS_COMM.__name__)
    users = RelatedFrom("User", relationship_type=PART_OF_COMM.__name__)


class TextPost(Post):
    __primarykey__ = "uuid"

    # Indexes
    # CREATE INDEX TextPostUUID FOR (tp:TextPost) on (tp.uuid)

    uuid: str = Property()
    caption: str = Property()
    location: str = Property()
    created_at: datetime = Property()
    is_safe: Optional[bool] = Property()
    likes_count: int = Property()
    comments_count: int = Property()
    saves_count: int = Property()
    views_count: int = Property()

    users_tagged = RelatedTo("User", relationship_type=TAGGED_USER_IN_TEXT_POST.__name__)

    posted_by = RelatedFrom("User", relationship_type=POSTED_TEXT_POST.__name__)
    posted_in = RelatedFrom("Community", relationship_type=TEXT_POST_POSTED.__name__)
    liked_by = RelatedFrom("User", relationship_type=LIKED_TEXT_POST.__name__)
    saved_by = RelatedFrom("User", relationship_type=SAVED_TEXT_POST.__name__)
    comments = RelatedFrom("User", relationship_type=COMMENTED_ON_TEXT_POST.__name__)

class ImagePost(Post):
    __primarykey__ = "uuid"

    # Indexes
    # CREATE INDEX ImagePostUUID FOR (ip:ImagePost) on (ip.uuid)

    uuid: str = Property()
    caption: str = Property()
    location: str = Property()
    blurhash: str = Property()
    url: str = Property()
    created_at: datetime = Property()
    aspect_ratio: float = Property()
    is_safe: Optional[bool] = Property()
    likes_count: int = Property()
    comments_count: int = Property()
    saves_count: int = Property()
    views_count: int = Property()

    users_tagged = RelatedTo("User", relationship_type=TAGGED_USER_IN_IMAGE_POST.__name__)

    posted_by = RelatedFrom("User", relationship_type=POSTED_IMAGE_POST.__name__)
    posted_in = RelatedFrom("Community", relationship_type=IMAGE_POST_POSTED.__name__)
    liked_by = RelatedFrom("User", relationship_type=LIKED_IMAGE_POST.__name__)
    saved_by = RelatedFrom("User", relationship_type=SAVED_IMAGE_POST.__name__)

    comments = RelatedFrom("User", relationship_type=COMMENTED_ON_TEXT_POST.__name__)

class Video(Content):
    __primarykey__ = "uuid"

    # Indexes
    # CREATE INDEX VideoUUID FOR (v:Video) on (v.uuid)

    uuid: str = Property()
    url: str = Property()
    title: str = Property()
    desc: str = Property()
    thumbnail: str = Property()
    location: str = Property()
    blurhash: str = Property()
    created_at: datetime = Property()
    likes_count: int = Property()
    comments_count: int = Property()
    dislikes_count: int = Property()
    saves_count: int = Property()
    views_count: int = Property()

    posted_by = RelatedFrom("User", relationship_type=POSTED_VIDEO.__name__)
    posted_in = RelatedFrom("Community", relationship_type=VIDEO_POSTED.__name__)
    liked_by = RelatedFrom("User", relationship_type=LIKED_VIDEO.__name__)
    saved_by = RelatedFrom("User", relationship_type=SAVED_VIDEO.__name__)
    disliked_by = RelatedTo("User", relationship_type=DISLIKED_VIDEO.__name__)

    comments = RelatedFrom("User", relationship_type=COMMENTED_ON_TEXT_POST.__name__)


