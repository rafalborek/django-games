from channels import route

from .gomoku.consumers import gomoku_ws_connect, gomoku_ws_receive, gomoku_ws_disconnect
from .bridge.consumers import bridge_ws_connect, bridge_ws_receive, bridge_ws_disconnect


"""
# You can have as many lists here as you like, and choose any name.
# Just refer to the individual names in the include() function.
custom_routing = [
    # Handling different chat commands (websocket.receive is decoded and put
    # onto this channel) - routed on the "command" attribute of the decoded
    # message.
    route("chat.receive", chat_join, command="^join$"),
    route("chat.receive", chat_leave, command="^leave$"),
    route("chat.receive", chat_send, command="^send$"),
]
"""


gomoku_websocket_routing = [
    # Called when WebSockets connect
    route("websocket.connect", gomoku_ws_connect),

    # Called when WebSockets get sent a data frame
    route("websocket.receive", gomoku_ws_receive),

    # Called when WebSockets disconnect
    route("websocket.disconnect", gomoku_ws_disconnect),
]

bridge_websocket_routing = [
    # Called when WebSockets connect
    route("websocket.connect", bridge_ws_connect),

    # Called when WebSockets get sent a data frame
    route("websocket.receive", bridge_ws_receive),

    # Called when WebSockets disconnect
    route("websocket.disconnect", bridge_ws_disconnect),
]
