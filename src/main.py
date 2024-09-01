from ai import GeneratePosts
from bsky import GetTimeline, QuotePost

if __name__ == '__main__':
  posts = GeneratePosts(GetTimeline(limit=5))
  print(type(posts))
  for post in posts['posts']:
    print(post)
    right = input("Post? y/n")
    if right.lower() == 'y':
      QuotePost(post)
      print('posted')