# XSS Finder
A Python script for crawling a website to extract GET parameters from links and testing whether those parameters are reflected in the page content, which could potentially indicate a vulnerability to Cross-Site Scripting (XSS) attacks.

# Features
- Crawl a given URL and extract all GET parameters from links on the page.
- Optionally test whether the extracted parameters are reflected in the page's response.
- Easily toggle between functionality using command-line arguments.

# Requirements
Ensure you have Python 3.x installed along with the required dependencies.

# Install Dependencies
Install the required libraries using pip:
```bash
pip install -r requirements.txt
```

# Usage
Run the Script
```bash
python finder.py [--reflected]
```

# Options
- --reflected: Enable reflection testing to check if GET parameters are reflected in the page.

# Example
### Crawl and Extract GET Parameters Only:
```bash
python finder.py
```
input:
```bash
Enter target URL: https://example.com
```
Output:
```bash
Crawling https://example.com for GET parameters...

Found URLs with GET parameters:
URL: https://example.com/page?param1=value1&param2=value2
  - Parameter: param1, Value(s): ['value1']
  - Parameter: param2, Value(s): ['value2']
```

### Crawl and Test for Reflected Parameters:
```bash
python finder.py --reflected
```
Input:
```bash
Enter target URL: https://example.com
```
Output:
```bash
Crawling https://example.com for GET parameters...

Found URLs with GET parameters that are reflected:
[!] Parameter 'param1' is reflected on the page.
Tested URL: https://example.com/page?param1=test_param1_1234&param2=value2

[ ] Parameter 'param2' is not reflected.
```

# Limitations

- Does not currently handle JavaScript-generated content or dynamically loaded links.
- Only tests for reflected parameters; additional validation is required for identifying full XSS vulnerabilities.
- Assumes all pages return HTML; may not work correctly with APIs or other content types.