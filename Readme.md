# simpledict

Makes dict modeling easy for document based databases with minimal extra funcitonality

* Permissioning
* No type system
* No validation
* Minimization of field names
* Python Properties
* One python file
* Doctests

Other libraries that provide this functionality in python

* @j2lab's DictShield - amazing library

# Example

Creating a simple model would involve createing a class that subclasses simpledict.Dictionary
 
    import simpledict

    class Tweet(simpledict.Dictionary):
        field_user = "u"
        field_text = "t"
        
        field_count = "c"
        @property
        def character_count():
            return len(field_text)
        
and then to create the object:

    tweet = Tweet(user="robspychala", text="hey everyone, what's cookin'?")
    
and to serialize to a dictionary
    
    tweet.to_dict()
    

## Minimization
    
If you would like to minimize the field names to what is defined in the field_* values you pass in a minimize=True value to the to_dict() method

    tweet.to_dict(minimize=True)
    
## Properties

If you would like to serialize properties

    tweet.to_dict(properties={"count":None})
    