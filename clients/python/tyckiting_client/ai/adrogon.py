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

        #    for bot in bots:
        #        logging.info(bot)
        #    for event in events:
        #        logging.info(event)

        response = []

        radar_positions = [
            [0, -11],
            [4, -11],
            [8, -11],
            [11, -11],
            [-4, -7],
            [1, -5],
            [5, -5],
            [9, -5],
            [11, -5],
            [-8, -3],
            [-3, -1],
            [1, -1],
            [5, -1],
            [9, -1],
            [12, -1]
        ]


        for event in events:
            if event.event in ['detected', 'damaged']:
                for bot in bots:
                    if bot.bot_id != event.bot_id:
                        continue
                    move_pos = random.choice(list(self.get_valid_moves(bot)))
                    response.append(actions.Move(bot_id=event.bot_id,
                                                 x=move_pos.x,
                                                 y=move_pos.y))

            if event.event in ['radarEcho']:
                logging.info(event.event)
                for bot in bots:
                    response.append(actions.Cannon(bot_id = bot.bot_id, x = event.pos.x, y = event.pos.y))

        # Default action
        radar_pos = random.choice(list(self.get_valid_radars(bots[0])))


        bot_one = [radar_pos.x+7, radar_pos.y-3]
        bot_two = [radar_pos.x +3, radar_pos.y + 4]

        response.append(actions.Radar(bot_id=bots[0].bot_id, x=radar_pos.x , y=radar_pos.y))
        response.append(actions.Radar(bot_id=bots[1].bot_id, x=bot_one[0], y=bot_one[1]))
        response.append(actions.Radar(bot_id=bots[2].bot_id, x=bot_two[0], y=bot_two[1]))

        return response
