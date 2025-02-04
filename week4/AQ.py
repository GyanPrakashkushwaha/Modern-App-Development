from string import Template

t =Template("I like eating $something and my favorite $something are $lfruits")

s = t.substitute(something = "fruits",lfruits = "Kiwi, Apple, Pear, Grapes")
print(s)


