from django.db import models
from django.contrib.auth.models import AbstractUser, Permission


class User(AbstractUser):
    first_name = None
    last_name = None

    ROLES = (
        ('operator', 'Operator'),
        ('back_office', 'Back Office Specialist'),
    )
    role = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return self.username


class Ticket(models.Model):
    STATUS_CHOICES = (
        ('Открыт', 'Открыт'),
        ('Закрыт', 'Закрыт'),
        ('В обработке', 'В обработке'),
    )

    account_number = models.CharField(max_length=100)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    description = models.TextField()
    responsible_person = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Обращения'
        verbose_name_plural = 'Обращения'


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментировано {self.author.username} в обращении {self.ticket.title}"

    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'

