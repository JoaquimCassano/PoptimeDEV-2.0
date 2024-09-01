import dotenv, os
from atproto import Client, models
from ai import Post


dotenv.load_dotenv()
user = os.getenv('BSKY_USER') ; passwd = os.getenv('BSKY_PASS')
print(user, passwd)


client = Client(base_url='https://bsky.social')
client.login(user, passwd)

class recreatedModel:
    def __init__(self, cid:str, uri:str) -> None:
      self.cid = cid
      self.uri = uri

def GetTimeline(limit:int=50):
  return client.get_timeline(limit=limit).feed

""" if __name__ == '__main__':
  feed = GetTimeline(10)
  for post in feed:
    print(post.post.author.display_name)
    print(post.post.record.text)
    if post.post.record.embed:
      for image in post.post.record.embed.images:
        print(image.image)
         """

def QuotePost(post:Post):
  postModel = recreatedModel(post['originalPostCID'], post['originalPostURI'])
  parent = models.create_strong_ref(postModel)
  quoted_post = models.AppBskyEmbedRecord.Main(record=parent)
  post = client.send_post(
    text=post['text'],
    embed=quoted_post
  )
  return post

