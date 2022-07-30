from level import Level


class TurnManager:
    def __init__(self, level: Level):
        self.level = level
        self.action_queue = []
        self.actors = []

    def _get_actors(self):
        self.actors = [obj for obj in self.level.get_objects() if obj.is_actor]

    def _collect_actions(self):
        for actor in self.actors:
            self.action_queue.append(actor.choose_action())

    def _execute_queue(self):
        for action in self.action_queue:
            action[0](*action[1])

    def make_turn(self):
        self._get_actors()
        self._collect_actions()
        self._execute_queue()
        self.action_queue = []

#  TODO: make wrong inputs by player not count as a turn
