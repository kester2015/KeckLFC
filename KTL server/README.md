## Generating KTL keywords and linking to the KeckLFC class

### 1. KTL keywords csv file
Fill in the csv file (keywords.csv) with KTL keywords to implement,
run `python write_xml.py` to generate the xml file named LFC.xml.sin

### 2. Implement functions in KeckLFC.py
In `mockKeckLFC.py`, the mockKeckLFC class reads the xml file, stores the keyword names and values as dictionaries in `self.keywords`.
The functions are defined as the same name as the keyword.

``` ruby
def KEYWORD(self, value = None):
    
    if value == None: 
        # This is called when keyword value is read
        return self.keywords['KEYWORD']
    else:
        # This is called when keyword value is being modified
        # do something    
        return 0 # return 0 if successful
```
