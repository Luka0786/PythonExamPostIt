from django.test import TestCase
from .models import PostModel, CommentModel, DraftModel
from django.contrib.auth.models import User
# Create your tests here.

class PostTestCase(TestCase):
    def setUp(self):
    
        #User
        User.objects.create(username="testUser", email="testEmail", first_name="testFirst", last_name="testLast", password="testPass1")
        User.objects.create(username="testUser2", email="testEmail2", first_name="testFirst2", last_name="testLast2", password="testPass2")
        user = User.objects.get(username="testUser")

        #Comment
        CommentModel.objects.create(user=user,body="testCommentBody")
        CommentModel.objects.create(user=user,body="testCommentBody22")

        #Post
        PostModel.objects.create(user=user, title="testPost", body="ThisIsATest")

        #Draft
        DraftModel.objects.create(user=user, title="testDraft", body="ThisIsATestDraft")

    def test_if_post_was_created_successfully(self):
        #Get Post,User,Comment,Draft
        test_post = PostModel.objects.get(title="testPost")
        test_user = User.objects.filter(username="testUser")
        test_user2 = User.objects.get(username="testUser2")
        test_draft = DraftModel.objects.get(title="testDraft")
        test_post.comments.set(CommentModel.objects.filter(pk=1))

        #Testing
        self.assertEqual(str(test_post),test_post.title)
        self.assertEqual(test_post.body, "ThisIsATest")
        self.assertEqual(test_post.comments.get(pk=1).body, "testCommentBody")

        #Setting Comments
        test_post.comments.set(CommentModel.objects.filter(pk=2))

        #Testing
        self.assertEqual(test_post.comments.get(pk=2).body, "testCommentBody22")
        self.assertNotEqual(test_post.user, test_user2)
        self.assertEqual(test_draft.body, "ThisIsATestDraft")
        test_post.save()

    




class TestViewUrls(TestCase):
    def setUp(self):
        #Some urls needs a user to be logged in otherwise we cant access them
        self.user = User.objects.create(username="testUserName")
        self.user.set_password("testPassword")
        self.user.save()
        self.client.force_login(self.user)

        
    def test_view_url_exists_at_location_home(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_location_posts(self):

        

        response = self.client.get('/posts')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_location_posts_create(self):

        

        response = self.client.get('/posts/create')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_location_posts_yours(self):

        response = self.client.get("/posts/yours")
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_location_posts_pk(self):

        response = self.client.get('/posts/1')

        #No post has been created so we expect a 404
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_location_post_comment(self):

        response = self.client.get('/post/comment')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_location_posts_drafts(self):

        response = self.client.get('/posts/drafts')
        self.assertEqual(response.status_code, 200)
