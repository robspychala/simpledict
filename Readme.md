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
* No validation

Other libraries that provide this functionality and more in python

* []@j2lab's](http://twitter.com/j2labs) [DictShield](../../j2labs/DictShield) - amazing library

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

    minimized_tweet_data = tweet.to_dict(minimize=True)
    
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
    
    
# License

The simpledict component is released under the MIT License.

The MIT License (MIT) Copyright (c) 2012 Robert Spychala

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.