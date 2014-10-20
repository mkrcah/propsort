propsort
=====

(THIS PROJECT IS STILL UNDER ACTIVE DEVELOPMENT AND IS NOT COMPLETED YET)

**propsort** is a command-line tool to sort Java/Scala/Play properties file according to a given template. 
It is aimed primarily for files containing language translations. It helps to keep the structure of properties synchronized and to detect missing, duplicated or unused keys among different translations.

### Install
````
pip install propsort
```

### Usage

```
propsort -t template file-to-sort
```

### Example
 
Let's say your English translations are nicely organized in `message_en.properties`:

```
# Email
email.from = hello@example.com
email.subject = Welcome {0}
email.text = This is an email from {0}

# Web
web.header = My website
web.content = Welcome to my website
```

However, German translations `message_de.properties`    are in different order and miss the structure or comments:

```
web.content = Herzlich Willkommen \
		in meiner Website
email.from = hello@example.de
web.header = Meine website
email.subject = Willkomen, {0}
email.text = Dies ist ein E-mail von {0}
```

**propsort** sorts the German translations according to the English template:
```
propsort -t message_en.properties message_de.properties
```
Output:

```
# Email
email.from = hello@example.de
email.subject = Willkomen, {0}
email.text = Dies ist ein E-mail von {0}

# Web
web.header = Meine website
web.content = Herzlich Willkommen \
		in meiner Website
```

### Detecting missing & unused keys

Assume the following Spanish translations `message_es.properties`:

```
yes = sí
no = no
email.from = hola@example.es
email.from = mi@example.de
email.subject = Hola, {0}
web.header = Mi sitio
```

**propsort** identifies missing, unused or duplicated keys and add warnings to the end of the output:

```
propsort -t message_en.properties message_es.properties
```

Output:

```
# Email
email.from = hola@example.es
email.subject = Hola, {0}

# Web
web.header = Mi sitio


##############################################
## Unused keys
##############################################
yes = sí
no = no

##############################################
## Missing keys
##############################################
# web.content
# email.text


##############################################
## Duplicated keys
##############################################
# email.from = mi@example.de
```

### Features

**propsort** fully supports the Properties file format, as specified in the [Java documentation](http://docs.oracle.com/javase/7/docs/api/java/util/Properties.html#load(java.io.Reader)).  This includes:
* Support for **multi-line values** (Yes, double backslashes at the end of a line are interpreted as part of the value, not a line delimiter)
* Support for **all allowed key-value delimiters** (space `key value`, equal-sign `key=value`, double-colon `key:value`)
* Support for **both types of comments** (lines starting with `#` or `!`)
* Support for **crazy key names** like `this\=is\:my\ key = value`. 

### Contributions

Ping me on Twitter ([@mkrcah](https://twitter.com/mkrcah)) if you're having issues or have an idea for improvement. 
Or just submit a PR :)   
	


