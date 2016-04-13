import random

from tyckiting_client.ai import base
from tyckiting_client import actions
from tyckiting_client import messages
import logging


class Ai(base.BaseAi):
    """
    Awesome bot that destroys anything in sight.
    """
    start_posx = -11

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
                    response.append(actions.Cannon(bot_id=bots[1].bot_id, x=event.pos.x, y=event.pos.y + 1))
                    response.append(actions.Cannon(bot_id=bots[2].bot_id, x=event.pos.x, y=event.pos.y - 1))
                    logging.info("bots shooting around %s,%s", event.pos.x, event.pos.y)

                    # Default action
            radar_pos = random.choice(list(self.get_valid_radars(bots[0])))
            start_posy = 0

            response.append(actions.Radar(bot_id=bots[0].bot_id, x=start_posx, y=start_posy))
            response.append(actions.Radar(bot_id=bots[1].bot_id, x=start_posx, y=start_posy + 5))
            response.append(actions.Radar(bot_id=bots[2].bot_id, x=start_posx, y=start_posy + 9))

            start_posx += 4

            # TEST GRID

        for bot in bots:
            radar_pos = random.choice(list(radar_positions))
            response.append(actions.Radar(bot_id=bot.bot_id,
                                          x=radar_pos[0],
                                          y=radar_pos[1]))

        return response
