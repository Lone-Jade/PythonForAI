import re

text = "alpha, beta, gamma, delta, epsilon, zeta"

print(re.split("[,]+", text))
print(re.split("[,]+", text, 2))

pat = "[a-z]+"
print(re.findall(pat, text))

pat = "{name}"
text = "Hello {name}, how are you?"
print(re.sub(pat, "world", text))

s = "a s d"
print(re.sub("a|s|d", "good", s))

s = "It is a very good good idea."
print(re.sub(r"(\b\w+) \1", r"\1", s))
print(re.sub(r"((\w+) )\1", r"\2", s))
