
class Stats(object):
    def __init__(self):
        self.skipped = 0
        self.errored = 0
        self.success = 0

    def get_total(self):
        return self.skipped + self.errored + self.success

    def string(self):
        str = """
              Success: {success}
              Skipped: {skipped}
              Errored: {errored}
              Total:   {total}
              """.format(success=self.success, skipped=self.skipped, errored=self.errored, total=self._total())

        return str

    def _total(self):
        return self.success + self.skipped + self.errored