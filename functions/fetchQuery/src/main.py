from appwrite.client import Client
from appwrite.services.databases import Databases

# Initialize the Appwrite client
client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1') \
    .set_project('661bf232a2d367eccb49') \
    .set_key('68a4559f483223bde0c57f0630be9b37191a1a809353da2538a1dcbc3da07039cdf6e9e09a62ae01baa5f026b241981f7cf95ea4be884a12cd95b23d22baae2cc25540fe12cb9655224b0d5c8b7d7022098e7afa558724718032854c413b0d25d08cd6c8615c61e611c6ad83b225f61e4a5bea40ef1b8b4573343bfea693d58a')

# Initialize the database client
database = Databases(client)

def main(context):
    if context.req.method == 'GET':
        try:
            path_parts = context.req.path.split('/')
            if len(path_parts) == 3 and path_parts[1] == 'documents':
                document_id = path_parts[2]
                result = database.get_document('661c0ff748205b5d00b5', '661c1000c15d1c28d50a', document_id)
                return context.res.json(result, 200, {'Access-Control-Allow-Origin': '*'})
            else:
                return context.res.json({'message': 'Invalid path'}, 400, {'Access-Control-Allow-Origin': '*'})
        except Exception as e:
            return context.res.json({'error': str(e)}, 500, {'Access-Control-Allow-Origin': '*'})
