from allauth.account.admin import EmailAddressAdmin, EmailConfirmationAdmin
from allauth.account.models import EmailConfirmation, EmailAddress
from allauth.socialaccount.admin import (
    SocialAppAdmin,
    SocialTokenAdmin,
    SocialAccountAdmin,
)
from allauth.socialaccount.models import SocialApp, SocialToken, SocialAccount
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from machina.apps.forum.admin import ForumAdmin
from machina.apps.forum.models import Forum
from machina.apps.forum_conversation.admin import TopicAdmin, PostAdmin
from machina.apps.forum_conversation.forum_attachments.admin import AttachmentAdmin
from machina.apps.forum_conversation.forum_attachments.models import Attachment
from machina.apps.forum_conversation.forum_polls.admin import (
    TopicPollAdmin,
    TopicPollOptionAdmin,
    TopicPollVoteAdmin,
)
from machina.apps.forum_conversation.forum_polls.models import (
    TopicPoll,
    TopicPollOption,
    TopicPollVote,
)
from machina.apps.forum_conversation.models import Topic, Post
from machina.apps.forum_member.admin import ForumProfileAdmin
from machina.apps.forum_member.models import ForumProfile
from machina.apps.forum_permission.admin import (
    ForumPermissionAdmin,
    GroupForumPermissionAdmin,
    UserForumPermissionAdmin,
)
from machina.apps.forum_permission.models import (
    ForumPermission,
    GroupForumPermission,
    UserForumPermission,
)
from machina.apps.forum_tracking.admin import ForumReadTrackAdmin, TopicReadTrackAdmin
from machina.apps.forum_tracking.models import ForumReadTrack, TopicReadTrack

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin
from unfold.admin import StackedInline
from unfold.mixins import BaseModelAdminMixin

from users.models import Profile


class ProfileInline(StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Профиль"
    fk_name = "user"


# Отменяем стандартную регистрацию модели User
admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ("user", "avatar", "about")
    list_display_links = ("user",)
    list_filter = ("user",)
    search_fields = ("user__username", "user__email")
    list_per_page = 10
    list_max_show_all = 100
    ordering = ("user",)
    readonly_fields = ("user",)


models_to_register = {
    Forum: ForumAdmin,
    Topic: TopicAdmin,
    TopicPoll: TopicPollAdmin,
    TopicPollOption: TopicPollOptionAdmin,
    TopicPollVote: TopicPollVoteAdmin,
    ForumProfile: ForumProfileAdmin,
    ForumPermission: ForumPermissionAdmin,
    GroupForumPermission: GroupForumPermissionAdmin,
    UserForumPermission: UserForumPermissionAdmin,
    ForumReadTrack: ForumReadTrackAdmin,
    TopicReadTrack: TopicReadTrackAdmin,
    Post: PostAdmin,
    Attachment: AttachmentAdmin,
    SocialApp: SocialAppAdmin,
    SocialToken: SocialTokenAdmin,
    SocialAccount: SocialAccountAdmin,
    EmailAddress: EmailAddressAdmin,
}

# Удаляем стандартные регистрации
for model in models_to_register.keys():
    admin.site.unregister(model)

# Регистрируем кастомные админ-классы
for model, admin_class in models_to_register.items():

    @admin.register(model)
    class CustomAdmin(ModelAdmin, admin_class):
        pass
