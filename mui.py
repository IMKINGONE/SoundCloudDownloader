import requests as requests
from requests.sessions import Session
import re
import m3u8


def track_authorization(url):
    global session
    session = requests.Session()
    global response
    response = session.get(url = url)
    regex=r'"track_authorization":".*?"'
    track_authorization = re.search(regex,response.text)
    edit = track_authorization.group(0)
    sl = edit.split('"')
    global result_authorization
    result_authorization = sl[3]
    
    


def client_id(url):
    regex = r'clientId":".*?"'
    client = re.search(regex,response.text)
    get = client.group(0)
    part = get.split('"')
    global result_client
    result_client = part[2]
    
    
    
    
def get_id(url):
    regex = r'"pageUrn":".*?"'
    get = re.search(regex,response.text)
    id = get.group(0)
    Edit_id = id.split(':')
    part = Edit_id[3]
    global remove
    remove = part.removesuffix('"')
    
def details(url):
    regex = rf"https://api-mobi.soundcloud.com/media/soundcloud:tracks:{remove}/.*?/"
    center = re.search(regex,response.text)
    need = center.group(0)
    Splitting = need.split('/')
    global save
    save = Splitting[5].strip()

def make_url():
    url = f"https://api-mobi.soundcloud.com/media/soundcloud:tracks:{remove}/{save}/stream/hls?client_id={result_client}&track_authorization={result_authorization}"
    while True:
        r = session.get(url = url)
        if r.json() == {}:
            pass
        else:
            answer = r.json()
            break
    
    global Link
    Link = answer['url']
    
    
    
    
    
def sendreq():
    global all_link
    all_link = []
    result_from_Link = session.get(url = Link)
    global get_links
    get_links = result_from_Link.text
    get_https = get_links.split('\n')
    for g in get_https:
        if g.startswith('https') == True:
            all_link.append(g)
        else:
            pass




    
def parsing():
    m3u8_pars = m3u8.loads(get_links)
    kos = m3u8_pars.data['segments']
    with open('p2le4ase.mp3','ab') as f:
       for k in kos:
          url = k['uri']
          response_url = session.get(url)
          f.write(response_url.content)
       print ('Finished')
        
    
    
    
    
 
    
if __name__ == '__main__':
    url = input('Link music: ')
    track_authorization(url)
    client_id(url)
    get_id(url)
    details(url)
    make_url()
    sendreq()
    parsing()

    
    
