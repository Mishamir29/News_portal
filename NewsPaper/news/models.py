from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # Рейтинг каждой статьи автора умножается на 3;
        post_rating = sum(post.rating * 3 for post in self.posts.all())

        # Рейтинг комментариев автора;
        comment_rating = sum(comment.rating for comment in Comment.objects.filter(user=self.user))

        # Рейтинг всех комментариев к статьям автора
        comment_to_posts_rating= sum(
            comment.rating for post in self.posts.all()
            for comment in post.comments.all())
        self.rating = post_rating + comment_rating + comment_to_posts_rating
        self.save()

    def __str__(self):
        return self.user.username

POST_TYPE_CHOICES = [
    ('статья', 'Статья'),
    ('новость', 'Новость'),
]

class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    POST_TYPE_CHOICES = [(NEWS, 'Новость'),(ARTICLE, 'Статья')]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts_authors")
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField("Category",through='PostCategory', related_name='posts')
    title = models.CharField(max_length=255)
    post_type = models.CharField(max_length=2, choices=POST_TYPE_CHOICES)
    content = models.TextField()
    rating = models.IntegerField(default= 0)

    def like(self):
        self.rating= self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()

    def preview(self):
        return self.content[:124] + '...'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("news_detail", kwargs={"pk": self.pk})


class Category(models.Model):
    name= models.CharField(max_length= 255, unique= True)

    subscribers = models.ManyToManyField(User,
                                         related_name='subscribed_categories',
                                         blank=True
                                         )

    def __str__(self): return self.name


class PostCategory(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_categories_through")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="category_posts_through")

    class Meta:
        unique_together = ('post', 'category')


class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"Комментарий от {self.user.username} к '{self.post.title}'"

