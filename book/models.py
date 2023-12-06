from django.db import models


# Create your models here.

class Books(models.Model):
    id = models.CharField(primary_key=True, max_length=20, verbose_name='图书编号')
    name = models.CharField(max_length=20, verbose_name='图书名称')
    status = models.BooleanField(default=False, verbose_name='是否出借', blank=True)

    # 元信息
    class Meta:
        # 数据库的表名
        db_table = 'book'
        # 后台的字段名称
        verbose_name = '图书表'

    # 打印这个图书对象的时候显示的是什么
    def __str__(self):
        return self.name


class Record(models.Model):
    # on_delete=models.CASCADE 如果Books表 被删除，则在Recoed表中一并删除
    book = models.ForeignKey('Books', on_delete=models.CASCADE, verbose_name="借还书籍")
    name = models.CharField(max_length=20, verbose_name='借书人')
    s_time = models.DateTimeField(auto_created=True, auto_now=True, blank=True, verbose_name='借书时间')
    e_time = models.DateTimeField(auto_created=True, auto_now=True, verbose_name='还书时间', blank=True)
    # false 表示未还,可以借出
    state = models.BooleanField(default=False, verbose_name='是否归还', blank=True)
