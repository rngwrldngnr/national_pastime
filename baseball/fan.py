class Fan(object):
    """The baseball-fan layer of a person's being."""

    def __init__(self, person):
        """Initialize a Fan object."""
        self.person = person  # The person in whom this fan layer embeds
        self.games_attended = []

    def attend_game(self, game):
        """Attend a baseball game."""
        # Update attributes
        self.games_attended.append(game)

    def heckle(self, player):
        """Heckle a player, thus affecting the player's internal state."""
        # TODO SELECT EFFECTIVE THOUGHT_PROTOTYPE FORCE A CALL TO PLAYER.MIND.ENTERTAIN(THOUGHT_PROTOTYPE)
        pass