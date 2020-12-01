from django.dispatch import Signal


flag_disabled = Signal(providing_args=["instance", "flag_name"])
flag_enabled = Signal(providing_args=["instance", "flag_name"])
