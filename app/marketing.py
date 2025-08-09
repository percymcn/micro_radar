import logging
def post_to_x(message: str): logging.info("[stub] X post: %s", message)
def post_to_telegram(message: str, channel: str="@micro_radar"): logging.info("[stub] Telegram %s: %s", channel, message)
