import random
from mite3.Map import Map

"""
    Preface:
        I will rewrite this.
        I am bad at this.
        End me.
"""


class UI():
    inputs = {}
    browser = None
    xj = None
    xf = None
    elements = {}
    get_object = {}

    def __init__(self, mite):
        self.mite = mite
        self.browser = mite.browser
        self.xj = self.mite.xj
        self.xf = self.browser.ExecuteFunction
        self.debug = True

    def element(self, id):
        # Returns an element Object, lets you set stuff.
        return self._UIElement(self, id)


    class _UIElement():
        def __init__(self, UI, id):
            self.id = id
            self.UI = UI
            UI.elements[id] = {}


        def prop(self, prop):
            id_ = "".join([ str(random.randint(0, 9)) for x in range(0, 16) ])
            script = "getcallback('{id_}',$('#{id}').prop(`{prop}`));".format(id=self.id, prop=prop, id_=id_)
            self.UI.xj(script)

            while not id_ in self.UI.mite.callback_result:
                # print(self.UI.mite.callback_result)
                pass

            return self.UI.mite.callback_result[id_]


        def attr(self, attr, value=None):
            # generates a callbackID
            id_ = "".join([ str(random.randint(0, 9)) for x in range(0, 16) ])
            if value is None:
                script = "getcallback('{id_}',$('#{id}').attr(`{prop}`));".format(id=self.id, prop=attr, id_=id_)
            else:
                script = "getcallback('{id_}',$('#{id}').attr(`{prop}`, `{value}`));".format(id=self.id, id_=id_, prop=attr, value=value)

            self.UI.xj(script)

            while not id_ in self.UI.mite.callback_result:
                print(self.UI.mite.callback_result)
                pass 


            return self.UI.mite.callback_result[id_]


        def __getattr__(self, attr):
            if attr == "text":
                attr = "innerHTML"
            return self.prop(attr)
            #return self.UI.elements[self.id][attr]

        def __str__(self):
            return "#"+self.id

        def __setattr__(self, name, value):
            try:
                script = "$('#{id}').prop(`{attr}`,`{value}`);".format(id=self.id, attr=name, value=value)
                self.UI.xj(script)
            except:
                super().__setattr__(name, value)

            # if name == "text":
            #     self.UI.setText(self.id, value)
            #         
            # if name == "value":
            #     self.UI.setValue(self.id, value)