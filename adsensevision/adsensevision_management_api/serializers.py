from rest_framework import serializers
from .models import Camera, CameraScreen, MediaContent, Schedule, Screen
from moviepy.editor import VideoFileClip
from django.core.files.base import ContentFile
from .models import MediaContent
import os
import tempfile


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'


class CameraScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraScreen
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = '__all__'


class MediaContentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaContent
        fields = '__all__'  # Все поля для чтения


class MediaContentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaContent
        fields = ['content']  # Ограничение полей для записи

    def create(self, validated_data):
        instance = super().create(validated_data)
        # Получение объекта MediaContent по ID
        media_content = MediaContent.objects.get(id=instance.id)
        # Получение объекта File, связанного с полем content в модели MediaContent
        video_file = media_content.content

        # Загрузка видеофайла в объект VideoFileClip для обработки
        video = VideoFileClip(video_file.path)

        # Извлечение названия файла без расширения
        filename, _ = os.path.splitext(os.path.basename(video_file.name))
        media_content.name = filename

        # Извлечение продолжительности видео и сохранение ее в формате MM:SS
        media_content.duration = str(int(video.duration // 60)) + ":" + str(int(video.duration % 60))

        # Задаем время кадра для превью
        frame_time = 10

        # Создаем временный файл
        fd, temp_preview_path = tempfile.mkstemp(suffix=".jpg")
        os.close(fd)  # Закрываем файловый дескриптор

        try:
            # Сохраняем кадр во временный файл
            video.save_frame(temp_preview_path, t=0)

            # Открываем и читаем временный файл для сохранения в модель
            with open(temp_preview_path, "rb") as file:
                media_content.preview.save(f"{filename}.jpg", ContentFile(file.read()), save=False)

        finally:
            video.close()  # Явно закрываем video
            os.remove(temp_preview_path)  # Удаляем временный файл

        # Сохранение изменений в объекте MediaContent
        media_content.save(update_fields=['name', 'duration', 'preview'])
        return instance

