# from datetime import timedelta

# from django.utils.timezone import now as timezone_now

# from zerver.actions.message_send import get_active_presence_idle_user_ids
# from zerver.lib.test_classes import ZulipTestCase
# from zerver.models import Message, UserPresence, UserProfile
# from zerver.models.recipients import (
#     bulk_get_direct_message_group_user_ids,
#     get_direct_message_group_user_ids,
#     get_or_create_direct_message_group,
# )


# class MissedMessageTest(ZulipTestCase):
#     def test_presence_idle_user_ids(self) -> None:
#         UserPresence.objects.all().delete()

#         sender = self.example_user("cordelia")
#         realm = sender.realm
#         hamlet = self.example_user("hamlet")
#         othello = self.example_user("othello")

#         hamlet_notifications_data = self.create_user_notifications_data_object(user_id=hamlet.id)
#         othello_notifications_data = self.create_user_notifications_data_object(user_id=othello.id)

#         def assert_active_presence_idle_user_ids(user_ids: list[int]) -> None:
#             presence_idle_user_ids = get_active_presence_idle_user_ids(
#                 realm=realm,
#                 sender_id=sender.id,
#                 user_notifications_data_list=[
#                     hamlet_notifications_data,
#                     othello_notifications_data,
#                 ],
#             )
#             self.assertEqual(sorted(user_ids), sorted(presence_idle_user_ids))

#         def set_presence(user: UserProfile, client_name: str, ago: int) -> None:
#             when = timezone_now() - timedelta(seconds=ago)
#             UserPresence.objects.update_or_create(
#                 user_profile_id=user.id,
#                 defaults=dict(
#                     realm_id=user.realm_id, last_active_time=when, last_connected_time=when
#                 ),
#             )

#         hamlet_notifications_data.dm_push_notify = True
#         othello_notifications_data.dm_push_notify = True
#         assert_active_presence_idle_user_ids([hamlet.id, othello.id])

#         # We have already thoroughly tested the `is_notifiable` function elsewhere,
#         # so we needn't test all cases here. This test exists mainly to avoid a bug
#         # which existed earlier with `get_active_presence_idle_user_ids` only looking
#         # at `private_message` and the `mentioned` flag, not stream level notifications.
#         # Simulate Hamlet has turned on notifications for the stream, and test that he's
#         # in the list.
#         hamlet_notifications_data.dm_push_notify = False
#         othello_notifications_data.dm_push_notify = False
#         hamlet_notifications_data.stream_email_notify = True
#         assert_active_presence_idle_user_ids([hamlet.id])

#         # Hamlet is idle (and is supposed to receive stream notifications), so he should be in the list.
#         set_presence(hamlet, "iPhone", ago=5000)
#         assert_active_presence_idle_user_ids([hamlet.id])

#         # If Hamlet is active, don't include him in the `presence_idle` list.
#         set_presence(hamlet, "website", ago=15)
#         assert_active_presence_idle_user_ids([])

#         # Hamlet is active now, so only Othello should be in the list for a group
#         # direct message.
#         hamlet_notifications_data.stream_email_notify = False
#         hamlet_notifications_data.dm_push_notify = False
#         othello_notifications_data.dm_push_notify = True
#         assert_active_presence_idle_user_ids([othello.id])


# class TestBulkGetDirectMessageGroupUserIds(ZulipTestCase):
#     def test_bulk_get_direct_message_group_user_ids(self) -> None:
#         hamlet = self.example_user("hamlet")
#         cordelia = self.example_user("cordelia")
#         othello = self.example_user("othello")
#         iago = self.example_user("iago")
#         message_ids = [
#             self.send_group_direct_message(hamlet, [cordelia, othello], "test"),
#             self.send_group_direct_message(cordelia, [hamlet, othello, iago], "test"),
#         ]

#         messages = Message.objects.filter(id__in=message_ids).order_by("id")

#         first_direct_message_group_recipient = messages[0].recipient
#         first_direct_message_group_user_ids = set(
#             get_direct_message_group_user_ids(first_direct_message_group_recipient)
#         )
#         first_direct_message_group = get_or_create_direct_message_group(
#             list(first_direct_message_group_user_ids)
#         )

#         second_direct_message_group_recipient = messages[1].recipient
#         second_direct_message_group_user_ids = set(
#             get_direct_message_group_user_ids(second_direct_message_group_recipient)
#         )
#         second_direct_message_group = get_or_create_direct_message_group(
#             list(second_direct_message_group_user_ids)
#         )

#         direct_message_group_user_ids = bulk_get_direct_message_group_user_ids(
#             [first_direct_message_group_recipient.id, second_direct_message_group_recipient.id]
#         )

#         self.assertEqual(
#             direct_message_group_user_ids[first_direct_message_group_recipient.id],
#             first_direct_message_group_user_ids,
#         )
#         self.assertEqual(
#             first_direct_message_group.group_size, len(first_direct_message_group_user_ids)
#         )

#         self.assertEqual(
#             direct_message_group_user_ids[second_direct_message_group_recipient.id],
#             second_direct_message_group_user_ids,
#         )
#         self.assertEqual(
#             second_direct_message_group.group_size, len(second_direct_message_group_user_ids)
#         )

#     def test_bulk_get_direct_message_group_user_ids_empty_list(self) -> None:
#         self.assertEqual(bulk_get_direct_message_group_user_ids([]), {})
