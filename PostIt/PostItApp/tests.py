from django.test import TestCase, Client
from .models import PostModel, CommentModel, DraftModel
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core import mail
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

class TestHTTPMethods(TestCase):
    def setUp(self):
        #Client
        self.client = Client()

        #User and login with the user
        self.user = User.objects.create(username="testUserName")
        self.user.set_password("testPassword")
        self.user.save()
        self.client.force_login(self.user)

        #Create user and a post with a comment
        User.objects.create(username="testUser", email="vmanpro2008@live.dk", first_name="testFirst", last_name="testLast", password="testPass1")
        user = User.objects.get(username="testUser")

        PostModel.objects.create(user=user, title="testPost", body="ThisIsATest")
        CommentModel.objects.create(user=user,body="testCommentBody")
        DraftModel.objects.create(user=user, title="testDraft", body="ThisIsATestDraft")

        self.test_draft = DraftModel.objects.get(title="testDraft")
        self.test_comment = CommentModel.objects.get(body="testCommentBody")
        self.test_post = PostModel.objects.get(title="testPost")
        self.test_post.comments.set(CommentModel.objects.filter(pk=1))
        self.test_post.save()

        self.long_title_30 = "THISTITLEISLONGLONGLONGLONGLONGLONGLONGLONG"
        self.long_body_1000 = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. N asd ds e a g hdfd s"
    
    def test_view_http_bad_request(self):
        response = self.client.post('/posts')
        #Testing bad request (400)
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/posts/yours')
        #Testing bad request (400)
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/posts/1')
        #Testing bad request (400)
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/posts/drafts')
        #Testing bad request (400)
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/posts/drafts')
        #Testing bad request (400)
        self.assertEqual(response.status_code, 400)

        response = self.client.put('/posts/create')
        #Testing bad request (400)
        self.assertEqual(response.status_code, 400)

        response = self.client.put('/posts/draft/1')
        #Testing bad request (400)
        self.assertEqual(response.status_code, 400)

        response = self.client.put('/post/comment')
        #Testing bad request (400)
        self.assertEqual(response.status_code, 400)

    def test_view_http_get_request(self):
        #<int:pk>
        response = self.client.get('/posts/1')
        #Testing get request (200)
        self.assertEqual(response.status_code, 200)

        #<int:pk>
        response = self.client.get('/posts/draft/1')
        #Testing get request (200)
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/post/comment')
        #Testing get request (200)
        self.assertEqual(response.status_code, 200)

    def test_view_send_mail_to_user(self):
        send_mail(
            'Someone commented on your post',
            'Your post ' + self.test_post.title + ' got a new comment! ' + 'User ' + self.test_comment.user.username + ' commented on your post!',
            'postitpython@gmail.com',
            [self.test_post.user.email],
            fail_silently=False,
        )
        self.assertEqual(mail.outbox[0].body, "Your post testPost got a new comment! User testUser commented on your post!")

    def test_view_http_post_request(self):
        #Creating a new post        
        response = self.client.post('/posts/create', {'post_submit':'post_submit', 'user':self.test_post.user, 'title': 'createdPostTest', 'body': self.test_post.body})

        #Checking if the post has been created in the database
        self.created_test_post = PostModel.objects.get(title="createdPostTest")
        self.assertEqual(self.created_test_post.title, "createdPostTest")

        #Creating a new draft     
        response = self.client.post('/posts/create', {'draft_submit':'draft_submit', 'user':self.test_post.user, 'title': 'createdDraftTest', 'body': self.test_post.body})

        #Checking if the draft has been created in the database
        self.created_test_draft = DraftModel.objects.get(title="createdDraftTest")
        self.assertEqual(self.created_test_draft.title, "createdDraftTest")

        #Publishing a draft
        response = self.client.post('/posts/draft/1', {'post_publish':'post_publish', 'user':self.test_post.user, 'title': 'publishedDraftTest', 'body': self.test_post.body})
        #Checking if it has become a post now
        self.published_draft = PostModel.objects.get(title="publishedDraftTest")
        self.assertEqual(self.published_draft.title, "publishedDraftTest")

        #Saving a draft
        response = self.client.post('/posts/draft/2', {'draft_save':'draft_save', 'user':self.test_post.user, 'title': 'savedDraftTest', 'body': self.test_post.body})
        self.saved_draft = DraftModel.objects.get(title="savedDraftTest")
        self.assertEqual(self.saved_draft.title, "savedDraftTest")

        #Commenting on a post
        response = self.client.post('/post/comment', {'id': 1, 'user': self.user, 'text': "commentBody"})
        self.created_comment = CommentModel.objects.get(body="commentBody")
        self.assertEqual(self.created_comment.body, "commentBody")

    def test_view_create_post_validator(self):
        #Creating a new post with a title longer than 30 chars        
        response = self.client.post('/posts/create', {'post_submit':'post_submit', 'user':self.test_post.user, 'title': self.long_title_30, 'body': self.test_post.body})
        #Checking if response contains the error message
        self.assertEqual(response.context['error'], "Post too long. Title max length is 30 characters! Body max length is 3000 characters!")

        #Creating a new draft with a title longer than 30 chars        
        response = self.client.post('/posts/create', {'draft_submit':'draft_submit', 'user':self.test_post.user, 'title': self.long_title_30, 'body': self.test_post.body})
        #Checking if response contains the error message
        self.assertEqual(response.context['error'], "Post too long. Title max length is 30 characters! Body max length is 3000 characters!")

        #Publishing a draft with a title longer than 30 chars        
        response = self.client.post('/posts/draft/1', {'post_publish':'post_publish', 'user':self.test_post.user, 'title': self.long_title_30, 'body': self.test_post.body})
        #Checking if response contains the error message
        self.assertEqual(response.context['error'], "Post too long. Title max length is 30 characters! Body max length is 3000 characters!")

        #Saving a draft with a title longer than 30 chars        
        response = self.client.post('/posts/draft/1', {'draft_save':'draft_save', 'user':self.test_post.user, 'title': self.long_title_30, 'body': self.test_post.body})
        #Checking if response contains the error message
        self.assertEqual(response.context['error'], "Post too long. Title max length is 30 characters! Body max length is 3000 characters!")

        #Saving a draft with a title longer than 30 chars        
        response = self.client.post('/post/comment', {'id': 1, 'user': self.user, 'text': self.long_body_1000})
        #Checking if response contains the error message
        self.assertEqual(response.context['error'], "Comment too long. Max length is 1000 characters!")