from bs4 import BeautifulSoup as sp
from urllib.request import urlopen as Req

# Fetch the url
url = 'https://www.flipkart.com/search?q=laptop&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_0_1_na_na_pr&otracker1=AS_QueryStore_OrganicAutoSuggest_0_1_na_na_pr&as-pos=0&as-type=RECENT&suggestionId=laptop%7Cin+Laptops&requestId=1b3d9c1e-e5c3-4268-812d-26db8c5a1fb1&as-searchtext=l'

Client = Req(url)
page_html = Client.read()
Client.close()

page_soup = sp(page_html, "html.parser")

# Save all the contents in a variable
content = page_soup.findAll("div", {"class": "_KigyA"})
print(len(content))  # number of products in content

# print(sp.prettify(content[0]))  # to display html code of first product

# Create a csv file
filename = "Laptops.csv"
f = open(filename, "w")

headers = "Product_Name, Pricing, Discount(%), Savings, Ratings\n"
f.write(headers)

for container in content:
    # for product_name
    product_name = container.div.img["alt"]
    print("product_name: " + product_name)

    # for cost of products
    price_container = container.findAll("div", {"class": "_1vC4OE _1DTbR5"})
    price = price_container[0].text.strip()
    trim_price = ''.join(price.split(','))
    add_rs = trim_price.split('₹')
    rupees = "Rs " + add_rs[1]
    print("price: " + rupees)

    # for discount offered on each product
    discount_container = container.findAll("div", {"class": "VGWI6T _2YXy_Y"})
    discount = discount_container[0].text.strip()
    trim_discount = ' '.join(discount.split('% off'))
    percent = trim_discount.split(' ')
    final_discount = percent[0]
    print("Discount: " + final_discount)

    # Amount saved after buying this product
    saving = int(add_rs[1]) * int(final_discount)/(100-int(final_discount))
    saved = str(saving)
    savings = "Rs " + saved
    print("Savings: " + savings)

    # ratings out of 5
    rating_container = container.findAll("div", {"class": "hGSR34"})
    rating = rating_container[0].text
    split_rating = rating.split(' ')
    final_rating = split_rating[0] + "/5"
    print("rating: " + final_rating + "\n")

    print(product_name + ", " + rupees + ", " + final_discount + ", " + savings + ", " + final_rating + "\n")

    # push the values in the csv file created
    f.write(product_name.replace(",", "|") + ", " + rupees + ", " + final_discount + ", " + savings + ", " +
            final_rating + "\n")
f.close()

