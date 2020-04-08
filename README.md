# Persistables

A persistable is a python class that can be saved to a file in a portable manner, and recreated on demand. This can be useful if you wish to save the state of your code to make errors more reproducible.

## What is a persistable?
Making a persistable class is often as easy as

```python
import persist
class Foo(persist.Persistable):
	pass
```

The class can then be written to disk with
```python
my_foo = Foo()
persist.persist_to_file('state.per', obj=my_foo)
```

and retrieved with

```python
state, meta = persist.restore_from_file('state.per')
my_foo = state['obj']
```

The metadata contains information about the function that called persist_to_file.

## Wait, what do you mean by "often"?
Many classes will be able to be persisted just by sublassing Persistable, but some will not. A class can be persisted if it is composed of one or more of 

* Numbers (ints, floats, complex)
* strings
* Iterables (lists, dicts, etc.)
* Functions
* Nonetypes
* Numpy Arrays
* Pandas Dataframes
* Any object that implements the `to_dict` and `from_dict` methods to descibe how the class can be converted to/from a dictionary of simple data types (i.e anything that can be written to json)

If this is not true of your class, you need to implement a method `to_dict` which converts your class to a dictionary of json compatible types (numbers, strings, lists, and dictionaries). You also need to implement a `from_dict` to convert a dictionary back into a class.

Examples of classes that need to implement their own `to_dict` method are ones that maintain file pointers or network connections. These classes need a way of saving enough infomation about the connection that it can be recreated at a later date.

#### Example

```python
from foobar import ComplicatedThing

# Note: Any class that implements to_dict and from_dict can be
# persisted. It does not need to extend the Persistable class
class Foo():
	def __init__(self, a, b, c):
		self.a = a
		self.complicated_thing = ComplicatedThing(b, c)
		
	def to_dict(self):
		out = dict()
		#This key is required. It is used by persist.py to
		#recreate the object
		out['__class__'] = 'mymodule.submodule.Foo'
		out['a'] = a
		out['b'] = b
		out['c'] = c
		extra = self.complicated_thing.get_internal_variable()
		out['extra'] = extra 
		return out

	@classmethod
	def from_dict(cls, cfg):
		a =  cfg['a']
		b =  cfg['b']
		c =  cfg['c']		
		stuff = cfg['extra']
		
		object = cls(a, b, c)
		object.complicated_thing = ComplicatedThing(b,c)
		object.complicated_thing.set_internal_variable(stuff)
```		
		
	
		

## Limitations
* A class can not be completely persisted if it is composed of a class whose internal state can not be exposed. This is probably a rare occurrence because the state is usually held in the `__dict__` variable

* Pandas series and dataframes can't be properly persisted if some of their columns contain objects. For example

```python
df = pd.DataFrame()
df['date'] = pd.to_daterange("2020-01-01", "2020-12-31")
persist.to_file('state.per', obj=df)
new_df = persist.from_file('state.per')['obj']
type(new_df['date'])
>>> np.int64
```

The datatime type gets persisted as an integer representing the time in milliseconds of unixtime. This is a limitation in pandas I can't figure out how to overcome.

## More examples

```
import persist.funcs

class Foo():
	"""Store and retrive a file with an open file handle"""
	def __init__(self, filename):
    		self.filename = filename
	    	self.file_pointer = open(fp, 'r')
	    	self.seek_pos = 0
    	
   	def to_dict(self):
   		#We can't save the filepointer, but we can save
   		#everything we need to restore the file_pointer
		out = dict()
		out['class'] = 'mymodule.submodule.Foo'
		out['filename'] = self.filename
		out['seek_pos'] = self.seek_pos
 	        return out
       
    def from_dict(cls, cfg):
        _class = persist.funcs.get_class_from_instance_dict(cfg)
        assert _class == cls
        cfg.pop('__class__')

	# Create a Foo() without calling __init__
        obj = cls.__new__(cls)
        obj.filename = cfg['filename']
        obj.seek_pos. = int(cfg['seekpos'])
        obj.file_pointer = open(filename, 'r')
        obj.file_pointer.seek(obj.seek_pos)
        
        #Check that obj is actually persistable
        persist.validate_dict(obj)
        return obj
```
