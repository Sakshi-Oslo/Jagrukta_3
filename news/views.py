from django.shortcuts import render

# Create your views here.
from unicodedata import name
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# import lxml
from bs4 import BeautifulSoup
import requests
from .forms import CustomUserCreationForm
# Create your views here.





def loginPage(request):
    page ='login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')


    return render(request, 'news/login_register.html',{'page': page})


def logoutUser(request):
    logout(request)
    return redirect('main')    

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect('home')

    context = {'form': form, 'page': page}
    return render(request,'news/login_register.html',context)








@login_required(login_url='login')
def homePage(request):
 r=requests.get("https://www.jagran.com/news/national-news-hindi.html?itm_medium=national&itm_source=dsktp&itm_campaign=navigation")
 soup=BeautifulSoup(r.content,'lxml')
 heading=soup.find_all('div',{'class':'h3'})
    
    
 heading=heading[22:32]
    

 News=[]
 for news in heading:
    News.append(news.text)

    

    if "state-name" in request.GET:
        
            state=request.GET.get('state-name')
            
            if state=="chhattisgarh" or "madhya-pradesh" or "rajasthan":
                 url=f"https://www.amarujala.com/{state}"
                 r0=requests.get(url)
                 soup = BeautifulSoup(r0.content,'html5lib')

                 News=[]
                 for h in soup.find_all('div',{'class':'image_description'}):
                    for x in h.find_all('a'):
                      News.append(x.get('title'))

                 News=News[0:10]

                 Image=[]
                 for main in soup.find_all('figure',{'class':'auw-lazy-load'}):
                   for by in main.find_all('img'):
                      Image.append("https:" + by.get('data-src'))


                 Image=Image[0:10]

            elif state=="Andhra-Pradesh" or "Karnataka" or "Kerala" or "Tamil-Nadu" or "Telangana":
                url2=f"https://www.thenewsminute.com/section/{state}"  
                r=requests.get(url2)
                soup10=BeautifulSoup(r.content, 'html5lib')
                
                News=[]
                for h in soup10.find_all('h3',{'class':'article-title'}):
                   News.append(h.getText())    
                
                News=News[4:14]


                Image=[]
                for i in soup10.find_all('img',{'class':'card-image'}):
                      Image.append(i.get('src'))

                Image=Image[0:10]  

            else:
                url4=f"https://www.jagran.com/state/{state}"   #formattable strings

                r1=requests.get(url4)
    
                soup1 = BeautifulSoup(r1.content, 'html5lib')

                heading1 = soup1.find_all('div',{'class':'h3'})
                image=soup1.find_all('img',{'class':'lazy'})


                heading1=heading1[22:32]
                image=image[20:30]
  
                News=[]
       

                for con in heading1:
                  News.append(con.text)
        
                Image=[]
                base_url="https:"
                for img in image:
                  Image.append(base_url+img.attrs['data-src'])

    

            url3="https://www.mohfw.gov.in/"
            r3=requests.get(url3)

            soup2 = BeautifulSoup(r3.content, 'html5lib')

            covid=[]

            for miter in soup2.find_all('span', {'class' : 'mob-show'}):
                  for byiter in miter.find_all('strong'):
                     covid.append(byiter.text)
        
            ACases=covid[0]
            DCases=covid[1]
            DeCases=covid[2]

       
            return render(request, 'news/index.html', {'ACases' : ACases, 'DCases' : DCases, 'DeCases':DeCases, 'state':state, 'Image':Image, 'News': News})


 return render(request, 'news/index.html', {'News': News})