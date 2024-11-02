from django.db.models import CASCADE
from django.db import models

from .recipients import Recipient
from .users import UserProfile


class AbstractMessage(models.Model):
    MAX_TOPIC_NAME_LENGTH = 60

    id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
    )
    sender = models.ForeignKey(UserProfile, on_delete=CASCADE)

    # The target of the message is signified by the Recipient object.
    # See the Recipient class for details.
    recipient = models.ForeignKey(Recipient, on_delete=CASCADE)

    class MessageType(models.IntegerChoices):
        NORMAL = 1
        RESOLVE_TOPIC_NOTIFICATION = 2

    # IMPORTANT: message.type is not to be confused with the
    # "recipient type" ("channel" or "direct"), which is sometimes
    # called message_type in the APIs, CountStats or some variable
    # names. We intend to rename those to recipient_type.
    #
    # Type of the message, used to distinguish between "normal"
    # messages and some special kind of messages, such as notification
    # messages that may be sent by system bots.
    type = models.PositiveSmallIntegerField(
        choices=MessageType.choices,
        default=MessageType.NORMAL,
        # Note: db_default is a new feature in Django 5.0, so we don't use
        # it across the codebase yet. It's useful here to simplify the
        # associated database migration, so we're making use of it.
        db_default=MessageType.NORMAL,
    )

    # The message's topic.
    #
    # Early versions of Zulip called this concept a "subject", as in an email
    # "subject line", before changing to "topic" in 2013 (commit dac5a46fa).
    # UI and user documentation now consistently say "topic".  New APIs and
    # new code should generally also say "topic".
    #
    # See also the `topic_name` method on `Message`.
    subject = models.CharField(max_length=MAX_TOPIC_NAME_LENGTH, db_index=True)

    # The raw Markdown-format text (E.g., what the user typed into the compose box).
    content = models.TextField()

    # The HTML rendered content resulting from rendering the content
    # with the Markdown processor.
    rendered_content = models.TextField(null=True)
    # A rarely-incremented version number, theoretically useful for
    # tracking which messages have been already rerendered when making
    # major changes to the markup rendering process.
    rendered_content_version = models.IntegerField(null=True)

    date_sent = models.DateTimeField("date sent", db_index=True)

    # The last time the message was modified by message editing or moving.
    last_edit_time = models.DateTimeField(null=True)

    # A JSON-encoded list of objects describing any past edits to this
    # message, oldest first.
    edit_history = models.TextField(null=True)

    # Whether the message contains a (link to) an uploaded file.
    has_attachment = models.BooleanField(default=False, db_index=True)
    # Whether the message contains a visible image element.
    has_image = models.BooleanField(default=False, db_index=True)
    # Whether the message contains a link.
    has_link = models.BooleanField(default=False, db_index=True)

    class Meta:
        abstract = True


class Message(AbstractMessage):
    API_RECIPIENT_TYPES = ["direct", "channel"]
