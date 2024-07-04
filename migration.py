import pandas as pd
from inf import Inf
from utils import PropertiesDict
from neo4j.time import DateTime

import asyncio
from utils import run_parallel, run_sequential
import pymysql
from time import time

HOST = ""
PORT = 3306
USER = ""
PASSWORD = ""
DATABASE = ""

mysql_cn= pymysql.connect(host=HOST, 
                port=PORT,user=USER, passwd=PASSWORD, 
                database=DATABASE,cursorclass=pymysql.cursors.DictCursor)
users = pd.read_sql('select * from users;', con=mysql_cn)    
rels = pd.read_sql('select * from user_relations;', con=mysql_cn)    
interests = pd.read_sql('select * from interests;', con=mysql_cn)    
comms = pd.read_sql('select * from communities;', con=mysql_cn)    
user_interests = pd.read_sql('select user_id,interest_id from user_interests;', con=mysql_cn)    
posts = pd.read_sql('select * from posts;', con=mysql_cn)    
post_likes = pd.read_sql('select post_id,user_id from likes;', con=mysql_cn)    
post_saves = pd.read_sql('select post_id,user_id from post_saved;', con=mysql_cn)    
post_user_tags = pd.read_sql('select post_id,user_id from user_post_tags;', con=mysql_cn)    
post_comments = pd.read_sql('select post_id,user_id from comments;', con=mysql_cn)    
videos = pd.read_sql('select * from video;', con=mysql_cn)    
video_saves = pd.read_sql('select video_id,user_id from video_saved;', con=mysql_cn)    
video_likes = pd.read_sql('select video_id,user_id from video_likes;', con=mysql_cn)    
video_dislikes = pd.read_sql('select video_id,user_id from video_dislikes;', con=mysql_cn)    
video_views = pd.read_sql('select video_id,user_id from video_views;', con=mysql_cn)    
video_comments = pd.read_sql('select video_id,user_id from video_comments;', con=mysql_cn)    
video_user_tags = pd.read_sql('select video_id,user_id from user_video_tags;', con=mysql_cn)   
 
inf = Inf()

mysql_cn.close()

async def create_users():
    def __create_user(user):
        return (
            f"""
            CREATE (u:User {user})
            """
        )

    print("Migrating Users")
    global users
    users["created_at"] = pd.to_datetime(
        users["created_at"], format="%Y-%m-%d %H:%M:%S"
    )
    users["updated_at"] = pd.to_datetime(
        users["updated_at"], format="%Y-%m-%d %H:%M:%S"
    )
    users["date_of_birth"] = pd.to_datetime(users["date_of_birth"], format="%d/%m/%y")

    users["verified"] = users["verified"].map({1: True, 0: None})
    users["is_staff"] = users["is_staff"].map({1: True, 0: None})
    users["is_superuser"] = users["is_superuser"].map({1: True, 0: None})

    users = users.drop(["coins"],axis=1)

    rels = pd.read_csv("./data/flyer_user_relations.csv")
    following_counts = rels.groupby("follower_id").size()
    followers_counts = rels.groupby("followee_id").size()

    views = pd.read_csv("./data/users_views.csv")
    profile_views_counts = views.groupby("profile_id").size()

    merged = pd.concat(
        [users.set_index("uuid"), following_counts, followers_counts, profile_views_counts], axis=1
    )
    merged = merged.reset_index()
    merged = merged.rename(
        columns={0: "following_count", 1: "followers_count",2:"profile_views_counts", "index": "uuid"}
    )

    merged["following_count"] = merged["following_count"].fillna(0).astype(int)
    merged["followers_count"] = merged["followers_count"].fillna(0).astype(int)
    merged["profile_views_counts"] = merged["profile_views_counts"].fillna(0).astype(int)

    # Only keep properties which are not nan
    data = [
        PropertiesDict({k: v for k, v in m.items() if pd.notnull(v)})
        for m in merged.to_dict(orient="records")
    ]


    with inf.driver.session() as session:
        tx = session.begin_transaction()

        for idx, user in enumerate(data):
            print(idx)
            tx.run(__create_user(user))
        tx.commit()

