from handlers.edit import handle_edit_reply
from handlers.add import handle_add_task

def text_message_handler(update, context):
    if context.user_data.get("edit_id"):
        return handle_edit_reply(update, context)
    else:
        return handle_add_task(update, context)
