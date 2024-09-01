from openai import OpenAI
from pydantic import BaseModel
from atproto_client.models.app.bsky.feed.defs import FeedViewPost
import json


import dotenv, os

dotenv.load_dotenv()
key = os.getenv('OPENAI_API_KEY')

openai = OpenAI(api_key=key)

class Post(BaseModel):
  text: str
  medias: list[str]
  originalPostCID: str
  originalPostURI: str

class Response(BaseModel):
  posts: list[Post]

ResponseModelAsJson={
           'type': 'json_schema',
           'json_schema':
              {
                "name":"whocares",
                "schema": Response.model_json_schema()
              }
         }

systemPrompt = {
  "role": "system",
  "content": '''Imagine que você é a IA de um bot de uma rede social chamada Bluesky, que é parecida com o twitter, que noticia fofocas ou curiosidades sobre a "bolha dev" da rede social. Você receberá o feed do bot, e checará quais posts tem algo de interessante, e me retornará uma lista de quotes para serem feitos sobre esses posts.
  Os textos das notícias devem começar com "🚨 TRETA:", "🚨 CURIOSIDADE:" ou algo do tipo, como forma de chamar atenção. No caso, caso o post contenha provocações ou algo do tipo, use treta. caso contrário, curiosidade. Siga o modelo de JSON
  Retorne sempre pelo menos um post. Caso deseje colocar um URL, coloque inteiro, e nunca com reticências no meio.
  Nunca reescreva o mesmo conteúdo do post. Fale na terceira pessoa.
  Exemplo:
    Post original:
      Eu, Fulano, criei um projeto legal! Confira! https://linkdoprojeto.com
    Exemplo de post seu:
      Fulano criou um projeto bacana! Dê uma olhada! https://linkdoprojeto.com
  Lembre-se: É um exemplo, não poste isso
  '''
  }

def GeneratePosts(timeline:list[FeedViewPost]) -> list[Post]:
  cleanedTimeline = []
  for post in timeline:
    cleanedTimeline.append({
      "author": '@'+post.post.author.handle,
      "content": post.post.record.text,
      "medias": [], #TODO add medias support
      "postID": post.post.cid,
      "postURI": post.post.uri
    })

  completion = openai.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[systemPrompt, {
      "role": "user",
      "content":str(cleanedTimeline)
    }],
    response_format=ResponseModelAsJson
  )
  print(completion.choices[0].message.content)
  try:
    data = json.loads(completion.choices[0].message.content)
    return data
  except:
    print("WARNING! AI GENERATED INVALID JSON")
    return completion.choices[0].message.content

if __name__ == '__main__':
  from bsky import GetTimeline
  timeline = GetTimeline(limit=10)
  posts = GeneratePosts(timeline)
