from mite3.Map import Map

class ElementBuilder():

    def __init__(self, element, **prop):
        self.element = element
        self._property = ""
        self.properties = Map({})
        self.innerHTML = ""
        self.suf = []
        if "c" in prop:
            prop["class"] = prop.pop("c")
        if "_class" in prop:
            prop["class"] = prop.pop("_class")

        if "_for" in prop:
            prop["for"] = prop.pop("_for")

        for x in prop.keys():
            self._property = x
            self.magic_smoke(prop[x])

        # self.property.update(prop)

    def get(self, prop):
        return self.properties[prop]

    def magic_smoke(self, arg, append = False):
        if self._property == "text" or self._property == "inner":
            if append:
                self.innerHTML += str(arg)
            else:
                self.innerHTML = str(arg)
        else:
            if append:
                if self._property in self.properties:
                    self.properties[self._property] += " " + arg
                else:
                    self.properties[self._property] = arg
            else:
                self.properties[self._property] = arg

        return self

    def __str__(self):
        return self.html

    def __add__(self, other):
        self.suf.append(other)
        return self

    def __getattr__(self, property):

        if property == "html":
            props = " ".join(["{0}='{1}'".format(x.replace("_", "-"), self.properties[x]) for x in self.properties.keys()])
            build = "<{0} {1}>{2}</{0}>".format(self.element, props, self.innerHTML)
            build += "".join([x.html if type(x) == ElementBuilder else x for x in self.suf])
            return build

        self._property = property

        if property == "_class" or property == "c":
            self._property = "class"

        if property == "_for":
            self._property = "for"

        return self.magic_smoke