import random

from tyckiting_client.ai import base
from tyckiting_client import actions
from tyckiting_client import messages
import logging
import random


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

        boots = []
        for bot in bots:
            if bot.alive:
                boots.append(bot)

        response = []

        radar_positions = [
            [0, -11],
            [11, -8],
            [0, -4],
            [4, 3],
            [8, -4],
            [11, -4],
            [0, 7],
            [-11, 0],
            [-4, 7],
            [-11, 3],
            [4, -11],
            [11, 0],
            [-8, -3],
            [4, -4],
            [8, -11],
            [-4, 0],
            [11, -11],
            [0, 3],
            [-4, -7],
            [8, 3],
            [-11, 7],
            [-8, 7],
            [4, 7]
        ]

        for event in events:
            if event.event in ['detected', 'damaged']:
                for bot in boots:
                    if bot.bot_id != event.bot_id:
                        continue
                    move_pos = random.choice(list(self.get_valid_moves(bot)))
                    response.append(actions.Move(bot_id=event.bot_id,
                                                 x=move_pos.x,
                                                 y=move_pos.y))

            if event.event in ['radarEcho']:
                if len(boots) > 2:
                    response.append(actions.Radar(bot_id=boots[0].bot_id, x=event.pos.x, y=event.pos.y))
                    rand_int = random.randint(0, 2)
                    if rand_int == 0:
                        response.append(actions.Cannon(bot_id=boots[1].bot_id, x=event.pos.x, y=event.pos.y + 1))
                        response.append(actions.Cannon(bot_id=boots[2].bot_id, x=event.pos.x, y=event.pos.y - 1))
                    elif rand_int == 1:
                        response.append(actions.Cannon(bot_id=boots[1].bot_id, x=event.pos.x + 1, y=event.pos.y - 1))
                        response.append(actions.Cannon(bot_id=boots[2].bot_id, x=event.pos.x - 1, y=event.pos.y + 1))
                    elif rand_int == 2:
                        response.append(actions.Cannon(bot_id=boots[1].bot_id, x=event.pos.x - 1, y=event.pos.y))
                        response.append(actions.Cannon(bot_id=boots[2].bot_id, x=event.pos.x + 1, y=event.pos.y))

                elif len(boots) > 1:
                    response.append(actions.Radar(bot_id=boots[0].bot_id, x=event.pos.x, y=event.pos.y))
                    rand_int = random.randint(0, 2)
                    if rand_int == 0:
                        response.append(actions.Cannon(bot_id=boots[1].bot_id, x=event.pos.x, y=event.pos.y + 1))
                    elif rand_int == 1:
                        response.append(actions.Cannon(bot_id=boots[1].bot_id, x=event.pos.x + 1, y=event.pos.y - 1))
                    elif rand_int == 2:
                        response.append(actions.Cannon(bot_id=boots[1].bot_id, x=event.pos.x - 1, y=event.pos.y))

                else:
                    rand_int = random.randint(0, 2)
                    if rand_int == 0:
                        response.append(actions.Cannon(bot_id=boots[0].bot_id, x=event.pos.x, y=event.pos.y + 1))
                    elif rand_int == 1:
                        response.append(actions.Cannon(bot_id=boots[0].bot_id, x=event.pos.x + 1, y=event.pos.y - 1))
                    elif rand_int == 2:
                        response.append(actions.Cannon(bot_id=boots[0].bot_id, x=event.pos.x - 1, y=event.pos.y))

        # Default action
        another_rand_int = random.randint(0, len(radar_positions) - 2)

        response.append(
                actions.Radar(bot_id=boots[0].bot_id, x=radar_positions[another_rand_int][0],
                              y=radar_positions[another_rand_int][1]))
        if len(boots) > 1:
            response.append(actions.Radar(bot_id=boots[1].bot_id, x=radar_positions[another_rand_int + 1][0],
                                          y=radar_positions[another_rand_int + 1][1]))
        if len(boots) > 2:
            response.append(actions.Radar(bot_id=boots[2].bot_id, x=radar_positions[another_rand_int + 2][0],
                                          y=radar_positions[another_rand_int + 2][1]))

        return response
