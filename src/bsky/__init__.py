import dotenv, os
from atproto import Client, models
from ai import Post
from datetime import datetime

dotenv.load_dotenv()
user = os.getenv('BSKY_USER') ; passwd = os.getenv('BSKY_PASS')
repostedCIDs = []

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

def GetMentions() -> list[models.AppBskyNotificationListNotifications.Notification]:
  mentions = []
  Unreadnotifications = client.app.bsky.notification.get_unread_count()
  if Unreadnotifications.count > 0:
    allNotifications = client.app.bsky.notification.list_notifications(params={'limit':Unreadnotifications.count})
    for notification in allNotifications.notifications:
      if notification.reason == 'mention' and notification.is_read == False:
        mentions.append(notification)

    client.app.bsky.notification.update_seen(data={'seen_at':client.get_current_time_iso()})
    return mentions
  return []

def RePost(cid:str, uri:str):
  if cid in repostedCIDs:
    return
  repostedCIDs.append(cid)
  client.repost(uri=uri, cid=cid)
  return