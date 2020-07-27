import os
import sys
import requests
import pprint

CHECK_URL = "https://api.gandi.net/v5/domain/check"
TLD_URL = "https://api.gandi.net/v5/domain/tlds"
ERROR_TLD = ["af", "au", "africa", "basketball", "best", "cd", "doctor", "rugby", "sg"]

session = requests.Session()

def domain_lookup(name, upper):
    final = {}
    limit = float(upper)
    for i in tld_list:
        lookup = name + "." + i
        print("Looking at "+lookup)
        try:
            response = session.get(CHECK_URL, headers=headers, params={"name": lookup})
            response.raise_for_status()
            json = response.json()
            try:
               result = json['products'][0]['status']
            except:
                continue
            if result == 'available':
                try:
                    price = float(json['products'][0]['prices'][0]['normal_price_after_taxes'])
                except:
                    price = float(json['products'][0]['prices'][0]['price_after_taxes'])
                if price <= limit:
                    #print("{}: {:4.2f}".format(lookup, price))
                    final[lookup]=price

        except Exception as err:
            print(f"{name}.{i} Error occurred: {err}")

    if len(final) > 4:
        return final

    return final


try:
    apikey = os.environ["GANDI_API"]
except KeyError:
    print("Environment variable GANDI_API must be set.")
    sys.exit(1)

headers = {"authorization": "Apikey " + apikey}

try:
    response = session.get(TLD_URL, headers=headers)
    response.raise_for_status()
except Exception as err:
    print(f"Error occurred: {err}")

tld_list = []
for i in response.json():
    if "xn--" not in i['name'] and i['name'] not in ERROR_TLD:
        tld_list.append(i['name'])

#pprint.pprint(list(tld_list))

result = domain_lookup(sys.argv[1], sys.argv[2])
print(type(result))
pprint.pprint(result)


[print(key, value) for (key, value) in sorted(result.items(), key=lambda x: x[1])]
