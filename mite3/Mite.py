from cefpython3 import cefpython as cef
from decorator import decorator
from mite3.Map import Map
import time
import sys
import win32gui
import time
import inspect
import asyncio
import threading
import enum
import random
import os

# Patched Javascript Bindings to allow uninitalized classes to be used as a function
class PatchedBinder(cef.JavascriptBindings):

    def SetProperty(self, name, value):
        allowed = self.IsValueAllowedRecursively(value) # returns True or string.
        if allowed is not True:
            raise Exception("JavascriptBindings.SetProperty() failed: name=%s, "
                            "not allowed type: %s (this may be a type of a nested value)"
                            % (name, allowed))

        valueType = type(value)
        if PatchedBinder.IsFunctionOrMethod(valueType):
            self.functions[name] = value
        else:
            self.properties[name] = value

    @staticmethod
    def IsFunctionOrMethod(valueType):
        
        if ('function' in str(valueType) or 'method' in str(valueType) or'type' in str(valueType) or 'Event' in str(valueType)):
            return True
        return False

    @staticmethod
    def IsValueAllowedRecursively(value, recursion=False):
        # When making changes here modify also Frame.SetProperty() as it
        # checks for FunctionType, MethodType.
        valueType = type(value)
        valueType2 = None
        key = None

        if valueType == list:
            for val in value:
                valueType2 = JavascriptBindings.IsValueAllowedRecursively(val, True)
                if valueType2 is not True:
                    return valueType2.__name__
            return True
        elif valueType == bool:
            return True
        elif valueType == float:
            return True
        elif valueType == int:
            return True
        elif 'Event' in str(valueType):
            return True
        elif valueType == type(None):
            return True
        elif PatchedBinder.IsFunctionOrMethod(valueType):
            if recursion:
                return valueType.__name__
            else:
                return True
        elif valueType == dict:
            for key in value:
                valueType2 = JavascriptBindings.IsValueAllowedRecursively(value[key], True)
                if valueType2 is not True:
                    return valueType2.__name__
            return True
        elif valueType == str or valueType == bytes:
            return True
        elif valueType == tuple:
            return True
        else:
            return valueType.__name__



class LoadHandler(object):
    finished = False
    def OnLoadingStateChange(self, browser, is_loading, **_):
        """Called when the loading state has changed."""
        if not is_loading:
            # Loading is complete. DOM is ready.
            if not self.finished:
                browser.ExecuteJavascript("preReadyInit();");
                browser.ExecuteJavascript("miteUIOnReady();");
                #Ensures that this doesn't get loaded again.
                self.finished = True



# This is an event object, please don't touch this.
# This gets called by the cef browser.
# P.S. I don't know what im doing.
# P.S. I don't know what im doing.
# P.S. I don't know what im doing.
class Event():
    mite = None
    function = None
    def __init__(self, *fargs):
        # P.S. I don't know what im doing.
        self.mite.pbug("Event {} called. Args: {}".format(self.function.__name__, fargs))
        
        # I know, this is not how you should be doing it. But im out of ideas.
        # I just want to run events concurrently. (´；д；`)
        # inb4 never touch programming again
        if self.function.__name__ == "getcallback":
            threading.Thread(target=self.function, args=fargs).start()
            self.mite.pbug("Special Event {} ended".format(self.function.__name__))
        else:
            coro = getattr(self.mite, self.function.__name__)(*fargs)
            event = asyncio.run_coroutine_threadsafe(coro, self.mite.event_loop)
            threading.Thread(target=event.result).start()
            self.mite.pbug("Event {} ended".format(self.function.__name__))


        # Legacy Stuff everything is asyncio now.
        """
        if self.async:
            threading.Thread(target=self.function, args=fargs).start()
        else:
            self.function(*fargs)
        """


