from requests_html import HTMLSession
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

def check_new_vid():
    session = HTMLSession()
    response = session.get("")
    response.html.render(sleep=1)

    title = response.html.xpath('//*[@id="video-title"]', first=True).text
    link = response.html.xpath('//*[@id="video-title"]/@href', first=True)
    compare_file(title, link)


def compare_file(title, link):
    with open("most_recent_vid", "r") as file:
        if file.read() == title:
            return
        else:
            get_vid_desc(title, link)


def get_vid_desc(title, link):
    url = "https://www.youtube.com" + link
    session = HTMLSession()
    response = session.get(url)
    response.html.render(sleep=1)

    desc = response.html.xpath('//*[@id="description"]/yt-formatted-string', first=True).text
    upload_post(title, url, desc)


def upload_post(title, url, desc):
    wp = Client('http://www.website.com/xmlrpc.php', 'username', 'password')

    post = WordPressPost()
    post.title = title
    post.content = url + f"<!-- wp:paragraph --><p>{desc}</p><!-- /wp:paragraph -->"
    post.terms_names = {
        'post_tag': [''],
        'category': [''],
        'series': ['']
    }
    post.post_status = 'publish'
    wp.call(NewPost(post))


check_new_vid()
