
from crowdstrike import CrowdStrikeAPI, Token
from config import CLIENT_ID, CLIENT_SECRET


token_store = Token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

api_object = CrowdStrikeAPI(token=token_store)

token_store.get_token(force_get=True)

print(api_object.get_event_streams(appid='test123'))