async def create_user_relations():
    def __create_user_relations( row):
        return(
            f"""
                MATCH (follower:User {{uuid: "{row['follower_id']}"}}), (followee:User {{uuid: "{row['followee_id']}"}})
                MERGE (follower) - 
                    [f:FOLLOWS
                        {{ts:apoc.date.parse('{str(DateTime.from_native(row['ts']))}', 's', "yyyy-MM-dd'T'HH:mm:ss")}}
                    ] -> (followee)
                """
        )

    print("Migrating user relations")

    rels["created_at"] = pd.to_datetime(rels["created_at"], format="%Y-%m-%d %H:%M:%S")
    rels.rename(columns={"created_at": "ts"}, inplace=True)

    with inf.driver.session() as session:
        tx = session.begin_transaction()
        for idx, row in rels.iterrows():
            print(idx)
            tx.run(__create_user_relations(row))
        tx.commit()

async def create_interests():
    def __create_interest( interest):
        return (
            f"""
            CREATE (i:Interest {interest})
            """
        )

    print("Migrating interests")

    global interests
    interests = interests.rename(
        columns={"interest_id": "uuid", "interest_name": "name", "interest_url": "url"}
    )

    data = [
        PropertiesDict({k: v for k, v in m.items() if pd.notnull(v)})
        for m in interests.to_dict(orient="records")
    ]

    with inf.driver.session() as session:
        tx = session.begin_transaction()
        for idx, interest in enumerate(data):
            print(idx)
            tx.run(__create_interest(interest))
        tx.commit()


async def create_comms():
    def __create_comm( comm):
        return(
            f"""
            CREATE (u:Community {comm})
            """
        )

    print("Migrating communities")

    df = comms.rename(columns={"comm_id": "uuid", "comm_name": "name", "comm_url": "url"})

    df = df[["uuid", "name", "url"]]

    data = [
        PropertiesDict({k: v for k, v in m.items() if pd.notnull(v)})
        for m in df.to_dict(orient="records")
    ]

    with inf.driver.session() as session:
        tx = session.begin_transaction()
        for idx, comm in enumerate(data):
            print(idx)
            tx.run(__create_comm(comm))
        tx.commit()


async def create_interest_comm_rel():
    def __create_interest_comm_rel( interest_id, comm_id):
        return(
            f"""
                    MATCH (i:Interest {{uuid: {interest_id}}})
                    MATCH (c:Community {{uuid: {comm_id}}})
                    MERGE (i) - [r:CONTAINS_COMM] -> (c)
                    """
        )

    print("Migrating interests and communities relations")

    df = comms[["comm_id", "comm_type"]]

    data = df.to_dict(orient="records")
    with inf.driver.session() as session:
        tx = session.begin_transaction()
        for idx, comm in enumerate(data):
            print(idx)
            tx.run(
                __create_interest_comm_rel(comm["comm_type"], comm["comm_id"])
            )
        tx.commit()


async def create_user_interest_comm_rel():
    def __create_user_interest_comm_rel( user_id, interest_id):
        # return(
        #     f"""
        #             MATCH (i:Interest {{uuid: {interest_id}}})
        #             MATCH (u:User {{uuid: '{user_id}'}})
        #             MERGE (u) - [rui:INTERESTED_IN] -> (i)
        #             """
        # )

        return(
            f"""
                    MATCH (i:Interest {{uuid: {interest_id}}})
                    MATCH (u:User {{uuid: '{user_id}'}})
                    MERGE (u) - [rui:INTERESTED_IN] -> (i)
                    WITH u, i
                    MATCH (c:Community) <- [ric:CONTAINS_COMM] - (i)
                    MERGE (u) - [ruc: PART_OF_COMM {{interest_uuid: {interest_id}}}] -> (c)
                    """
        )

    print("Migrating Users and interests, communities relations")

    
    global user_interests
    user_interests = user_interests[["user_id", "interest_id"]]

    data = user_interests.to_dict(orient="records")
    with inf.driver.session() as session:
        tx = session.begin_transaction()
        for idx, user_interest in enumerate(data):
            print(idx)
            tx.run(
                __create_user_interest_comm_rel(
                user_interest["user_id"],
                user_interest["interest_id"]
            ))
        tx.commit()


