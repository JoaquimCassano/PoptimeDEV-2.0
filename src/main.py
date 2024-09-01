from ai import GeneratePosts
from bsky import GetTimeline, QuotePost, GetMentions, RePost
import threading, time, rich

def MainFlow():
  while True:
    posts = GeneratePosts(GetTimeline(limit=30))
    for post in posts['posts']:
      rich.print(f'[red bold]NEW POST[/red bold]: {post}')
      QuotePost(post)
      print('Posted')
      print('\n \n \n \n')

    time.sleep(1200)

def RetweetsFlow():
  while True:
    mentions = GetMentions()
    for mention in mentions:
      rich.print(f'[blue bold]NEW MENTION[/blue bold]: {mention.author.display_name}')
      RePost(mention.cid, mention.uri)
      print('Reposted')
      print('\n \n \n \n')

    time.sleep(1200)


if __name__ == '__main__':
  #t1 = threading.Thread(target=MainFlow)
  t2 = threading.Thread(target=RetweetsFlow)
  #t1.start()
  t2.start()