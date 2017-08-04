from channels.routing import route

from channels import include



channel_routing = [
    include("games.routing.gomoku_websocket_routing", path=r"^/gomoku/"),
    include("games.routing.bridge_websocket_routing", path=r"^/bridge/"),
]

"""
channel_routing = [
    route("http.request", "games.consumers.http_consumer"),
]
"""