async def create_posts():
    def __create_text_post( post, user_id, comm_id):
        return(
            f"""
            CREATE (p:Content:Post:TextPost {post})
            WITH p
            MATCH (u:User {{uuid: '{user_id}'}})
            MERGE (u) - [upp: POSTED_TEXT_POST {{ts: apoc.date.parse('{str(DateTime.from_native(post['created_at']))}', 's', "yyyy-MM-dd'T'HH:mm:ss")}}] -> (p)
            WITH p
            MATCH (c:Community {{uuid: '{comm_id}'}})
            MERGE (c) - [ppc: TEXT_POST_POSTED {{ts: apoc.date.parse('{str(DateTime.from_native(post['created_at']))}', 's', "yyyy-MM-dd'T'HH:mm:ss")}}] -> (p)
            """
        ) 

    def __create_image_post( post, user_id, comm_id):
        return(
            f"""
            CREATE (p:Content:Post:ImagePost {post})
            WITH p
            MATCH (u:User {{uuid: '{user_id}'}})
            MERGE (u) - [upp: POSTED_IMAGE_POST {{ts: apoc.date.parse('{str(DateTime.from_native(post['created_at']))}', 's', "yyyy-MM-dd'T'HH:mm:ss")}}] -> (p)
            WITH p
            MATCH (c:Community {{uuid: '{comm_id}'}})
            MERGE (c) - [ppc: IMAGE_POST_POSTED {{ts: apoc.date.parse('{str(DateTime.from_native(post['created_at']))}', 's', "yyyy-MM-dd'T'HH:mm:ss")}}] -> (p)
            """
        )

    print("Migrating Posts")

    df = posts.rename(
        columns={
            "post_id": "uuid",
            "post_caption": "caption",
            "image_url": "url"
        }
    )

    df = df.drop(["post_created", "updated_at", "is_hidden", "likes_count", "comments_count"], axis=1)

    df["created_at"] = pd.to_datetime(df["created_at"], format="%Y-%m-%d %H:%M:%S")
    df["is_image"] = df["is_image"].map({1: True, 0: None})
    df["is_safe"] = df["is_safe"].map({1: True, 0: None})

    likes_count = post_likes.groupby("post_id").size()
    saves_count = post_saves.groupby("post_id").size()
    comments_count = post_comments.groupby("post_id").size()

    merged = pd.concat(
        [df.set_index("uuid"), saves_count, comments_count, likes_count], axis=1
    )
    merged = merged.reset_index()
    merged = merged.rename(
        columns={0: "saves_count", 1:"comments_count",2:"likes_count", "index": "uuid"}
    )

    merged["saves_count"] = merged["saves_count"].fillna(0).astype(int)
    merged["comments_count"] = merged["comments_count"].fillna(0).astype(int)
    merged["likes_count"] = merged["likes_count"].fillna(0).astype(int)

    

    data = merged.to_dict(orient="records")

    try:

        with inf.driver.session() as session:
            tx = session.begin_transaction()
            for idx, post in enumerate(data):
                print(idx)
                if post["is_image"]:
                    tx.run(
                        __create_image_post(PropertiesDict(
                        {
                            k: v
                            for k, v in post.items()
                            if k not in ["user_id", "comm_id"] and pd.notnull(v)
                        }
                    ), 
                    post["user_id"],
                    post["comm_id"]
                    ))
                else:
                    tx.run(
                        __create_text_post(PropertiesDict(
                        {
                            k: v
                            for k, v in post.items()
                            if k not in ["user_id", "comm_id", "blurhash", "url", "location", "aspect_ratio"] and pd.notnull(v)
                        }
                    ), 
                    post["user_id"],
                    post["comm_id"]
                    ))
            tx.commit()
    except Exception as e:
        print(e)


