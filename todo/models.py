

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


CATEGORY = (('国', '国語'),('数', '数学'), ('英','英語'),('理','理科'), ('社','社会'))
PRIORITY = (1, '★☆☆ (低い)'),(2, '★★☆ (中くらい)'),(3, '★★★ (高い)')

class Task(models.Model):


    CATEGORY_CHOICES = (('国', '国語'),('数', '数学'), ('英','英語'),('理','理科'), ('社','社会'))
    PRIORITY_CHOICES = (1, '★☆☆ (低い)'),(2, '★★☆ (中くらい)'),(3, '★★★ (高い)')


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=2, choices=CATEGORY)
    priority = models.IntegerField(choices=PRIORITY, default=2)

    subtitle1 = models.CharField(max_length=200, blank=True, null=True)
    subtitle1_completed = models.BooleanField(default=False)  # サブタスク1の完了状態
    subtitle2 = models.CharField(max_length=200, blank=True, null=True)
    subtitle2_completed = models.BooleanField(default=False)
    subtitle3 = models.CharField(max_length=200, blank=True, null=True)
    subtitle3_completed = models.BooleanField(default=False)
    subtitle4 = models.CharField(max_length=200, blank=True, null=True)
    subtitle4_completed = models.BooleanField(default=False)
    subtitle5 = models.CharField(max_length=200, blank=True, null=True)
    subtitle5_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


    def check_if_completed(self):
        """すべてのサブタスクが完了したら、タスクも完了済みにする"""
        # サブタスクがすべて完了しているかどうかをチェック
        all_subtasks_completed = all([
            self.subtitle1_completed if self.subtitle1 else True,
            self.subtitle2_completed if self.subtitle2 else True,
            self.subtitle3_completed if self.subtitle3 else True,
            self.subtitle4_completed if self.subtitle4 else True,
            self.subtitle5_completed if self.subtitle5 else True,
        ])
        # すべて完了していれば、親タスクも完了とする
        self.is_completed = all_subtasks_completed
        self.save()







class Template(models.Model):


    CATEGORY = (('国', '国語'),('数', '数学'), ('英','英語'),('理','理科'), ('社','社会'))
    PRIORITY = (1, '★☆☆ (低い)'),(2, '★★☆ (中くらい)'),(3, '★★★ (高い)')


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=2, choices=CATEGORY)
    priority = models.IntegerField(choices=PRIORITY, default=2)

    subtitle1 = models.CharField(max_length=200, blank=True, null=True)
    subtitle2 = models.CharField(max_length=200, blank=True, null=True)
    subtitle3 = models.CharField(max_length=200, blank=True, null=True)
    subtitle4 = models.CharField(max_length=200, blank=True, null=True)
    subtitle5 = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title
