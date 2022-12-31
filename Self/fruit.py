import requests

url = "https://fruits-api.netlify.app/graphql"

body = """
{
fruit(id:14){
scientific_name
tree_name
}
}
"""

response = requests.post(url=url, json={"query": body})
print("response status code", response.status_code)
if response.status_code == 200:
    print("response:", response.content)