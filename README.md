# README

## NOTES
### Foreign keys
```pyhton
class ModelClass(models.Model):
...
parent = models.ForeignKey('ModelClass')
```

### F-Strings are OP!

./manage.py migrate --run-syncdb