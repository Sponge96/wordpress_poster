from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()


def get_video_data():
    url = input("Please Enter the Video URL: ")
    response = session.get(url)
    response.html.render(sleep=1)

    soup = BeautifulSoup(response.html.html, "html.parser")

    video_data = {}

    # URL
    video_data["url"] = url

    # Title
    video_data['title'] = soup.find("h1").text.strip()
    if video_data['title']:
        print(f"Title: {video_data['title']}")

    # Description
    video_data["description"] = soup.find("yt-formatted-string", {"class": "content"}).text
    if video_data['description']:
        print(f"Description: {video_data['description']}")

    return video_data


wp = Client('http://WEBSITE.com/xmlrpc.php', 'username', 'password')


def new_post(video_data):
    answer = input("Do you wish to publish?: ")
    if answer.lower() in ("y", "ci", "yes"):
        post = WordPressPost()
        post.title = video_data['title']
        post.content = video_data['url'] + f"<!-- wp:paragraph --><p>{video_data['description']}</p><!-- /wp:paragraph -->"
        post.terms_names = {
            'post_tag': ['video'],
            'category': ['Video Podcast'],
            'series': ['Sector Gaming']
        }
        post.post_status = 'publish'
        wp.call(NewPost(post))
        print("Your new post has been published and is now live!")
    else:
        return

new_post(get_video_data())
