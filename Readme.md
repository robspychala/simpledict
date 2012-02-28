# simpledict

Makes dict modeling easy for document based databases with minimal extra funcitonality

* Permissioning
* Embedded documents
* Minimization of field names
* Python Properties
* One python file
* Doctests - functionality is unit tested

Missing features

* No type system
* No validation - up to you as the developer to add it.

Other libraries that provide this functionality and more in python

* [@j2lab's](http://twitter.com/j2labs) [DictShield](../../j2labs/DictShield) - great library with a type system and more

# Installation

Easiest way to install is from PyPI

```pip install simpledict```

# Example

Creating a simple model would involve creating a Class that subclasses simpledict.Dictionary

```python
import simpledict

class Tweet(simpledict.Dictionary):
  field_user = "u"
  field_text = "t"
  field_count = "c"
  @property
  def character_count():
    return len(self.text)
```

and then to create the object:

```python
tweet = Tweet(user="robspychala", text="hey everyone, what's cookin'?")
```

and to serialize to a dictionary

```python
tweet_data = tweet.to_dict()
```

and of course to de-serialize back to an object, you'd

```python
tweet = Tweet(**tweet_data)
```

## Minimization

If you would like to minimize the field names to what is defined in the field_* values you pass in a minimize=True value to the to_dict() method

```python
minimized_tweet_data = tweet.to_dict(minimize=True)
```
    
and even if you have minimized data, you'd still be able to de-serialize it to a dictionary, ex:

```python
minimized_tweet = Tweet(**minimized_tweet_data)

assert(tweet.title == minimized_tweet.title, tweet.user == minimized_tweet.user)
```

## Properties

If you would like to serialize properties

```python
tweet_data_props = tweet.to_dict(properties={"count":None})

assert(tweet_data_props["count"] == tweet.count)
```
    
## Permissioning

And if you don't want to show the user, for whatever reason you'd use the omit_fields option

```python
tweet_data = tweet.to_dict(omit_fields={"user":None})

assert(not tweet_data.has_key("user"))
```

### Embedded Documents

```python
import simpledict

class UserSettings(Dictionary):
    field_color = "c"
    field_size = "s"
    
class User(Dictionary):
    field_settings = ("s", UserSettings)
    field_name = "n"

user = User(name="Price", settings=UserSettings(color="purple", size="medium"))
```

### array of Embedded Documents

```python
import simpledict

class EmbeddedInnerTest(simpledict.Dictionary):
    field_title = "t"
    field_page = "p"
    
class EmbeddedTest(simpledict.Dictionary):
    field_title = "t"
    field_author = "a"
    field_toc = ("o", list, EmbeddedInnerTest)
    
embedded_data = { 'title': "Embedded Title", 'author': "Embedded Author", 
                    'toc': [{'t':'Chapter One', 'p': 100}, {'t':'Chapter Two', 'p': 201}]}
embedded_obj = EmbeddedTest(**embedded_data)
embedded_obj.title
embedded_obj.author
embedded_obj.toc[0].title
embedded_obj.toc[1].title
embedded_obj.toc[1].page
```


### MongoDB example

```python
import simpledict
import pymongo

from pymongo import Connection
connection = Connection()
db = connection.main_database

class User(simpledict.Dictionary):

  field_email = "e"
  field_password = "p"

  def insert(self):
    if not db or not self.email or not self.password:
      raise Exception()
    db[self.__class__.__name__.lower()].insert(self.to_dict(minimize=True))
    return self
```

and then to use this User class in your app and insert into a mongodb, it would involve

```python
entry = model.User(email="robspychala@gmail.com",
                    password="mysekr3t").insert()
entry_dict = entry.to_dict(minimize=False)
self.response.out.write(json.dumps({'success': True, 'result': entry_dict}, 
                            default=simpledict.json_date_handler))
```


# License

The simpledict component is released under the MIT License.

The MIT License (MIT) Copyright (c) 2012 Robert Spychala

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.