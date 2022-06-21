# ceaserSalad
A simple but powerful ceaser cipher with varying shift margin based on cyclic passphrase iteration.
The algorithm can also be performed on pen and paper.

```python
from main import engine

cs = engine()
plainText = "This is a secret message"
password = "secret"
cipher = cs.encrypt(plainText, password)
plainAgain = cs.decrypt(cipher, password)

# test
print(plain, cipher, plainAgain)
```
