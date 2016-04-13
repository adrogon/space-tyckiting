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

        bot_ids = []

        for bot in bots:
            bot_ids.append(bot.bot_id)

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
            if event.event in ['radarEcho']:
                for bot in bots:
                    response.append(actions.Cannon(bot_id=bot.bot_id, x=event.pos.x,y=event.pos.y))

            # Default action

            radar_pos = random.choice(list(self.get_valid_radars(bots[0])))
            start_posy = 0

            logging.info(bot_ids[0])

            response.append(actions.Radar(bot_id=bots[0].bot_id, x=start_posx , y=start_posy))
            response.append(actions.Radar(bot_id=bots[1].bot_id, x=start_posx, y=start_posy + 5 ))
            response.append(actions.Radar(bot_id=bots[2].bot_id, x=start_posx , y=start_posy + 9))

            #response.append(actions.Radar(bot_id=bots[0].bot_id, x=radar_pos.x , y=radar_pos.y))
            #response.append(actions.Radar(bot_id=bots[1].bot_id, x=radar_pos.x + 7, y=radar_pos.y - 3))
            #response.append(actions.Radar(bot_id=bots[2].bot_id, x=radar_pos.x + 3, y=radar_pos.y + 4))

                start_posx +=4


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
