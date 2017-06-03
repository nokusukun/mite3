from mite3.ElementBuilder import ElementBuilder as Element

class Query():
    query_cache = {}
    cache_proved = {}

    def __init__(self, identifier=None, recache=False):
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

        # cache_proved makes sure that the cache has already been declared
        if not identifier in Query.cache_proved or recache:
            # Generate ID as a variable name for the cache
            # PS. this is the fastest way to do it.
            # see: https://stackoverflow.com/questions/2484156/is-str-replace-replace-ad-nauseam-a-standard-idiom-in-python
            unique = "cache{}".format(identifier).replace("#", "_id").replace(".", "_class").replace("-", "_").replace(" ", "")
            Query.query_cache[identifier] = unique
            self._query = "{unique} = {selector};{unique}".format(unique=unique, selector=self._query)
        else:
            self._query = Query.cache_proved[identifier]
            


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
        self._prove()

    def _prove(self):
        proved = {}
        identifiers = []
        identifiers.extend(Query.query_cache.keys())
        for identifier in identifiers:
            if identifier in self._query:
                proved[identifier] = Query.query_cache.pop(identifier)

        # Moving a cache to proved marks it as active and reuseable. 
        Query.cache_proved.update(proved)



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
