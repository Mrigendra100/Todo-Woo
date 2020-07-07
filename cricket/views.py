from django.shortcuts import render , redirect
import requests
from cricket.models import CricApi
from cricket.forms import NameForm
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request , id ):
    url = 'https://cricapi.com/api/playerStats?apikey=ZLaCifWTz4V3bi5frVqjy4AKcGb2&pid={}'

    UniqueId = id

    r = requests.get(url.format(UniqueId)).json()
    # print(r)
    odi = r["data"]["batting"][ "ODIs"]
    odi_bw = r["data"]["bowling"]["ODIs"]
    

    player_info = {
        'name': r["name"],
        'born' : r["born"],
        'country' : r["country"],
        'photo' : r["imageURL"],
        '50': odi['50'],
        '100' : odi['100'],
        'highest' : odi['HS'],
        'runs' : odi['Runs'],
        'inns' : odi['Inns'],
        'match' : odi['Mat'],
        '5w' : odi_bw['5w'],
        '4w' : odi_bw['4w'],
        'econ' : odi_bw['Econ'],
        'wkts' : odi_bw['Wkts'],
        'bbm'  : odi_bw['BBM'],
    }

    context = {'player_info': player_info}
    
    return render(request, 'cricket/crichome.html', context )

@login_required
def player_search(request):
    
    if request.method == 'GET':
        return render(request, 'cricket/player_search.html', {'forms':NameForm()})

    elif request.method == 'POST' :
         
        # try:
            
            data = request.POST.copy()
            
            url ='https://cricapi.com/api/playerFinder?apikey=ZLaCifWTz4V3bi5frVqjy4AKcGb2&name={}'

            
            print(data.get('player_name'))
            
               
           
            name = data.get('player_name')
            player = requests.get(url.format(name)).json()
            data = player['data']
            
            try:
                id =data[0]['pid']
                
                # print(id)
                # print(type(id) is int)
            

                return redirect('cricket:index', id) 

            except IndexError:
                return render(request, 'cricket/player_search.html', {'forms':NameForm() , 'error': 'No Such Player in our Database , Please Try Again'})

        

    




