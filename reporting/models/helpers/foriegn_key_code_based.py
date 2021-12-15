from django.db import models


class ForeignKeyCodeBased(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        super(ForeignKeyCodeBased, self).__init__(*args, **kwargs)

    def get_attname(self):
        return "%s_code" % self.name
