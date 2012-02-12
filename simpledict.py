"""Provides a way to serialize and deserialize Python class objects to 
dictionaries. Also allows for minimization of dictionary key fields.
"""
__author__ = "Robert Spychala"

import json
import datetime
import types

json_date_handler = lambda obj: obj.strftime('%Y-%m-%dT%H:%M:%S') if isinstance(obj, datetime.datetime) else None

class Dictionary:
  """
  This is the "simpledict" module.
  
  to test on command line: python -m doctest -v simpledict.py

  >>> class Test(Dictionary): field_title = "t"; field_author = "a";
  >>> minimized_data = {"t": "This is the title of the book 1", "a": "And the author 1"}
  >>> normal_data = {"title": "This is the title of the book 2", "author": "And the author 2"}
  
  Create the object from a "minimized" dictionary that has been minimized
  >>> test_obj_from_minimized = Test(**minimized_data)
  >>> test_obj_from_minimized['title']
  'This is the title of the book 1'
  >>> test_obj_from_minimized['t']
  'This is the title of the book 1'
  >>> test_obj_from_minimized.title
  'This is the title of the book 1'
  >>> test_obj_from_minimized['title'] = 'This is the ammended title of the book 1'
  >>> test_obj_from_minimized.title
  'This is the ammended title of the book 1'
  >>> test_obj_from_minimized['title']
  'This is the ammended title of the book 1'
  >>> test_obj_from_minimized['t']
  'This is the ammended title of the book 1'
  >>> test_obj_from_minimized['t'] = 'This is the title of the book 1'
  >>> test_obj_from_minimized.title
  'This is the title of the book 1'
  >>> test_obj_from_minimized.author
  'And the author 1'
  
  Create the object from a "normal" dictionary which has not been minized
  >>> test_obj_from_normal = Test(**normal_data)
  >>> test_obj_from_normal.title
  'This is the title of the book 2'
  >>> test_obj_from_normal.author
  'And the author 2'
  
  Get dict back from object that was created from minimized data
  >>> ret = test_obj_from_minimized.to_dict()
  >>> ret == {'a': 'And the author 1', 't': 'This is the title of the book 1'}
  True
  >>> ret = test_obj_from_minimized.to_dict(minimize=False)
  >>> ret == {'author': 'And the author 1', 'title': 'This is the title of the book 1'}
  True
  
  Get dict back from object that was created from normal data
  >>> ret = test_obj_from_normal.to_dict()
  >>> ret == {'a': 'And the author 2', 't': 'This is the title of the book 2'}
  True
  >>> ret = test_obj_from_normal.to_dict(minimize=False)
  >>> ret == {'author': 'And the author 2', 'title': 'This is the title of the book 2'}
  True
  
  Test ValueError when field_ varaibles are not passed in
  >>> test_failure = Test(title="Book title", author="Author", year_written=1992)
  Traceback (most recent call last):
      ...
  ValueError: field_year_written class variables missing in your Dictionary subclass
  
  
  Test data with _id field
  >>> minimized_data_with_id = {"_id": 1234, "t": "This is the title of the book 1", "a": "And the author 1"}
  >>> test_obj_from_minimized_data_with_id = Test(**minimized_data_with_id)
  >>> test_obj_from_minimized_data_with_id._id
  1234
  >>> test_obj_from_minimized_data_with_id_dict = test_obj_from_minimized_data_with_id.to_dict(minimize=True)
  >>> test_obj_from_minimized_data_with_id_dict == {'a': 'And the author 1', 't': 'This is the title of the book 1', '_id': 1234}
  True
  
  Test Embedded classes
  >>> class EmbeddedInnerTest(Dictionary): field_title = "t"; field_page = "p";
  >>> class EmbeddedTest(Dictionary): field_title = "t"; field_author = "a"; field_toc = ("o", list, EmbeddedInnerTest);
  >>> embedded_data = { 'title': "Embedded Title", 'author': "Embedded Author", 'toc': [{'t':'Chapter One', 'p': 100}, {'t':'Chapter Two', 'p': 201}]}
  >>> embedded_obj = EmbeddedTest(**embedded_data)
  >>> embedded_obj.title
  'Embedded Title'
  >>> embedded_obj.author
  'Embedded Author'
  >>> embedded_obj.toc[0].title
  'Chapter One'
  >>> embedded_obj.toc[1].title
  'Chapter Two'
  >>> embedded_obj.toc[1].page
  201
  >>> embedded_data_2 = embedded_obj.to_dict(minimize=False)
  >>> embedded_data_2 == {'toc': [{'page': 100, 'title': 'Chapter One'}, {'page': 201, 'title': 'Chapter Two'}], 'author': 'Embedded Author', 'title': 'Embedded Title'}
  True
  >>> embedded_data_2 = embedded_obj.to_dict(minimize=True)
  >>> embedded_data_2 == {'a': 'Embedded Author', 't': 'Embedded Title', 'o': [{'p': 100, 't': 'Chapter One'}, {'p': 201, 't': 'Chapter Two'}]}
  True
  >>> toc2 = [EmbeddedInnerTest(title="Chapter Uno", page=123)]
  >>> embedded2_data = EmbeddedTest(title="Hi", author="John", toc=toc2)
  >>> embedded2_data_dict = embedded2_data.to_dict(minimize=False)
  >>> embedded2_data_dict == {'toc': [{'page': 123, 'title': 'Chapter Uno'}], 'title': 'Hi', 'author': 'John'}
  True
  
  Test property
  >>> class PropertyTest(Dictionary):
  ...   field_title = "t"
  ...   field_secret = "s"
  ...   field_taco = "m"
  ...   @property
  ...   def taco(self):
  ...     return "bell"
  ...
  >>> prop_test1 = PropertyTest(title="cheese", secret="pass")
  >>> prop_test1.title
  'cheese'
  >>> prop_test1.secret
  'pass'
  >>> prop_dict_test1 = prop_test1.to_dict(minimize=False, properties={"taco":None}, omit_fields={"secret":None})
  >>> prop_dict_test1["taco"]
  'bell'
  >>> prop_dict_test1["title"]
  'cheese'
  >>> prop_dict_test1.get("secret")
  
  >>> prop_dict_test2 = prop_test1.to_dict(minimize=True, properties={"taco":None}, omit_fields={"secret":None})
  >>> prop_dict_test2["m"]
  'bell'
  >>> prop_dict_test2["t"]
  'cheese'
  >>> prop_dict_test2 == {'m': 'bell', 't': 'cheese'}
  True
  >>> class PropertyEmbeddedTest2(Dictionary):
  ...   field_title = "t";
  ...   field_title_length ="tl"
  ...   @property
  ...   def title_length(self):
  ...     return len(self.title)
  >>> class PropertyTest2(Dictionary):
  ...   field_titles = ("t", list, PropertyEmbeddedTest2)
  ...   field_secret = "s"
  ...   field_taco = "m"
  ...   
  ...   @property
  ...   def taco(self):
  ...     return "bell"
  ...
  >>> prop_dict_test3 = PropertyTest2(titles=[PropertyEmbeddedTest2(title="XoXoXo"), PropertyEmbeddedTest2(title="YoYo")], secret="my secret")
  >>> ret = prop_dict_test3.to_dict(properties={"titles":{'title_length':None}})
  >>> ret == {'s': 'my secret', 't': [{'tl': 6, 't': 'XoXoXo'}, {'tl': 4, 't': 'YoYo'}]}
  True
  >>> class SingleEmbeddedTest1(Dictionary):
  ...   field_pizza = "p"
  ...   field_burger = "b"
  >>> class SingleTest1(Dictionary):
  ...   field_lunch = ("l", SingleEmbeddedTest1)
  ...   field_title = "t"
  ...
  >>> prop_single_dict_test = SingleTest1(title="things i eat", lunch=SingleEmbeddedTest1(pizza="of course", burger="on fridays"))
  >>> prop_single_dict_test.title == "things i eat"
  True
  >>> prop_single_dict_test.lunch != None
  True
  >>> prop_single_dict_test.lunch.pizza == "of course"
  True
  >>> ret = prop_single_dict_test.to_dict()
  >>> ret == {'l': {'p': 'of course', 'b': 'on fridays'}, 't': 'things i eat'}
  True
  >>> prop_single_dict_test_obj = SingleTest1(**{'l': {'p': 'of course', 'b': 'on fridays'}, 't': 'things i eat'})
  >>> prop_single_dict_test_obj.title == prop_single_dict_test.title
  True
  >>> prop_single_dict_test_obj.lunch.pizza == prop_single_dict_test.lunch.pizza
  True
  >>> prop_single_dict_test_obj.lunch.burger == prop_single_dict_test.lunch.burger
  True
  >>> prop_single_dict_test_obj.lunch.burger == prop_single_dict_test.lunch.pizza
  False
  """
  
  def __init__(self, **entries):
    fields_minimized_map = self._get_fields_map(minimize_id_key=True)
    if "_id" in entries:
       setattr(self, "_id", entries["_id"])
       del entries["_id"]
    if not set(entries.keys()) <= set([value[0] for value in fields_minimized_map.values()]) and not set(entries.keys()) <= set(fields_minimized_map.keys()):
      missing =  set(entries.keys()) - set([value[0] for value in fields_minimized_map.values()]) | set([fields_minimized_map[min_key] for min_key in (set(entries.keys()) - set(fields_minimized_map.keys())) if fields_minimized_map.has_key(min_key)])
      raise ValueError("field_%s class variables missing in your Dictionary subclass" % (" field_".join(missing)) )
      pass
    map(lambda name: setattr(self, fields_minimized_map[name][0], entries[name]), [name for name in entries if name in fields_minimized_map])
    map(lambda name: setattr(self, name, entries[name]), [name for name in entries if name not in fields_minimized_map])
    for key in self.__dict__:
      if key == "_id":
        continue
      value = getattr(self, key)
      key_metadata = fields_minimized_map[self._get_minimized_name(key)]
      if len(key_metadata) == 3:
        if isinstance(value, key_metadata[1]):
          if len(value) > 0 and not isinstance(value[0], key_metadata[2]):
            setattr(self, key, [key_metadata[2](**obj) for obj in self.__dict__[key]]);
        else:
          raise ValueError("%s type mis match; expecting %s for %s and got %s" % (self.__class__.__name__, key_metadata, key, value))
      elif len(key_metadata) == 2 and not isinstance(value, key_metadata[1]):
        setattr(self, key, key_metadata[1](**self.__dict__[key]))
        
  def to_dict(self, minimize=True, strip_none=False, properties={}, omit_fields={}):
    def get_value(type_description, value, name):
      if isinstance(value, types.ListType):
        return [val.to_dict(minimize=minimize, properties=properties.get(name, {}), omit_fields=omit_fields.get(name, {})) for val in value]
      elif isinstance(value, types.InstanceType):
        return value.to_dict(minimize=minimize, properties=properties.get(name, {}), omit_fields=omit_fields.get(name, {}))
      else:
        return value
    def omit(name):
      if name in omit_fields.keys() and not isinstance(omit_fields[name], types.DictType) or strip_none and not full_dict[name]:
        return True
      return False
    fields_map = self._get_fields_map(minimize_id_key=False)
    fields_map.update({"_id": ("_id",)})
    full_dict = dict((prop, getattr(self,prop)) for prop in properties)
    full_dict.update(self.__dict__)
    fields_map.update(dict((key, (None,)) for key in full_dict.keys() if key not in fields_map))
    if minimize:
      return dict((fields_map[name][0], get_value(fields_map[name], full_dict[name], name)) for name in full_dict if not omit(name))
    else:
      return dict((name, get_value(fields_map[name], full_dict[name], name)) for name in full_dict if not omit(name))
    
  def _get_custom_type(self, name):
    value = getattr(self, "field_" + name)
    if isinstance(value, types.TupleType) and len(value) == 3:
      return value[1]
    if isinstance(value, types.TupleType) and len(value) == 2:
      return value[1]
    else:
      return None
                
  def _get_minimized_name(self, name):
    value = getattr(self, "field_" + name)
    if isinstance(value, types.TupleType):
      return value[0]
    elif isinstance(value, types.StringTypes):
      return value
    else:
      return value[0]
          
  def _get_fields_map(self, minimize_id_key=True):
    def get_dict_values(name,  value):
      if isinstance(value, types.TupleType):
        if minimize_id_key:
          a = [name]
          a.extend(value[1:])
          return (value[0], tuple(a))
        else:
          return (name, value)
      elif isinstance(value, types.StringTypes):
        if minimize_id_key:
          return (value, (name,))
        else:
          return (name, (value,))
      else:
        raise ValueError("field %s can only be of type tupule or str, found %s" % (name, value))
    return dict(get_dict_values(name[6:], getattr(self, name)) for name in dir(self) if name.startswith('field_') and not callable(getattr(self, name)))
    
  def __setitem__(self, key, value):
    fields_minimized_map = self._get_fields_map(minimize_id_key=True)
    if fields_minimized_map.has_key(key):
      key = fields_minimized_map[key][0]
    setattr(self, key, value)
      
  def __getitem__(self, key):
    fields_minimized_map = self._get_fields_map(minimize_id_key=True)
    if fields_minimized_map.has_key(key):
      key = fields_minimized_map[key][0]
    return getattr(self, key)
    
def to_json(obj, minimize=True):
  return json.dumps(obj.to_dict(minimize=minimize), default=json_date_handler)
