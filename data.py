import csv
import random

# Define post types and biases
post_types = ['carousel', 'reels', 'static']
engagement_biases = {
    'carousel': {'likes': (150, 300), 'shares': (30, 70), 'comments': (20, 50)},
    'reels': {'likes': (400, 700), 'shares': (50, 100), 'comments': (60, 120)},
    'static': {'likes': (50, 150), 'shares': (10, 30), 'comments': (5, 20)},
}

# Generate data
data = []
data.append((1, 'carousel', random.randint(150, 300), random.randint(30, 70), random.randint(20, 50)))
data.append((3, 'static', random.randint(50, 150), random.randint(10, 30), random.randint(5, 20)))

# Add random posts
for post_id in range(4, 102):
    post_type = random.choice(post_types)
    likes = random.randint(*engagement_biases[post_type]['likes'])
    shares = random.randint(*engagement_biases[post_type]['shares'])
    comments = random.randint(*engagement_biases[post_type]['comments'])
    data.append((post_id, post_type, likes, shares, comments))

# Save to CSV
csv_file = "./social_media_engagement.csv"
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['post_id', 'post_type', 'likes', 'shares', 'comments'])
    writer.writerows(data)

csv_file
