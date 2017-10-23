# https://gearheart.io/blog/creating-a-chat-with-django-channels/

from channels import route


# This function will display all messages received in the console
def message_handler(message):
    print(message['text'])
    print("Ethe pahuch gaya hai babua")


channel_routing = [
    route("websocket.receive", message_handler)  # we register our message handler
]