async def create_posts_likes():
    def __create_text_post_like( post_id, user_id):
        return(
            f"""
            MATCH (p:Content:Post:TextPost {{uuid: '{post_id}'}})
            MATCH (u:User {{uuid: '{user_id}'}})
            MERGE (u) - [l:LIKED_TEXT_POST] -> (p)
            """
        )

    def __create_image_post_like( post_id, user_id):
        return(
            f"""
            MATCH (p:Content:Post:ImagePost {{uuid: '{post_id}'}})
            MATCH (u:User {{uuid: '{user_id}'}})
            MERGE (u) - [l:LIKED_IMAGE_POST] -> (p)
            """
        )

    print("Migrating Posts Likes")

    merged = pd.merge(post_likes,posts[["post_id", "is_image"]],how="left",on=["post_id"])
    data = merged.to_dict(orient="records")

    with inf.driver.session() as session:
        tx = session.begin_transaction()
        for idx, post_like in enumerate(data):
            print(idx)
            if post_like["is_image"] == 1:
                tx.run(
                    __create_image_post_like(post_like["post_id"], post_like["user_id"])
                )
            else:
                tx.run(
                    __create_text_post_like(post_like["post_id"], post_like["user_id"])
                )
        tx.commit()

async def create_posts_saves():
    def __create_text_post_save( post_id, user_id):
        return(
            f"""
            MATCH (p:Content:Post:TextPost {{uuid: '{post_id}'}})
            MATCH (u:User {{uuid: '{user_id}'}})
            MERGE (u) - [l:SAVED_TEXT_POST] -> (p)
            """
        )

    def __create_image_post_save( post_id, user_id):
        return(
            f"""
            MATCH (p:Content:Post:ImagePost {{uuid: '{post_id}'}})
            MATCH (u:User {{uuid: '{user_id}'}})
            MERGE (u) - [l:SAVED_IMAGE_POST] -> (p)
            """
        )
    
    print("Migrating Posts Saves")

    merged = pd.merge(post_saves,posts[["post_id","is_image"]],how="left",on=["post_id"])
    data = merged.to_dict(orient="records")

    with inf.driver.session() as session:
        tx = session.begin_transaction()
        for idx, post_save in enumerate(data):
            print(idx)
            if post_save["is_image"] == 1:
                tx.run(
                    __create_image_post_save(post_save["post_id"], post_save["user_id"])
                )
            else:
                tx.run(
                    __create_text_post_save(post_save["post_id"], post_save["user_id"])
                )
        tx.commit()

async def create_posts_user_tags():
    def __create_text_post_user_tag( post_id, user_id):
        return(
            f"""
            MATCH (p:Content:Post:TextPost {{uuid: '{post_id}'}})
            MATCH (u:User {{uuid: '{user_id}'}})
            MERGE (p) - [put: TAGGED_USER_IN_TEXT_POST] -> (u)
            """
        )
    def __create_image_post_user_tag( post_id, user_id):
        return(
            f"""
            MATCH (p:Content:Post:ImagePost {{uuid: '{post_id}'}})
            MATCH (u:User {{uuid: '{user_id}'}})
            MERGE (p) - [put: TAGGED_USER_IN_TEXT_POST] -> (u)
            """
        )

    print("Migrating Posts User Tags")

    merged = pd.merge(post_user_tags,posts[["post_id","is_image"]],how="left",on=["post_id"])
    data = merged.to_dict(orient="records")

    with inf.driver.session() as session:
        tx = session.begin_transaction()
        for idx, post_user_tag in enumerate(data):
            print(idx)
            if post_user_tag["is_image"] == 1:
                tx.run(
                    __create_image_post_user_tag(
                    post_user_tag["post_id"],
                    post_user_tag["user_id"],
                ))
            else:
                tx.run(
                    __create_text_post_user_tag(
                    post_user_tag["post_id"],
                    post_user_tag["user_id"],
                ))
        tx.commit()

