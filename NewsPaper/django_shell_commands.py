from django.contrib.auth.models import User
from news.models import Author, Category, Post, Comment


# Создание пользователей:
user1 = User.objects.create_user('Frodo_Baggins')
user2= User.objects.create_user('John_Smith')


# Создание авторов:
author1, created = Author.objects.get_or_create(user=user1)
author2, created = Author.objects.get_or_create(user=user2)


# Создание 4 категорий постов
cat_sport, _ = Category.objects.get_or_create(name='Спорт')
cat_politics, _ = Category.objects.get_or_create(name='Политика')
cat_humor, _ = Category.objects.get_or_create(name='Юмор')
cat_education,_ = Category.objects.get_or_create(name='Образование')


# Создание 2 статей и 1 новости:
post1 = Post.objects.create(
    author = author1,
    post_type = 'статья',
    title= 'Литрбол - Олимпийский вид спорта?',
    content= 'вид спорта, известный со времён Геракла и Ганнибала Лектора. В этом особо трудном виде спорта могут участвовать практически все '
)

post2 = Post.objects.create(
    author=author1,
    post_type='статья',
    title='Польза бега для здоровья',
    content='Бег — один из самых доступных и эффективных видов кардио. Он укрепляет сердце, помогает снизить стресс и поддерживать форму...'
)

post3 = Post.objects.create(
    author=author2,
    post_type='новость',
    title= 'Выплату к началу учебного года в размере МРОТ хотят ввести для всех школьников',
    content = 'Расширить поддержку семей с детьми предложила группа парламентариев. Об этом сообщили в телеграм-канале депутата...'
)


# Присвоение категорий:
post1.categories.add(cat_sport,cat_humor)
post2.categories.add(cat_sport)
post3.categories.add(cat_politics,cat_education)


# Создание комментариев:
comment1 = Comment.objects.create(
    post=post1,
    user= user1,
    text= 'Посмеялся со статьи, ну и подумываю теперь стать "спортсменом"!'
)

comment2 = Comment.objects.create(
    post= post1,
    user= user2,
    text= 'Абсурдная статья!Как такое вообще могли причислить к спорту?!'
)

comment3 = Comment.objects.create(
    post= post2,
    user= user1,
    text= 'Спасибо! После прочтения, решил начать своё утро с лёгкой пробежки.'
)

comment4 = Comment.objects.create(
    post= post3,
    user= user2,
    text= 'Хорошая новость, хотелось бы узнать подробнее о способах получения.'
)


# Лайки и дизлайки к статьям:
post1.like()
post1.dislike()
post1.dislike()
post1.dislike()

post2.like()
post2.dislike()
post2.like()

post3.like()


#Лайки и дизлайки к комментариям:
comment1.like()
comment1.like()
comment2.dislike()
comment3.like()
comment4.like()


# Обновление рейтинга авторов:
author1.update_rating()
author2.update_rating()


# Вывод рейтинга и лучшего пользователя:
best_author = Author.objects.order_by('-rating').first()
print(f"Лучший автор:{best_author.user.username}, Рейтинг: {best_author.rating}")


# Вывод лучшей статьи:
best_post = Post.objects.filter(post_type='статья').order_by('-rating').first()

print(f"Дата публикации: {best_post.created_at}")
print(f"Автор: {best_post.author.user.username}")
print(f"Рейтинг статьи: {best_post.rating}")
print(f"Заголовок: {best_post.title}")
print(f"Превью: {best_post.preview()}")

# Вывести все комментарии к этой лучшей статье:
comments = Comment.objects.filter(post=best_post)

for comment in comments:
    print(
        f"Дата: {comment.created_at.strftime('%Y-%m-%d %H:%M')}, "
        f"Пользователь: {comment.user.username}, "
        f"Рейтинг: {comment.rating}, "
        f"Текст: {comment.text}"
    )

