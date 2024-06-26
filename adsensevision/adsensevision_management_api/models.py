# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Camera(models.Model):
    name = models.CharField(max_length=120)
    url_address = models.CharField(max_length=80)
    connection_login = models.CharField(max_length=50)
    connection_password = models.CharField(max_length=50)
    location_address = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'camera'
        # Параметры для панели администратора
        verbose_name = "Камера"
        verbose_name_plural = "Камеры"


class CameraScreen(models.Model):
    camera = models.ForeignKey(Camera, models.DO_NOTHING, blank=True, null=True)
    screen = models.ForeignKey('Screen', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'camera_screen'
        # Параметры для панели администратора
        verbose_name = "Камера-экран"
        verbose_name_plural = "Камера-экран"


class MediaContent(models.Model):
    video = models.FileField(upload_to='videos/')  # Изменено на FileField
    name = models.CharField(max_length=120, blank=True, null=True)
    description = models.CharField(max_length=360, blank=True, null=True)
    upload_date = models.DateField(blank=True, null=True)
    duration = models.TimeField(blank=True, null=True)
    preview = models.ImageField(upload_to='previews/', blank=True, null=True)  # Изменено на ImageFiled

    class Meta:
        managed = False
        db_table = 'media_content'
        # Параметры для панели администратора
        verbose_name = "Медиаконтент"
        verbose_name_plural = "Медиаконтент"


class Schedule(models.Model):
    queue_number = models.IntegerField()
    media_content = models.ForeignKey(MediaContent, models.DO_NOTHING, blank=True, null=True)
    screen = models.ForeignKey('Screen', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'schedule'
        # Параметры для панели администратора
        verbose_name = "Расписание"
        verbose_name_plural = "Расписание"


class Screen(models.Model):
    name = models.CharField(max_length=120)
    start_time = models.TimeField()
    end_time = models.TimeField()
    pause_time = models.TimeField()
    update_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'screen'
        # Параметры для панели администратора
        verbose_name = "Экран"
        verbose_name_plural = "Экраны"


class Statistics(models.Model):
    media_content = models.ForeignKey(MediaContent, models.DO_NOTHING, blank=True, null=True)
    screen = models.ForeignKey(Screen, models.DO_NOTHING, blank=True, null=True)
    total_viewing_time = models.TimeField()
    max_viewers_count = models.IntegerField()
    show_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'statistics'
        # Параметры для панели администратора
        verbose_name = "Статистика"
        verbose_name_plural = "Статистика"


class StatisticsPerShow(models.Model):
    media_content = models.ForeignKey(MediaContent, models.DO_NOTHING, blank=True, null=True)
    screen = models.ForeignKey(Screen, models.DO_NOTHING, blank=True, null=True)
    viewing_time = models.TimeField()
    viewers_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'statistics_per_show'
        # Параметры для панели администратора
        verbose_name = "Статистика показа"
        verbose_name_plural = "Статистика показа"