async def create_post_comments_edges():
    def __create_text_post_comment( post_id, user_id):
        return(
            f"""
            MATCH (p:Content:Post:TextPost {{uuid: '{post_id}'}})
            MATCH (u:User {{uuid: '{user_id}'}})
            MERGE (u) - [l:COMMENTED_ON_TEXT_POST] -> (p)
            """
        )

    def __create_image_post_comment( post_id, user_id):
        return(
            f"""
            MATCH (p:Content:Post:ImagePost {{uuid: '{post_id}'}})
            MATCH (u:User {{uuid: '{user_id}'}})
            MERGE (u) - [l:COMMENTED_ON_IMAGE_POST] -> (p)
            """
        )

    print("Migrating posts comments edges")

    merged = pd.merge(post_comments,posts[["post_id","is_image"]],how="left",on=["post_id"])
    data = merged.to_dict(orient="records")

    with inf.driver.session() as session:
        tx = session.begin_transaction()
        for idx, post_comment in enumerate(data):
            print(idx)
            if post_comment["is_image"] == 1:
                tx.run(
                    __create_image_post_comment(post_comment["post_id"], post_comment["user_id"])
                )
            else:
                tx.run(
                    __create_text_post_comment(post_comment["post_id"], post_comment["user_id"])
                )
        tx.commit()

async def create_videos():
    def __create_video( video, user_id, comm_id):
        return(
            f"""
            CREATE (v:Content:Video {video})
            WITH v
            MATCH (u:User {{uuid: '{user_id}'}})
            MERGE (u) - [upv: POSTED_VIDEO {{ts: apoc.date.parse('{str(DateTime.from_native(video['created_at']))}', 's', "yyyy-MM-dd'T'HH:mm:ss")}}] -> (v)
            WITH v
            MATCH (c:Community {{uuid: '{comm_id}'}})
            MERGE (c) - [vpc: VIDEO_POSTED {{ts: apoc.date.parse('{str(DateTime.from_native(video['created_at']))}', 's', "yyyy-MM-dd'T'HH:mm:ss")}}] -> (v)
            """
        ) 

    print("Migrating Videos")
    
    videos["created_at"] = pd.to_datetime(videos["created_at"], format="%Y-%m-%d %H:%M:%S")
    df = videos.rename(columns={
        "video_id": "uuid",
        "video_url": "url",
        "video_title": "title",
        "video_desc": "desc"
    })

    df = df.drop(columns=["video_created", "updated_at", "is_hidden", "orientation", "is_landscape", "likes_count", "comments_count", "dislikes_count"], axis=1)

    saves_count = video_saves.groupby("video_id").size()
    likes_count = video_likes.groupby("video_id").size()
    dislikes_count = video_dislikes.groupby("video_id").size()
    views_count = video_views.groupby("video_id").size()
    comments_count = video_comments.groupby("video_id").size()

    merged = pd.concat(
        [df.set_index("uuid"), saves_count, views_count, comments_count, likes_count, dislikes_count], axis=1
    )
    merged = merged.reset_index()
    merged = merged.rename(
        columns={0: "saves_count", 1: "views_count", 2:"comments_count",3:"likes_count",4:"dislikes_count", "index": "uuid"}
    )

    merged["saves_count"] = merged["saves_count"].fillna(0).astype(int)
    merged["views_count"] = merged["views_count"].fillna(0).astype(int)
    merged["comments_count"] = merged["comments_count"].fillna(0).astype(int)
    merged["likes_count"] = merged["likes_count"].fillna(0).astype(int)
    merged["dislikes_count"] = merged["dislikes_count"].fillna(0).astype(int)

    

    data = merged.to_dict(orient="records")

    try:

        with inf.driver.session() as session:
            tx = session.begin_transaction()
            for idx, video in enumerate(data):
                print(idx)

                tx.run(
                    __create_video(PropertiesDict(
                    {
                        k: v
                        for k, v in video.items()
                        if k not in ["user_id", "comm_id"] and pd.notnull(v)
                    }
                ), 
                video["user_id"],
                video["comm_id"]
                ))
            tx.commit()

    except Exception as e:
        print(e)

