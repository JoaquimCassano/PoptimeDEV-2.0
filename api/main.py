from .ai import GeneratePosts
from .bsky import GetTimeline, QuotePost, GetMentions, RePost
import threading, time, rich
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
  return 'Hello World!'



def MainFlow():
  print('Started mainflow.')
  while True:
    print('Running mainflow.')
    posts = GeneratePosts(GetTimeline(limit=30))
    for post in posts['posts']:
      rich.print(f'[red bold]NEW POST[/red bold]: {post}')
      QuotePost(post)
      print('Posted')
      print('\n \n \n \n')

    time.sleep(3000)

def RetweetsFlow():
  print('Started retweetsflow.')
  while True:
    print('Running retweetsflow.')
    mentions = GetMentions()
    for mention in mentions:
      rich.print(f'[blue bold]NEW MENTION[/blue bold]: {mention.author.display_name}')
      RePost(mention.cid, mention.uri)
      print('Reposted')
      print('\n \n \n \n')

    time.sleep(180)


if __name__ == '__main__':
  t1 = threading.Thread(target=MainFlow)
  t2 = threading.Thread(target=RetweetsFlow)
  t1.start()
  t2.start()
  app.run()