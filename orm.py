from inspect import Signature, Parameter
from collections import OrderedDict
from databases import Database


def make_signature(names):
    return Signature(
        Parameter(name, Parameter.POSITIONAL_OR_KEYWORD)
        for name in names)


class Descriptor:
    def __init__(self, name=None):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class Typed(Descriptor):
    ty = object

    def __set__(self, instance, value):
        if not isinstance(value, self.ty):
            raise TypeError('Expected %s' % self.ty)
        super().__set__(instance, value)


class Integer(Typed):
    ty = int


class Float(Typed):
    ty = float


class String(Typed):
    ty = str


class Insert:
    def __new__(cls, clsname, clsdict):
        table_name = clsname.__name__
        table_rows = tuple(clsdict.keys())
        q_marks = ', '.join(['?'] * len(table_rows))
        query = 'INSERT INTO %s%s values(%s)' % (
            table_name,
            table_rows,
            q_marks)
        return Database.execute(query, *list(clsdict.values()))


class Select:
    def __init__(self, cls, kwargs):
        self.cls = cls
        self.kwargs = kwargs

    def __new__(cls, clsname, clsdict):
        table_name = clsname.__name__
        table_rows = tuple(clsdict.keys())
        query_args = list(clsdict.values())
        where_keys = [key+' = ?' for key in clsdict.keys()]
        query_where = 'where ' + ' and '.join(where_keys) if len(where_keys) > 0 else ''
        query = 'SELECT * FROM %s %s' % (
            # table_rows,
            table_name,
            query_where,
        )
        return Database.execute(query, *query_args).fetchall()


class NoDupOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if key in self:
            raise NameError('%s already defined' % key)
        super().__setitem__(key, value)


class StructMeta(type):
    @classmethod
    def __prepare__(cls, name, bases):
        return NoDupOrderedDict()

    def __new__(cls, clsname, bases, clsdict):
        _fields = [key for key, val in clsdict.items()
                   if isinstance(val, Descriptor)]
        for name in _fields:
            clsdict[name].name = name

        clsobj = super().__new__(cls, clsname, bases, dict(clsdict))
        sig = make_signature(_fields)
        setattr(clsobj, '__signature__', sig)
        return clsobj


class Structure(metaclass=StructMeta):
    # _fields = []

    @classmethod
    def create(cls, *args, **kwargs):
        bound = cls.__signature__.bind(*args, **kwargs)
        for name, val in bound.arguments.items():
            setattr(cls, name, val)

    @classmethod
    def select(cls, **kwargs):
        for row in Select(cls, kwargs):
            setattr(cls, 'id', row[0])
            cls.create(*row[1:])
            yield cls

    @classmethod
    def insert(cls, **kwargs):
        cls.create(*list(kwargs.values()))
        return Insert(cls, kwargs)
