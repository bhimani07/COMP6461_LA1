class BgColor:
    SUCCESS = '\033[92m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'
    ERROR = '\033[91m'

    @staticmethod
    def color_error_wrapper(string):
        return BgColor.ERROR + string + BgColor.ENDC

    @staticmethod
    def color_bold_wrapper(string):
        return BgColor.BOLD + string + BgColor.ENDC

    @staticmethod
    def color_success_wrapper(string):
        return BgColor.SUCCESS + string + BgColor.ENDC
