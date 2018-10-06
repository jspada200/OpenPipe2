# Copyright 2018 - James Spadafora
# Open Pipe
# Data type for representing a take in the API


class Take(object):
    """Rep a take in the API."""

    def __init__(self,
                 shot,
                 task_type,
                 take_number=None,
                 path=None,
                 created_on=None,
                 created_by=None,
                 take_data={},
                 retarget_list=None):
        """
        Init the take object.
        Args:
            shot(openPipe Shot Object): The shot to create this take for
            task_type(str): The type of task this take is for
            take_number (int) index for this take.
            path(str): Published path to the json take data
            created_on(datetime): When this take was made
            created_by(str): Who created this take
            retarget_list(dict): When processing, we may need to retarget the files for the pubed version of the scene
                This dict contains a mapping of [oldpath] = "new_path" that can be used to rebuild the scene
        """
        self.shot = shot
        self.take_number = take_number
        self.path = path
        self.created_on = created_on
        self.created_by = created_by
        self.retarget_list = retarget_list
        self.task_type = task_type

        print(take_data)
        for k, v in take_data.items():
            setattr(self, k, v)

    def update(self):
        """Update the take in the DB."""
        self.shot._dm.database.update_take(self)