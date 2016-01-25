import cPickle as pickle

class GameObject(object):
    def __init__(self, path, cls, args = (), kwargs = {}, autosave = True, new = True):
        if new:
            if hasattr(cls.__init__, "func_code"):
                if "host_object" in cls.__init__.func_code.co_varnames:
                    kwargs["host_object"] = self
            obj = cls.__new__(cls)
        else:
            with open(path, "rb") as f:
                obj = pickle.load(f)
        
        object.__setattr__(self, "auto", autosave)
        object.__setattr__(self, "path", path)
        object.__setattr__(self, "obj", obj)

        if new:
            obj.__init__(*args, **kwargs)

        self.set_object()

    def __getattr__(self, name):
        if object.__getattribute__(self, "obj") is None:
            with open(object.__getattribute__(self, "path"), "rb") as f:
                obj = pickle.load(f)
        else:
            obj = object.__getattribute__(self, "obj")
        return getattr(obj, name)

    def __setattr__(self, name, value):
        if object.__getattribute__(self, "obj") is None:
            with open(object.__getattribute__(self, "path"), "rb") as f:
                obj = pickle.load(f)
        else:
            obj = object.__getattribute__(self, "obj")
        setattr(obj, name, value)
        
        if self.auto:
            with open(object.__getattribute__(self, "path"), "wb") as f:
                pickle.dump(obj, f)

    def __getitem__(self, name):
        if object.__getattribute__(self, "obj") is None:
            with open(object.__getattribute__(self, "path"), "rb") as f:
                obj = pickle.load(f)
        else:
            obj = object.__getattribute__(self, "obj")
        return obj[name]

    def __setitem__(self, name, value):
        if object.__getattribute__(self, "obj") is None:
            with open(object.__getattribute__(self, "path"), "rb") as f:
                obj = pickle.load(f)
        else:
            obj = object.__getattribute__(self, "obj")
        obj[name] = value

        if self.auto:
            with open(object.__getattribute__(self, "path"), "wb") as f:
                pickle.dump(obj, f)

    def __repr__(self):
        if object.__getattribute__(self, "obj") is None:
            with open(object.__getattribute__(self, "path"), "rb") as f:
                obj = pickle.load(f)
        else:
            obj = object.__getattribute__(self, "obj")
        return repr(obj)

    def __str__(self):
        if object.__getattribute__(self, "obj") is None:
            with open(object.__getattribute__(self, "path"), "rb") as f:
                obj = pickle.load(f)
        else:
            obj = object.__getattribute__(self, "obj")
        return str(obj)

    def get_object(self):
        with open(object.__getattribute__(self, "path"), "rb") as f:
            obj = pickle.load(f)
        object.__setattr__(self, "obj", obj)

    def set_object(self, obj = None):
        if obj is None:
            obj = object.__getattribute__(self, "obj")
        with open(object.__getattribute__(self, "path"), "wb") as f:
            pickle.dump(obj, f)
        object.__setattr__(self, "obj", None)

    def __enter__(self):
        self.get_object()
        return self

    def __exit__(self, type, value, traceback):
        self.set_object()
        return False

class GameObjectFactory(object):
    def __init__(self, cls, path, autosave = True):
        self.cls = cls
        self.path = path
        self.auto = autosave

        self.acc = 0

    def __call__(self, *args, **kwargs):
        return GameObject(self.path(self), self.cls, args, kwargs, self.auto)
