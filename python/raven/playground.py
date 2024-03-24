
import tldextract

list = tldextract.extract('http://www.google.co.in/about')

domain_name = list.domain + '.' + list.suffix

print(domain_name)
