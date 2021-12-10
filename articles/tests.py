from django.http import response
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Article

class ArticleTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", email="test@email.com", password="secret"
        )
        self.post = Article.objects.create(
            title="A title", body="A body", author=self.user
        )

    def test_string_representation(self):
        post = Article(title="A sample title")
        self.assertEqual(str(post), post.title)

    def test_get_absolute_url(self):
        self.assertEqual(str(self.post.get_absolute_url()), "/blog/1/")

    def test_post_content(self):
        self.assertEqual(f"{self.post.title}", "A title")
        self.assertEqual(f"{self.post.author}", "test")
        self.assertEqual(f"{self.post.body}", "A body")

    def test_post_list_view(self):
        response = self.client.get(reverse("blog_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A body")
        self.assertTemplateUsed(response, "blog_list.html")

    def test_post_detail_view(self):
        response = self.client.get("/blog/1/")
        not_found_response = self.client.get("/blog/1000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(not_found_response.status_code, 404)
        self.assertContains(response, "A title")
        self.assertTemplateUsed(response, "blog_detail.html")

    def test_post_create_view(self):
        response = self.client.post(
            reverse("blog_new"),
            {"title": "new title", "body": "new body", "author": self.user.id},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Article.objects.last().title, "new title")
        self.assertEqual(Article.objects.last().body, "new body")

    def test_article_update_view(self):
        response = self.client.post(
            reverse("article_edit", args=[1]),
            {
                "title": "Updated title",
                "body": "Updated body",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):
        response = self.client.post(reverse("article_delete", args=[1]))
        self.assertEqual(response.status_code, 302)

