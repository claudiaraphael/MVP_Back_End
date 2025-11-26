from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  data_model import Base


def add_comment(self, comment:Comment):
    """ Adiciona um novo comentário ao Product
    """
    self.comments.append(comment)