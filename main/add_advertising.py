import pandas as pd
import random
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "Reviews_classified.xlsx")
output_path = os.path.join(script_dir, "Reviews_classified_with_synthetic.csv")

# Base templates for advertising reviews
templates = [
    "Buy the best {product} today! Huge discount available, limited time only!",
    "Free shipping on all {product}! Don’t miss out, shop now!",
    "Get 50% off on our new {product} – click here to order: {url}",
    "Amazing deals on {product}! Order before stock runs out!",
    "Sign up today and receive a free gift with every {product} purchase!",
    "Best {product} in town – order now and taste the difference!",
    "Huge clearance sale on {product}! Everything must go – shop online today!",
    "Limited edition {product} available now! Grab yours fast: {url}",
    "Exclusive offer: Buy one {product}, get one free – today only!",
    "New {product} collection launched! Don’t wait, click to get yours: {url}"
]

# Sample products, business names, authors
products = ["headphones", "laptops", "skincare products", "coffee beans", 
            "sneakers", "watches", "bags", "smartphones", "home appliances", "books"]

businesses = ["TechWorld", "BeautyHub", "CoffeeCorner", "SneakerStore", "SmartGadgets"]
authors = ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona"]

# Generate fake URLs
def fake_url():
    domains = ["example.com", "shopnow.com", "dealsonline.net", "buytoday.org"]
    return f"http://{random.choice(domains)}/{random.randint(100,999)}"

# Generate 50 synthetic advertising reviews
reviews = []
for _ in range(50):
    template = random.choice(templates)
    product = random.choice(products)
    url = fake_url()
    review_text = template.format(product=product, url=url)
    
    reviews.append({
        "business_name": random.choice(businesses),
        "author_name": random.choice(authors),
        "text": review_text,
        "photo": None,
        "rating": random.randint(1,5),
        "rating_category": "advertising",
        "Review_Classification": "advertising",
        "Review_Classification_reason": "promotional content"
    })

# Convert to DataFrame
synthetic_df = pd.DataFrame(reviews)

# Save to CSV
df = pd.read_excel(file_path)
df_combined = pd.concat([df, synthetic_df], ignore_index=True)
df_combined.to_csv(output_path, index=False)
print(f"Combined dataset saved to: {output_path}")