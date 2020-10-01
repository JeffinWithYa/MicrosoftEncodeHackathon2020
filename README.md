# MicrosoftEncodeHackathon2020
# FUN-311 by Team BB

This sample demonstrates the use of FUN-311, a service that simplifies reporting of problematic city services and creates a feedback loop for citizen engagement

**Applies To**
Everyone with the spirit of learning, and anyone interested in creating a similar architecture using Microsoft Azure services. This project was made during the Microsoft Encode Hackathon, 2020.

## ScreenShots ##


## Console ## 
**This console identifies negative tweets using Azure Cognitive Services Sentiment Analysis and further categorizes them based on problem**
![image](https://github.com/JeffinWithYa/MicrosoftEncodeHackathon2020/blob/master/hackathonpics/web_console.png) 

## Heatmap ## 
**Alerts are sent to users who report an incident. The alert contains a link to a heatmap that centers on the location of the reported incident, and shows similar incidents in the area.**
![image](https://github.com/JeffinWithYa/MicrosoftEncodeHackathon2020/blob/master/hackathonpics/hackathonheatmap.png) 

## Azure Services ## 
**See below for an architecture diagram of the project, as well as a screenshot of our Azure console showing all services deployed on our $150 hackathon subscription.**

![image](https://github.com/JeffinWithYa/MicrosoftEncodeHackathon2020/blob/master/hackathonpics/arch_diagram.png)
![image](https://github.com/JeffinWithYa/MicrosoftEncodeHackathon2020/blob/master/hackathonpics/azure_console.png)

## How To Build ##

1. Clone the repo to your computer.
2. To install dependencies, navigate to the unzipped repo from the terminal and run 'pip3 install -r requirements.txt'
3. Start the Flask web app from the terminal by running 'python3 wsgi.py'
4. The project should display locally on your computer at http://0.0.0.0:5000/ 
6. The application will now accept queries about city service complaints from any municipality twitter account. Click the buttons on a card to engage with users. 

