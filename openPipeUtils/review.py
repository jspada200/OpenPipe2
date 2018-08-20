# Copyright 2018 - James Spadafora
# Open Pipe
# Data type for representing a review in the API

class Review(object):
    """Rep a Review in the API."""

    def __init__(self, shot, take, reviewData=None, **kwargs):
        """
        Init the review object.

        Args:
            shot(openPipe Shot Object): The shot to create this review for
            takeNumber (int) index for this take.
            reviewNumber (int) index for this review
            createdOn(datetime): When this take was made
            createdBy(str): Who created this take
            media (list:str): Paths to media for the review
            notes (list:openPipe Notes): Notes for this review in order
        """
        self.shot = shot
        self.take = take
        self.notes = []
        self.createdBy = ""
        self.createdOn = None
        self.reviewData = []

        for k, v in kwargs.items():
            setattr(self, k, v)

        if reviewData:
            self._build_review(reviewData)

    def _build_review(self, reviewData):
        """Build a review from the dict provided."""
        for k, v in reviewData.items():
            setattr(self, k, v)

    def add_media(self, path):
        """Add media to this review and move to the publish area."""
        # Move media to publish area
        # Amend DB table to contain path to media for this review
        pass
