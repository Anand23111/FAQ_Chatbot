import requests
from bs4 import BeautifulSoup
import csv

# Base URL for the forum
base_url = "https://community.jupiter.money"
# URL for the "Help" category under the forum
help_category_url = f"{base_url}/c/help/27"

# Function to get all tag links from the Help category page
def scrape_tags_from_help_category(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links that represent individual topics (tags) on the Help page
    tag_links = [link['href'] for link in soup.find_all('a', class_='raw-topic-link')]

    return tag_links

# Function to scrape detailed information from a single topic page
def scrape_topic_details(topic_url):
    topic_data = []
    
    # Construct full URL if the topic_url is relative
    if not topic_url.startswith("http"):
        topic_url = base_url + topic_url
    
    # Request the topic page content
    response = requests.get(topic_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the topic title (usually the question or main heading)
    title = soup.find('h1').get_text(strip=True)

    # Extract the detailed explanation (initial post content)
    detailed_explanation = soup.find('div', class_='post').get_text(strip=True)

    # Extract all tags/categories assigned to this topic
    tags = [tag.get_text(strip=True) for tag in soup.find_all('span', class_='badge-category-name')]

    # Extract the category name from breadcrumb navigation
    category = soup.find('span', class_='category-name').get_text(strip=True)

    # Initialize list to hold all replies to the topic
    replies = []
    # Find all reply posts in the topic thread
    posts = soup.find_all('div', class_='topic-body crawler-post')
    
    for post in posts:
        try:
            # Extract reply text content within each post
            reply = post.find('div', itemprop='text')
            if reply:
                replies.append(reply.get_text(strip=True))
            else:
                # If reply text is missing, append placeholder text
                replies.append("No reply text available")
        except AttributeError as e:
            # Handle unexpected HTML structure gracefully
            replies.append(f"Error parsing reply: {e}")
    
    # Check for pagination (i.e., if there are more pages of replies)
    next_page = soup.find('a', class_='next')
    if next_page:
        next_page_url = next_page['href']
        # Recursively scrape additional replies from subsequent pages
        additional_replies = scrape_topic_details(next_page_url)
        replies.extend(additional_replies)  # Append these replies to current list
    
    # Package the scraped data into a dictionary
    topic_data.append({
        "Topic Title": title,
        # "Detailed Explanation": detailed_explanation,  # Currently commented out
        "Replies": replies,
        "Tags": tags,
        "Category": category
    })
    
    return topic_data

# Function to scrape all topic URLs listed under a specific tag page
def scrape_topics_from_tag(tag_url):
    response = requests.get(tag_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract all topic links from the tag page
    topic_links = [link['href'] for link in soup.find_all('a', class_='raw-topic-link')]

    return topic_links

# Function to save the scraped data into a CSV file
def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        # Define CSV columns based on keys in the data dictionaries
        writer = csv.DictWriter(file, fieldnames=["Topic Title", "Replies", "Tags", "Category"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Main driver function to orchestrate the scraping process
def main():
    topic_data = []
    
    # Step 1: Get all tag URLs from the Help category
    tag_links = scrape_tags_from_help_category(help_category_url)
    
    # Step 2: For each tag, get all topics listed under it
    for tag_link in tag_links:
        topic_links = scrape_topics_from_tag(tag_link)
        
        # Step 3: For each topic, scrape its detailed data
        for topic_link in topic_links:
            topic_details = scrape_topic_details(topic_link)
            topic_data.extend(topic_details)  # Add topic details to main data list
    
    # Step 4: Save all scraped topic data into a CSV file
    save_to_csv(topic_data, "scraped_02.csv")

# Run the scraping process if this script is executed directly
if __name__ == "__main__":
    main()
