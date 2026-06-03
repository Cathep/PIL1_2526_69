from django.contrib import admin
from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('expediteur', 'contenu', 'date_envoi', 'lu')


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('utilisateur1', 'utilisateur2', 'date_creation')
    search_fields = ('utilisateur1__nom', 'utilisateur2__nom')
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'expediteur', 'contenu_court', 'lu', 'date_envoi')
    list_filter = ('lu',)
    search_fields = ('expediteur__nom', 'contenu')

    def contenu_court(self, obj):
        return obj.contenu[:50] + '...' if len(obj.contenu) > 50 else obj.contenu
    contenu_court.short_description = 'Message'
