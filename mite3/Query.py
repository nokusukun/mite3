from mite3.ElementBuilder import ElementBuilder as Element

class Query():

    def __init__(self, identifier=None):
        self.function = ""
        self._name = ""

        if identifier == "this":
            self._query = "$({0})".format(identifier)
        elif str(identifier).startswith("$"):
            self._query = "$({0})".format(identifier)
        elif str(identifier).startswith("~"):
            self._query = "$({0})".format(identifier[1:])
        elif identifier is None:
            self._query = "$()"
        else:
            self._query = "$('{0}')".format(identifier)

    def magic_smoke(self, *args):
        if len(args) > 0:
            nwarg = []
            for a in args:
                if type(a) is str:
                    try:
                        if a.startswith("function"):
                            nwarg.append(a)
                        elif a[0] == "{" and a[-1:] == "}":
                            nwarg.append('{0}'.format(a))
                        else:
                            nwarg.append('`{0}`'.format(a))
                    except:
                        nwarg.append('`{0}`'.format(a))

                elif type(a) is Element:
                    nwarg.append('`{0}`'.format(str(a)))

                elif type(a) is dict:
                    arg = []
                    for key in a.keys():
                        if type(a[key]) is Query:
                            arg.append("{} : {}".format(key, str(a[key])))
                        else:
                            arg.append("{} : '{}' ".format(key, str(a[key])))
                    arg = "{{{}}}".format(", ".join(arg))
                    nwarg.append(arg)
                else:
                    nwarg.append(str(a))

            # could use just ", ".join(nwarg) itself, but I think it has
            # something to do with the older verion where it's "`{0}`"
            arg = "{0}".format(", ".join(nwarg))
        else:
            arg = ""

        self._query += ".{0}({1})".format(self._name ,arg)
        return self

    

    def execute(self, mite):
        mite.xj(self._query+";")

    def __str__(self):
        return self._query

    def __add__(self, other):
        self._query = self._query + ";" + other._query
        return self

    def __getattr__(self, name):
        if name == "q":
            return self._query

        self._name = name
        return self.magic_smoke


    @staticmethod
    def event_compile(function, args=[]):
        """
            compile - converts python fucntion into a javascript function
            @function = python function/event
            @args = tuple of events
        """
        if len(args) > 0:
            compiled_arg = ", ".join([ '"{}"'.format(x) for x in args])
        else:
            compiled_arg = ""

        compiled = "{}({})".format(function.__name__, compiled_arg)
        return compiled
