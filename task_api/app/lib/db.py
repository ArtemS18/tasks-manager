from sqlalchemy.orm import relationship as sa_relationship


def relationship(*args, **kwargs):
    if not kwargs.get("lazy"):
        kwargs["lazy"] = "noload"
    return sa_relationship(*args, **kwargs)
