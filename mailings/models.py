from django.db import models


NULLABLE = {'blank': True, 'null': True}


class ServiceClient(models.Model):
    email = models.EmailField(verbose_name="электронная почта")
    name = models.CharField(max_length=200, verbose_name="имя")
    comment = models.TextField(verbose_name="комментарий", **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")


    def __str__(self):
        return f"{self.email} ({self.name})"

    class Meta:
        verbose_name = "клиент сервиса"
        verbose_name_plural = "клиенты сервиса"


class Message(models.Model):
    topic = models.CharField(max_length=200, verbose_name="тема сообщения")
    body = models.TextField(verbose_name="текст сообщения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")

    def __str__(self):
        return f"{self.topic}"

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"

class AttemptSend(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name="дата последнего отправления")
    status_send = models.CharField(max_length=20, verbose_name="статус отправки")
    mail_server_response = models.TextField(verbose_name="ответ сервера почты")

    def __str__(self):
        return f"{self.status_send} ({self.mail_server_response[:50]})"

    class Meta:
        verbose_name = "попытка рассылки"
        verbose_name_plural = "попытки рассылки"


class Mailing(models.Model):
    start_date = models.DateTimeField(verbose_name="дата начала рассыл")
    periodicity = models.PositiveIntegerField(verbose_name="периодичность рассыл")
    status = models.CharField(max_length=20, verbose_name="статус рассылки")
    email = models.EmailField(verbose_name="электронная почта")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")

    service_client = models.ForeignKey(ServiceClient, on_delete=models.SET_NULL, verbose_name="клиент сервиса")
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, verbose_name="сообщение")
    attempt_send = models.ForeignKey(AttemptSend, on_delete=models.SET_NULL, verbose_name="попытка рассылки")


    def __str__(self):
        return f"{self.email} ({self.status})"

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"


class User(models.Model):
    name = models.CharField(max_length=200, verbose_name="имя")
    mailings = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="рассылки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    email = models.EmailField(verbose_name="электронная почта")

    def __str__(self):
        return f"{self.email} ({self.name})"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
