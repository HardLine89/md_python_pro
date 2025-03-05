from django.contrib import admin
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from django.forms import CheckboxInput
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


admin.site.unregister(Forum)
admin.site.unregister(Topic)
admin.site.unregister(TopicPoll)
admin.site.unregister(TopicPollOption)
admin.site.unregister(TopicPollVote)
admin.site.unregister(ForumProfile)
admin.site.unregister(ForumPermission)
admin.site.unregister(GroupForumPermission)
admin.site.unregister(UserForumPermission)
admin.site.unregister(ForumReadTrack)
admin.site.unregister(TopicReadTrack)
admin.site.unregister(Post)
admin.site.unregister(Attachment)


@admin.register(Forum)
class CustomForumAdmin(BaseModelAdminMixin, ForumAdmin):
    pass


@admin.register(Topic)
class CustomForumAdmin(BaseModelAdminMixin, TopicAdmin):
    pass


@admin.register(TopicPoll)
class CustomForumAdmin(BaseModelAdminMixin, TopicPollAdmin):
    pass


@admin.register(TopicPollOption)
class CustomForumAdmin(BaseModelAdminMixin, TopicPollOptionAdmin):
    pass


@admin.register(TopicPollVote)
class CustomForumAdmin(BaseModelAdminMixin, TopicPollVoteAdmin):
    pass


@admin.register(ForumProfile)
class CustomForumAdmin(BaseModelAdminMixin, ForumProfileAdmin):
    pass


@admin.register(ForumPermission)
class CustomForumAdmin(BaseModelAdminMixin, ForumPermissionAdmin):
    pass


@admin.register(GroupForumPermission)
class CustomForumAdmin(BaseModelAdminMixin, GroupForumPermissionAdmin):
    pass


@admin.register(ForumReadTrack)
class CustomForumAdmin(BaseModelAdminMixin, ForumReadTrackAdmin):
    pass


@admin.register(TopicReadTrack)
class CustomForumAdmin(BaseModelAdminMixin, TopicReadTrackAdmin):
    pass


@admin.register(Post)
class CustomForumAdmin(BaseModelAdminMixin, PostAdmin):
    pass


@admin.register(Attachment)
class CustomForumAdmin(BaseModelAdminMixin, AttachmentAdmin):
    pass
