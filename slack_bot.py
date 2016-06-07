from slackclient import SlackClient
from time import sleep
from random import randint


def handler(firehose):
    if len(firehose) > 0 and "text" in firehose[0] and "user" in firehose[0]: # Filters everything but chat messages.
        text = firehose[0]["text"]  # Content of chat message
        user = firehose[0]["user"]  # User ID of chat message
        channel = firehose[0]["channel"]  # Channel of chat message
        print("On " + channel + ", " + user + " says: " + text)  # Showing information in console for debugging
        recent_comments.append(text.lower())  # Logging comments for possible contextual use.
        if bot_id in text and user != bot_id:
            if "help" in text.lower():
                sc.rtm_send_message(channel, "I work best when you speak to me like a person.  "
                                             "I'll figure out what you're looking for through contextual clues.  "
                                             "You might try asking me about the next assignment, it's due date, "
                                             "when it will be graded, or any number of other things.")
            elif "debug bot" in text.lower():
                sc.rtm_send_message(channel, str(randint(100000, 200000)))  # Checking for multiple instances
                for message in recent_comments:  # Showing messages in recent_comments
                    sc.rtm_send_message(channel, message)
                sc.rtm_send_message(channel, "https://github.com/JB-pythonic-py/starterbot-for-slack")


            #  There might be a better way to do this, but I'm using list comprehension to prevent false positive chat.

            elif all(x in text.lower() for x in ["next", "due"]) and any(
                            y in text.lower() for y in ["assignment", "project", "homework", "test", "quiz", "lab"]):
                sc.rtm_send_message(channel, "Our next assignment is due on: {Build assignment dictionary.}")

            elif all(x in text.lower() for x in ["next", "what"]) and any(
                            y in text.lower() for y in ["assignment", "project", "homework", "test", "quiz", "lab"]):
                sc.rtm_send_message(channel, "Our next assignment is: {Build assignment dictionary.}")

            elif any(x in text.lower() for x in ["grade", "graded", "grading"]):
                sc.rtm_send_message(channel, "Hahahahaha!")
                sleep(1)
                sc.rtm_send_message(channel, "Oh, you were serious?")
                sleep(2)
                sc.rtm_send_message(channel, "Mary grades your assignments when she feels like it.  :)")

            elif any(x in text.lower() for x in ["hi", "hello", "howdy", "hey"]):
                sc.rtm_send_message(channel, "Howdy!")

            else:
                sc.rtm_send_message(channel, "I'm sorry, I don't know how to respond to that.")

        if bot_name in text.lower() and user != bot_id and bot_id not in text:  # Making sure people are talking to him.
            sc.rtm_send_message(channel, "I heard my name.  If you're trying to talk to me, use @starterbot.")

        if any(x == text.lower() for x in ["what", "what?", "wat", "wat?", "wut", "wut?", "wot", "wot?"]):  # LOL
            louder = recent_comments[-2].upper()
            sc.rtm_send_message(channel, louder)



bot_name = "starterbot"

token = "Create a token at https://my.slack.com/services/new/bot"

sc = SlackClient(token)
if sc.rtm_connect():
    print("Starterbot successfully connected.")

for usr in sc.api_call("users.list")["members"]:  # Finding the bot's id from channel userlist.
    if bot_name == usr["name"]:
        bot_id = usr["id"]

recent_comments = ["1", "2"]  # When bot starts, last line of chat is loaded.  This prevents any errors with that.

while True:
    handler(sc.rtm_read())
    while len(recent_comments) > 2:  # Keeping only last 2 recent comments.
        del recent_comments[0]
    sleep(1)
