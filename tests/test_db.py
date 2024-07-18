import unittest
from peewee import *

from app import TimelinePost

MODELS = [TimelinePost]

#use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)
    
    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_timeline_post(self):
        first_post = TimelinePost.create(name='Jon Doe', email='john@example.com', content='Hello world, I\'m John')
        assert first_post.id == 1
        first_post_created_time = first_post.created_at
        second_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content='Hello world, I\'m Jane')
        assert second_post.id == 2
        second_post_created_time = second_post.created_at

        #TODO: Get timeline posts and assert that they are correct
        retreived_first_post = TimelinePost.get_by_id(1)
        retreived_second_post = TimelinePost.get_by_id(2)

        assert retreived_first_post.name == 'Jon Doe'
        assert retreived_first_post.email == 'john@example.com'
        assert retreived_first_post.content == 'Hello world, I\'m John'
        assert retreived_first_post.created_at == first_post_created_time

        assert retreived_second_post.name == 'Jane Doe'
        assert retreived_second_post.email == 'jane@example.com'
        assert retreived_second_post.content == 'Hello world, I\'m Jane'
        assert retreived_second_post.created_at == second_post_created_time