async def create_video_likes():
    def __create_video_like( video_id, user_id):
        return(
            f"""
            MATCH (v:Content:Video {{uuid: '{video_id}'}})
            MATCH (u:User {{uuid: '{user_id}'}})
            MERGE (u) - [l:LIKED_VIDEO] -> (v)
            """
        )

    print("Migrating Videos likes")

    data = video_likes.to_dict(orient="records")

    with inf.driver.session() as session:
        tx = session.begin_transaction()
        for idx, video_like in enumerate(data):
            print(idx)

            tx.run(
                __create_video_like(video_like["video_id"], video_like["user_id"])
            )
        tx.commit()

async def create_video_user_tags():
    def __create_video_user_tag( video_id, user_id):
        return(
            f"""
            MATCH (v:Content:Video {{uuid: '{video_id}'}})
            MATCH (u:User {{uuid: '{user_id}'}})
            MERGE (u) - [l:TAGGED_USER_IN_VIDEO] -> (v)
            """
        )

    print("Migrating Videos user tags")

    data = video_user_tags.to_dict(orient="records")

    with inf.driver.session() as session:
        tx = session.begin_transaction()
        for idx, video_like in enumerate(data):
            print(idx)

            tx.run(
                __create_video_user_tag(video_like["video_id"], video_like["user_id"])
            )
        tx.commit()


async def create_video_saves():
    def __create_video_save( video_id, user_id):
        return(
            f"""
            MATCH (v:Content:Video {{uuid: '{video_id}'}})
            MATCH (u:User {{uuid: '{user_id}'}})
            MERGE (u) - [l:SAVED_VIDEO] -> (v)
            """
        )

    print("Migrating Videos saves")

    data = video_saves.to_dict(orient="records")

    with inf.driver.session() as session:
        tx = session.begin_transaction()
        for idx, video_like in enumerate(data):
            print(idx)

            tx.run(
                __create_video_save(video_like["video_id"], video_like["user_id"])
            )
        tx.commit()

async def create_video_dislikes():
    def __create_video_dislike( video_id, user_id):
        return(
            f"""
            MATCH (v:Content:Video {{uuid: '{video_id}'}})
            MATCH (u:User {{uuid: '{user_id}'}})
            MERGE (u) - [l:DISLIKED_VIDEO] -> (v)
            """
        )

    print("Migrating Videos dislikes")
    data = video_dislikes.to_dict(orient="records")

    with inf.driver.session() as session:
        tx = session.begin_transaction()
        for idx, video_like in enumerate(data):
            print(idx)

            tx.run(
                __create_video_dislike(video_like["video_id"], video_like["user_id"])
            )
        tx.commit()

async def create_video_comments_edges():
    def __create_video_comment( post_id, user_id):
        return(
            f"""
            MATCH (v:Content:Video{{uuid: '{post_id}'}})
            MATCH (u:User {{uuid: '{user_id}'}})
            MERGE (u) - [l:COMMENTED_ON_VIDEO] -> (v)
            """
        )

    print("Migrating video comments edges")
    data = video_comments.to_dict(orient="records")

    with inf.driver.session() as session:
        tx = session.begin_transaction()
        for idx, video_comment in enumerate(data):
            print(idx)
            tx.run(
                    __create_video_comment(video_comment["video_id"], video_comment["user_id"])
            )
        tx.commit()

async def main():
    await run_sequential(
        run_parallel(
            create_users(),
            create_interests(),
            create_comms()
        ),
        create_interest_comm_rel(),
        create_user_interest_comm_rel(),
        run_parallel(
            create_user_relations(),
            run_sequential(
                create_posts(),
                run_parallel(
                    create_posts_likes(),
                    create_posts_saves(),
                    create_posts_user_tags(),
                    create_post_comments_edges()
                )
            ),
            run_sequential(
                create_videos(),
                run_parallel(
                    create_video_likes(),
                    create_video_saves(),
                    create_video_dislikes(),
                    create_video_comments_edges(),
                    create_video_user_tags()
                )
            )
        )
    )

start = time()
asyncio.run(main())
end = time()

print(f"Time taken: str({(end - start)/60}) minutes")

inf.driver.close()