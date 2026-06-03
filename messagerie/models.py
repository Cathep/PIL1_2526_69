from django.db import models
from comptes.models import Utilisateur
from mentorat.models import Matching


class Conversation(models.Model):
    utilisateur1 = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='conversations_en1')
    utilisateur2 = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='conversations_en2')
    matching = models.ForeignKey(Matching, on_delete=models.SET_NULL, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'conversations'
        verbose_name = 'Conversation'
        # empecher les doublons - user1 doit toujours avoir id < user2
        unique_together = ('utilisateur1', 'utilisateur2')

    def __str__(self):
        return f"Conv. {self.utilisateur1} ↔ {self.utilisateur2}"

    @staticmethod
    def get_ou_creer(user_a, user_b, matching=None):
        # on trie pour respecter la contrainte user1_id < user2_id
        if user_a.id > user_b.id:
            user_a, user_b = user_b, user_a
        conv, cree = Conversation.objects.get_or_create(
            utilisateur1=user_a,
            utilisateur2=user_b,
            defaults={'matching': matching}
        )
        return conv


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    expediteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    contenu = models.TextField()
    lu = models.BooleanField(default=False)
    date_envoi = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        verbose_name = 'Message'
        ordering = ['date_envoi']

    def __str__(self):
        return f"{self.expediteur} : {self.contenu[:40]}"
