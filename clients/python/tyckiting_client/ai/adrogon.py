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

        response = []
        hex_visisted = []

        radar_positions = [
            [0, -11],
            [4, -11],
            [8, -11],
            [11, -11],
            [11, -8],
            [-4, -7],
            [0, -4],
            [4, -4],
            [8, -4],
            [11, -4],
            [-11, 0],
            [-11, 3],
            [11, 0],
            [-8, -3],
            [-4, 0],
            [0, 3],
            [4, 3],
            [8, 3],
            [-11, 7],
            [-8, 7],
            [-4, 7],
            [0, 7],
            [4, 7]
        ]

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

            # HIT SOMEBODY!! FIRE MORE!!
            # if event.event in ['hit']:
            #     if len(bots) == 3:
            #         response.append(actions.Radar(bot_id=bot_ids[0], x=event.pos.x, y=event.pos.y))
            #         response.append(actions.Cannon(bot_id=bot_ids[1], x=event.pos.x, y=event.pos.y + 1))
            #         response.append(actions.Cannon(bot_id=bot_ids[2], x=event.pos.x, y=event.pos.y + 1))
            #         logging.info("bots shooting around %s,%s", event.pos.x, event.pos.y)

            # Found somebody, fire in the hole
            if event.event in ['radarEcho']:
                if len(bots) == 3:
                    response.append(actions.Radar(bot_id=bots[0].bot_id, x=event.pos.x, y=event.pos.y))
                    rand_int = random.randint(0, 2)
                    if rand_int == 0:
                        response.append(actions.Cannon(bot_id=bots[1].bot_id, x=event.pos.x, y=event.pos.y + 1))
                        response.append(actions.Cannon(bot_id=bots[2].bot_id, x=event.pos.x, y=event.pos.y - 1))
                    elif rand_int == 1:
                        response.append(actions.Cannon(bot_id=bots[1].bot_id, x=event.pos.x + 1, y=event.pos.y - 1))
                        response.append(actions.Cannon(bot_id=bots[2].bot_id, x=event.pos.x - 1, y=event.pos.y + 1))
                    elif rand_int == 2:
                        response.append(actions.Cannon(bot_id=bots[1].bot_id, x=event.pos.x - 1, y=event.pos.y))
                        response.append(actions.Cannon(bot_id=bots[2].bot_id, x=event.pos.x + 1, y=event.pos.y))

                    logging.info("bots shooting around %s,%s", event.pos.x, event.pos.y)

        # Default action
        radar_pos = random.choice(list(self.get_valid_radars(bots[0])))

        start_posy = 0

        hex_visisted.append(radar_pos)
        logging.info(hex_visisted)

        response.append(actions.Radar(bot_id=bots[0].bot_id, x=radar_pos.x, y=radar_pos.y))
        response.append(actions.Radar(bot_id=bots[1].bot_id, x=radar_pos.x + 7, y=radar_pos.y - 3))
        response.append(actions.Radar(bot_id=bots[2].bot_id, x=radar_pos.x + 3, y=radar_pos.y + 4))

        return response
