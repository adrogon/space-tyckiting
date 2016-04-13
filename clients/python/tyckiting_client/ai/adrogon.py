import random

from tyckiting_client.ai import base
from tyckiting_client import actions
from tyckiting_client import messages
import logging


class Ai(base.BaseAi):
    """
    Awesome bot that destroys anything in sight.
    """

    def move(self, bots, events):
        """
        Assign a convenient Move to each bot.

        Args:
            bots: List of bot states for own team
            events: List of events form previous round

        Returns:
            List of actions to perform this round.
        """

        for bot in bots:
            logging.info(bot)
        for event in events:
            logging.info(event)

        response = []

        for event in events:
            # Take evasive actions
            if event.event in ['detected', 'damaged']:
                for bot in bots:
                    if bot.bot_id != event.bot_id:
                        continue
                    move_pos = random.choice(list(self.get_valid_moves(bot)))
                    response.append(actions.Move(bot_id=event.bot_id,
                                                 x=move_pos.x,
                                                 y=move_pos.y))

            # Found somebody, fire in the hole
            if event.event == ['radarEcho']:
                for bot in bots:
                    response.append(actions.Cannon(bot_id=bot.bot_id, x=0, y=0))
                    response.append(
                            actions.Cannon(bot_id=bot.bot_id, x=0 + self.config.cannon, y=0 + self.config.cannon))
                    response.append(
                            actions.Cannon(bot_id=bot.bot_id, x=0 - self.config.cannon, y=0 - self.config.cannon))

            # Default action
            for bot in bots:
                radar_pos = random.choice(list(self.get_valid_radars(bot)))
                response.append(actions.Radar(bot_id=bot.bot_id,
                                              x=radar_pos.x,
                                              y=radar_pos.y))

                # for bot in bots:
                #     if not bot.alive:
                #         continue
                #
                #     response.append(actions.Cannon(bot_id=bot.bot_id, x=0, y=0))

                # move_pos = random.choice(list(self.get_valid_moves(bot)))
                # response.append(actions.Move(bot_id=bot.bot_id,
                #                              x=move_pos.x,
                #                              y=move_pos.y))

        return response