class Mite():
    j_funcs  = []
    j_obj    = []
    j_prop   = []
    debug = True
    synchronized = []
    _exit_func = None
    _before_init = None
    event_loop = None
    callback_result = {}

    def __init__(self, **settings):
        self.event_loop = asyncio.get_event_loop()
        self.pbug("Initalizing mitemite")
        sys.excepthook = cef.ExceptHook
        self.pbug("init done")


    def run(self, **settings):
        self.pbug("init0")

        cef_settings = settings["cef_settings"] if "cef_settings" in settings else {}
        cef.Initialize(settings=cef_settings)
        if "url" in settings:
            url = settings["url"]
        else:
            raise ValueError("URL is not defined")

        title = settings["title"] if "title" in settings else "Mite3 App"

        self.event_loop = settings["event_loop"] if "event_loop" in settings else self.event_loop

        # browser initalization
        window = cef.WindowInfo()
        if "window" in settings:
            window.windowRect = settings["window"]

        if url != "":
            if not url[1:3] == ":\\":
                pre = "\\" if url[0] == "" else "\\"
                url = os.getcwd() + pre + url

        self.pbug("Load UI > {}".format(url))
        self.browser = cef.CreateBrowserSync(url=url,
                                    window_title=title,
                                    window_info=window)

        handle = self.browser.GetWindowHandle()
        if "window" in settings:
            self.pbug("Resizing UI")
            self.resizeWindow(window.windowRect[0], 
                            window.windowRect[1], 
                            window.windowRect[2], 
                            window.windowRect[3])

        self.pbug("Attaching Handler")
        self.browser.SetClientHandler(LoadHandler())
        self.pbug("App Started")
        threading.Thread(target=self.event_loop.run_forever).start()
        self.start()
        self.close()
        



    def start(self):
            
        self.pbug("Starting Application".format())
        self.j_funcs.append({"name": "miteErrorCallback", "function": self.javascriptErrorCallback, "async": False})
        self.j_funcs.append({"name": "preReadyInit", "function": self.preReadyInitalize, "async": False})
        self.j_funcs.append({"name": "getcallback", "function": self.getcallback, "async": True})
        self.pbug("Appending Javascript Functions...".format())
        self._bindJS()
        self.pbug("Window Initalized")
        cef.MessageLoop()
        cef.Shutdown()
        if self._exit_func is not None:
            self._exit_func()

    def close(self):
        self.event_loop.stop()
        self.event_loop.close()
        self.pbug("App Exited")



    async def preReadyInitalize(self):
        """
            preReadyInitalize = Gets Executed before the app gets ready and 
                executes any onReady functions.
        """
        # TODO: Change/Add this
        # self.xj('document.head.appendChild(`<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>`)')
        
        # Execute preinit code
        if self._before_init is not None:
            self._before_init()

        self._bindJS()

        self.pbug("Pre Ready Initalization")
        self.xj("window.onerror = miteErrorCallback")
        for funcs in self.j_funcs:
            if "bind" in funcs:
                    for bind in funcs["bind"]:
                        self.pbug("Binding {0} function to #{1}".format(bind, funcs["name"]))
                        script = "$('#{0}').attr('{1}', '{2}()');".format(bind, funcs["event"], funcs["name"])
                        self.xj(script)
        self.pbug("Mite Load Finished")



    def pbug(self, args):
        if len(args) > 10000:
            args = args[0:10000] + "..."
        real_arg = ""
        for char in args:
            try:
                char.encode('cp932')
                real_arg += char
            except:
                pass 

        class bcolors:
            HEADER =    '\033[95m'
            OKBLUE =    '\033[94m'
            OKGREEN =   '\033[92m'
            WARNING =   '\033[93m'
            FAIL =      '\033[91m'
            ENDC =      '\033[0m'
            BOLD =      '\033[1m'
            UNDERLINE = '\033[4m'
        if self.debug:
            print("{0}[{a}.{b}]{1}{c}{2}".format(bcolors.HEADER, bcolors.OKBLUE, bcolors.ENDC,
                a=inspect.stack()[2][3],b=inspect.stack()[1][3], c=real_arg))

    async def javascriptErrorCallback(self, error, url, line, five, six):
        class bcolors:
            HEADER = '\033[95m'
            OKBLUE = '\033[94m'
            OKGREEN = '\033[92m'
            WARNING = '\033[93m'
            FAIL = '\033[91m'
            ENDC = '\033[0m'
            BOLD = '\033[1m'
            UNDERLINE = '\033[4m'
        print("{0}[mite.js.{a}]{1}{c} | {five} | {six}{2}".format(bcolors.FAIL, bcolors.WARNING, bcolors.ENDC,
                                                a=line, c=error, five=five, six=six))
    

    def getcallback(self, id, var):
        # this is actually the newer callback.
        print("{} Callback Value: {}".format(id, var))
        self.callback_result[id] = var
        print(self.callback_result)


    def xj(self, script):
        """
            xj =  Executes a javascript file
            script = The javascript in string format.
        """
        self.pbug("Executing > {0}".format(script))
        script = "try {{ {0} }} catch(e) {{ miteErrorCallback(String(e), e, 'execute', '', '');}}".format(script)
        return self.browser.ExecuteJavascript(script)


    def resizeWindow(self, left, top, right, bottom):
        handle = self.browser.GetWindowHandle()
        win32gui.MoveWindow(handle, left, top, right, bottom, True)



    def _bindJS(self):
        """
            _bindJS    = Internal function to bind the app functions to
                            the HTML elements.
        """
        # Loads the javascript bindings
        bindings = PatchedBinder(
            bindToFrames=False, bindToPopups=False)

        for funcs in self.j_funcs:

            # Create an new Event Instance for thread creation
            event = type("Event_{}".format(funcs["name"]), (Event,), {})
            event.function = funcs["function"]
            event.mite = self

            self.pbug("Binding {0} to {1}".format(funcs["name"], funcs["function"]))
            bindings.SetFunction(funcs["name"], event)

        for obj in self.j_obj:
            self.pbug("Loading {1} as {0}".format(obj["name"], obj["function"]))
            bindings.SetObject(obj["name"], obj["function"])

        self.browser.SetJavascriptBindings(bindings)


    #shortform access to reserve the function names

    # DECORATORS #
    def event(bind=None, event="onclick"):
        """
            jFucntion   = decorator to expose functions to the GUI
            --params--
                bind    = ID of the HTML Element
                event   = type of event the function will trigger.
                            Defaults to onclick

            Leaving the parameters empty just exposes it in 
                the javascript engine.
        """
        # f is the function

        def deco(f):
            # Im so sorry
            # if not inspect.iscoroutinefunction(f):
            #     raise Exception("Function '{}' is not a coroutine".format(f.__name__))

            nonlocal bind, event
            function = {"name": f.__name__, "function": f}
            
            # binds event to an html element
            if bind is not None:
                Mite.pbug(Mite, "Bind to: {0}".format(bind))
                if not isinstance(bind, list):
                    bind = [bind]

                new_bind = []
                for b in bind:
                    if b.startswith("#"):
                        new_bind.append(b[1:])
                    else:
                        new_bind.append(b)


                function["bind"] = new_bind
                function["event"] = event

            Mite.pbug(Mite, "FunctionBind: {}".format(function))
            # self.events[function["name"]] = f
            Mite.j_funcs.append(function)
            return f

        return deco


    # DECORATOR #
    def on_ready():

        def deco(f):
            Mite.j_funcs.append({"name": "miteUIOnReady", "function": f, "async": True});
            return f
        return deco

    def before_init():
        def deco(f):
            Mite._before_init = f
            return f
        return deco

    def on_exit():

        def deco(f):
            Mite._exit_func = f
            return f
        return deco

    # DECORATOR #
    def jObject(self, f):
        Mite.j_obj.append({"name": f.__name__, "function": f});
        return f


    # Events shortform
    # It's here cause it can't find the events if it's place up there.
    on = Map({
        "ready": on_ready,
        "exit": on_exit,
        "event": event,
        "preinit": before_init
        })