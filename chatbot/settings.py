CHAT_BUBBLE_USER = (
    """ 
    .QLabel { 
        background-color: grey;
        border-width: 2px;
        border-color: solid black;
        color: solid black;
        border-radius: 25px;
    }
    """
)

CHAT_BUBBLE_BOT = (
    """ 
    .QLabel { 
        background-color: rgb(0, 0, 0);
        color: rgb(243, 243, 243);
        border-radius: 25px;
    }
    """
)

ROLE_DESIGN_MAPPING = {
    'user': CHAT_BUBBLE_USER,
    'bot': CHAT_BUBBLE_BOT
}