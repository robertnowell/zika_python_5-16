import pip
!pip install tweepy
import tweepy
import pandas as pd
import matplotlib.pyplot as plt

consumer_key = "" # Use your own key. To get a key https://apps.twitter.com/
consumer_secret = ""

#pass to o auth handler
auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)

#authentication to API object
api = tweepy.API(auth)


#The max_id = top of tweets id list . since_id = bottom of tweets id list .

results = []
for tweet in tweepy.Cursor(api.search, q="Zika").items(1500):
    results.append(tweet)

#define a function to generate a data frame with the info we want from
    #the results of the first "Zika" query
def process_results(results):
    #first create the index, essentially, being tweet id numbers
    id_list = [tweet.id for tweet in results]
    data_set = pd.DataFrame(id_list, columns=["id"])

    # Processing Tweet Data
    data_set["text"] = [tweet.text for tweet in results]
    data_set["created_at"] = [tweet.created_at for tweet in results]
    data_set["source"] = [tweet.source for tweet in results]
    data_set["tweet_language"] = [tweet.lang for tweet in results]
    
    # Processing User Data
    data_set["user_screen_name"] = [tweet.author.screen_name for tweet in results]
    data_set["user_name"] = [tweet.author.name for tweet in results]
    data_set["user_created_at"] = [tweet.author.created_at for tweet in results]
    data_set["user_description"] = [tweet.author.description for tweet in results]
    data_set["user_location"] = [tweet.author.location for tweet in results]
    data_set["time_zone"] = [tweet.author.time_zone for tweet in results]
    return data_set

#use process_results to store the results of the first query in a data frame
data_set = process_results(results)


#Now for the loop that will return up to 1500 tweets for each of the four most
    #common languages of tweets in the general "Zika" query

#First, create a list of the four most common languages used
languages_series = data_set["tweet_language"].value_counts()[:4][::-1]
languages_list = languages_series.index.values 

#Next, perform queries for "Zika" tweets in those four languages.
for language in languages_list:
    if (language != "und"):
        for tweet in tweepy.Cursor(api.search, q="Zika", lang = language).items(1500):
            results.append(tweet)

#use process_results to generate a data frame from the four queries.
data_set_2 = process_results(results)
pd.DataFrame.drop_duplicates(data_set_2, inplace = True)

#now that we have our results in a data frame, we want to analyze the data
#PLOTS

# colors for all plots
colors =  ['seagreen', 'royalblue', 'mediumpurple', 'sage', 'skyblue', 'blueviolet', 'slateblue', 'lightgreen', 'cornflowerblue', 'palevioletred', 'mediumpurple', 'darkorchid']




#language analysis first
#language data is in the wrong format (ISO 639-1), so let's change that
#create data frame of ISO 639-1 codes
#source: http://data.okfn.org/data/core/language-codes
lang_codes = pd.read_csv("C:\\Users\\Robert\\Documents\\Google Drive\\Spring 2016\\CU Denver\\BIOS 6640\\language-codes.csv")
lang_codes.set_index("alpha2", inplace = True) 
lang_codes = lang_codes.T
lang_codes["und"] = "undefined"
lang_codes["in"] = "in"




#####1######
#create list of top languages in ascending order, for each general dataget
#GENERAL DATASET 1 CORRUPTED

#TOP LANGUAGES FOR GENERAL DATAGET 2
top_languages_2 = general_data_set_2["tweet_language"].value_counts()[:5][::-1]
top_languages_list_2_unicode = top_languages_2.index.values
top_languages_list_2 = []
for data in top_languages_list_2_unicode:
    A = data.encode('utf-8')
    top_languages_list_2.append(A)

#rename languages based on ISO 639-1 code data frame created above
for i in range(0, len(top_languages_list_2)):    
    top_languages_2.index.values[i] = lang_codes[top_languages_list_2[i]][0]    


#TOP LANGUAGES FOR GENERAL DATASET 4
top_languages_4 = general_data_set_4["tweet_language"].value_counts()[:5][::-1]
top_languages_list_4_unicode = top_languages_4.index.values
top_languages_list_4 = []
for data in top_languages_list_4_unicode:
    A = data.encode('utf-8')
    top_languages_list_4.append(A)

#rename languages based on ISO 639-1 code data frame created above
for i in range(0, len(top_languages_list_4)):    
    top_languages_4.index.values[i] = lang_codes[top_languages_list_4[i]][0]    

#TOP LANGUAGES FOR DATASETS COMBINED

general_data_set_total = pd.concat([general_data_set_2,general_data_set_4])
top_languages_total = general_data_set_total["tweet_language"].value_counts()[:5][::-1]
top_languages_total_list_unicode = top_languages_total.index.values
top_languages_list_total = []
for data in top_languages_total_list_unicode:
    A = data.encode('utf-8')
    top_languages_list_total.append(A)

#rename languages based on ISO 639-1 code data frame created above
for i in range(0, len(top_languages_list_total)):    
    top_languages_total.index.values[i] = lang_codes[top_languages_list_total[i]][0]    

#PLOT OF THE TOP LANGUAGES AT 12pm, 12AM MDT ON 5/9/16 AND COMBINED TOTALS

labels2 = top_languages_2.index.values
labels4 = top_languages_4.index.values

fig = plt.figure()
ax = fig.gca()

ax.pie(general_data_set_4["tweet_language"].value_counts()[:5][::-1],
       labels=labels4, colors=colors,
       autopct='%1.1f%%', shadow=True,
       radius=2.5, center=(5.75, 8.25), frame=True)
       
ax.pie(general_data_set_2["tweet_language"].value_counts()[:5][::-1], 
       labels=labels2, colors=colors, autopct='%1.1f%%', shadow=True,
       radius=2.5, center=(1.5, 2.25))

ax.pie(general_data_set_total["tweet_language"].value_counts()[:5][::-1],
        labels = top_languages_total.index.values, autopct = '%1.1f%%',
        colors = colors, shadow=True, radius = 2.5, center = (5.75, -4.25))
title("Top tweet languages 5/9/16")

ax.set_xlim((0, 10))
ax.set_ylim((0, 13))

plt.show()












#######2######
#PLOT OF THE TOP 8 TIME ZONES AT 12pm AND 12AM MDT ON 5/9/16


eight_time_zones_2 = general_data_set_2["time_zone"].value_counts()[:8][::-1]
eight_time_zones_2_unicode = eight_time_zones_2.index.values
#cleaned up time zone data in tz_data_2

eight_time_zones_4 = general_data_set_4["time_zone"].value_counts()[:8][::-1]
eight_time_zones_4_unicode = eight_time_zones_4.index.values
#cleaned up time zone data in tz_data_4

eight_time_zones_total = general_data_set_total["time_zone"].value_counts()[:8][::-1]
eight_time_zones_total_unicode = eight_time_zones_total.index.values
#cleaned up time zone data in tz_data_t

fig = plt.figure()
ax = fig.gca()

patches, texts = ax.pie(general_data_set_4["time_zone"].value_counts()[:8][::-1],
                        labels= tz_data_4, labeldistance = 1.45, colors=colors, shadow=True,
                        radius=3.5, center=(.5, 2.25))
for t in texts:
    t.set_horizontalalignment('center')

ax.pie(general_data_set_2["time_zone"].value_counts()[:8][::-1], 
       labels= tz_data_2, labeldistance = 1.2, 
       colors=colors, shadow=True, radius=3.5, center=(7.75, 13.25))

ax.pie(general_data_set_total["time_zone"].value_counts()[:8][::-1],
       labels = tz_data_t, colors = colors,
       labeldistance = 1.2, shadow=True, radius = 3.5, center=(7.75, -8.75))
title("Top tweet time zones 5/9/16")

ax.set_xlim((0, 12))
ax.set_ylim((0, 21))

plt.show()














########3#########################
#PIE CHARTS FOR TOP TIME ZONES OF TOP THREE LANGUAGES AT EACH TIME POINT (1-4)
#== twelve total pie charts
#FIRST, SPLIT FOUR DATAFRAMES BY TOP THREE LANGUAGES 



pie_data_set_3 = plt.pie(data_set_4["time_zone"].value_counts()[:12][::-1], 
                         labels = twelve_time_zones.index.values)


pie_general_data_set_4 = plt.pie(general_data_set_4["time_zone"].value_counts()[:8][::-1], 
                                 labels = eight_time_zones.index.values, 
                                 autopct='%1.f%%', colors=colors)




#FIND TOP LANGUAGES IN DATA SETS
languages_series_1 = data_set_1["tweet_language"].value_counts()[:3][::-1]
languages_series_1

languages_series_2 = data_set_2["tweet_language"].value_counts()[:3][::-1]
languages_series_2

languages_series_3 = data_set_3["tweet_language"].value_counts()[:3][::-1]
languages_series_3

languages_series_4 = data_set_4["tweet_language"].value_counts()[:3][::-1]
languages_series_4

#all are es, en, and pt as top three (in differing orders)


#make three pie charts, one for each language
#with four subplots, one for each data get throughout the day
#so each pie chart will have 0600 1200 1800 and 2359 for 5/9/16

#SPANISH FIRST

fig = plt.figure()
ax = fig.gca()

data_set_1_es = data_set_1.loc[data_set_1['tweet_language'] == "es"]
#spanish time zone pie chart, data set 1
data_set_1_es_zones = data_set_1_es["time_zone"].value_counts()[:8][::-1]
ds1_es_tz_u = data_set_1_es_zones.index.values

ax.pie(data_set_1_es["time_zone"].value_counts()[:8][::-1], 
       labels= ds1_es_tz, colors=colors, center=(3, 5.75))


data_set_2_es = data_set_2.loc[data_set_2['tweet_language'] == "es"]
#spanish time zone pie chart, data set 2
data_set_2_es_zones = data_set_2_es["time_zone"].value_counts()[:8][::-1]
ds2_es_tz_u = data_set_2_es_zones.index.values

ax.pie(data_set_2_es["time_zone"].value_counts()[:8][::-1], 
       labels= ds2_es_tz, colors=colors,
       center=(5.75, 5.75))

data_set_3_es = data_set_3.loc[data_set_3['tweet_language'] == "es"]
#spanish time zone pie chart, data set 3
data_set_3_es_zones = data_set_3_es["time_zone"].value_counts()[:8][::-1]
ds3_es_tz_u = data_set_3_es_zones.index.values

ax.pie(data_set_3_es["time_zone"].value_counts()[:8][::-1], 
       labels= ds3_es_tz, colors=colors,
       center=(3, 3))

data_set_4_es = data_set_4.loc[data_set_4['tweet_language'] == "es"]
#spanish time zone pie chart, data set 4
data_set_4_es_zones = data_set_4_es["time_zone"].value_counts()[:8][::-1]
ds4_es_tz_u = data_set_4_es_zones.index.values

ax.pie(data_set_4_es["time_zone"].value_counts()[:8][::-1], 
       labels= ds4_es_tz, colors=colors,
       center=(5.75, 3))


#pie chart of top spanish time zones, sum of four datasets
data_set_total_es = pd.concat([data_set_1_es, data_set_2_es, 
                              data_set_3_es, data_set_4_es])
data_set_total_es_zones = data_set_total_es["time_zone"].value_counts()[:8][::-1]
dst_es_tz_u = data_set_total_es_zones.index.values

ax.pie(data_set_total_es["time_zone"].value_counts()[:8][::-1], 
       labels= dst_es_tz, colors=colors, center=(4.375, .25))


plt.show()



#NEXT, ENGLISH


fig = plt.figure()
ax = fig.gca()

data_set_1_en = data_set_1.loc[data_set_1['tweet_language'] == "en"]
#english time zone pie chart, dataset 1
data_set_1_en_zones = data_set_1_en["time_zone"].value_counts()[:8][::-1]
ds1_en_tz_u = data_set_1_en_zones.index.values

ax.pie(data_set_1_en["time_zone"].value_counts()[:8][::-1], 
       labels= ds1_en_tz_u, colors=colors, center=(3, 5.75))
       
       
data_set_2_en = data_set_2.loc[data_set_2['tweet_language'] == "en"]
#english time zone pie chart, dataset 2
data_set_2_en_zones = data_set_2_en["time_zone"].value_counts()[:8][::-1]
ds2_en_tz_u = data_set_2_en_zones.index.values

ax.pie(data_set_2_en["time_zone"].value_counts()[:8][::-1], 
       labels= ds2_en_tz, colors=colors,center=(5.75, 5.75))

       
data_set_3_en = data_set_3.loc[data_set_3['tweet_language'] == "en"]
#english time zone pie chart, dataset 3
data_set_3_en_zones = data_set_3_en["time_zone"].value_counts()[:8][::-1]
ds3_en_tz_u = data_set_3_en_zones.index.values

ax.pie(data_set_3_en["time_zone"].value_counts()[:8][::-1], 
       labels= ds3_en_tz, colors=colors, center=(3, 3))

            
data_set_4_en = data_set_4.loc[data_set_4['tweet_language'] == "en"]
#english time zone pie chart, dataset 4
data_set_4_en_zones = data_set_4_en["time_zone"].value_counts()[:8][::-1]
ds4_en_tz_u = data_set_4_en_zones.index.values

ax.pie(data_set_4_en["time_zone"].value_counts()[:8][::-1], 
       labels= ds4_en_tz, colors=colors, center=(5.75, 3))


#pie chart of top english time zones, sum of four datasets
data_set_total_en = pd.concat([data_set_1_en, data_set_2_en, 
                              data_set_3_en, data_set_4_en])
data_set_total_en_zones = data_set_total_en["time_zone"].value_counts()[:8][::-1]
dst_en_tz_u = data_set_total_en_zones.index.values

ax.pie(data_set_total_en["time_zone"].value_counts()[:8][::-1], 
       labels= dst_en_tz, colors=colors, center=(4.375, .25))

plt.show()


#LAST, PORTUGUESE
fig = plt.figure()
ax = fig.gca()
data_set_1_pt = data_set_1.loc[data_set_1['tweet_language'] == "pt"]
#portuguese time zone pie chart, dataset 1
data_set_1_pt_zones = data_set_1_pt["time_zone"].value_counts()[:8][::-1]
ds1_pt_tz_u = data_set_1_pt_zones.index.values

ax.pie(data_set_1_pt["time_zone"].value_counts()[:8][::-1], 
       labels= ds1_pt_tz, colors=colors, center=(3, 5.75))


data_set_2_pt = data_set_2.loc[data_set_2['tweet_language'] == "pt"]
#portuguese time zone pie chart, dataset 2
data_set_2_pt_zones = data_set_2_pt["time_zone"].value_counts()[:8][::-1]
ds2_pt_tz_u = data_set_2_pt_zones.index.values

ax.pie(data_set_2_pt["time_zone"].value_counts()[:8][::-1], 
       labels= ds2_pt_tz, colors=colors, center=(5.75, 5.75))
       
       
data_set_3_pt = data_set_3.loc[data_set_3['tweet_language'] == "pt"]
#portuguese time zone pie chart, dataset 3
data_set_3_pt_zones = data_set_3_pt["time_zone"].value_counts()[:8][::-1]
ds3_pt_tz_u = data_set_3_pt_zones.index.values
time_zone_replace(ds3_pt_tz)

ax.pie(data_set_3_pt["time_zone"].value_counts()[:8][::-1], 
       labels= ds3_pt_tz, colors=colors, center=(3, 3))

data_set_4_pt = data_set_4.loc[data_set_4['tweet_language'] == "pt"]
#portuguese time zone pie chart, dataset 4
data_set_4_pt_zones = data_set_4_pt["time_zone"].value_counts()[:8][::-1]
ds4_pt_tz_u = data_set_4_pt_zones.index.values

ax.pie(data_set_4_pt["time_zone"].value_counts()[:8][::-1], 
       labels= ds4_pt_tz, colors=colors, center=(5.75, 3))
       
       
#pie chart of top portuguese time zones, sum of four datasets
data_set_total_pt = pd.concat([data_set_1_pt, data_set_2_pt, 
                              data_set_3_pt, data_set_4_pt])
data_set_total_pt_zones = data_set_total_pt["time_zone"].value_counts()[:8][::-1]
dst_pt_tz_u = data_set_total_pt_zones.index.values

ax.pie(data_set_total_pt["time_zone"].value_counts()[:8][::-1], 
       labels= dst_pt_tz, colors=colors, center=(4.375, .25))

plt.show()


#LAST ARE TWO THINGS:

#Weighted pt, en, es plot
fig = plt.figure()
ax = fig.gca()

ax.pie(data_set_total_pt["time_zone"].value_counts()[:8][::-1], 
       labels= dst_pt_tz, colors=colors, center=(7.375, .25),
        radius = 2/4.91)


ax.pie(data_set_total_en["time_zone"].value_counts()[:8][::-1], 
       labels= dst_en_tz, colors=colors, center=(4.375, .25), 
        radius = 2)

ax.pie(data_set_total_es["time_zone"].value_counts()[:8][::-1], 
       labels= dst_es_tz, colors=colors, center=(1.375, .25), 
        radius = 2/2.06)

plt.show()


#Korean/russian plot
fig = plt.figure()
ax = fig.gca()

ax.pie(data_set_ru["time_zone"].value_counts()[:8][::-1], 
       labels= dst_ru_tz, colors=colors, center=(4.375, .25))

ax.pie(data_set_ru["time_zone"].value_counts()[:8][::-1], 
       labels= dst_ru_tz, colors=colors, center=(4.375, .25))

plt.show()



###TIME ZONE VALUE CLEANUP
#this function was applied to each of the twelve unicode strings
#of top time zones, one for each dataset.
def time_zone_replace(x):
#this function takes a unicode string, so first convert to plain strings
#x should be a unicode string list of time zones.
    x_temp = []
    for data in x:
        A = data.encode('utf-8')
        x_temp.append(A)
    x = x_temp
#now, cleanup
    for i in range(0, len(x)):
        if (x[i] == "Caracas"):
            x[i] = "Venezuela"
        if (x[i] == "Madrid"):
            x[i] = "Spain"
        if (x[i] == "Mexico City"):
            x[i] = "Central Time (Mexico)"
        if (x[i] == "Bogota"):
            x[i] = "Colombia"
        if (x[i] == "Santiago"):
            x[i] = "Chile"
        if (x[i] == "Quito"):
            x[i] = "Ecuador"
        if (x[i] == "Paris"):
            x[i] = "France"
        if (x[i] == "London"):
            x[i] = "Britain"
        if (x[i] == "New Delhi"):
            x[i] = "India"
        if (x[i] == "Buenos Aires"):
            x[i] = "Argentina"
        if (x[i] == "Kabul"):
            x[i] = "Afghanistan"
        if (x[i] == "Pacific Time (US & Canada)"):
            x[i] = "Pacific (US/CA)"
        if (x[i] == "Atlantic Time (Canada)"):
            x[i] = "Atlantic (CA)"
        if (x[i] == "Central Time (US & Canada)"):
            x[i] = "Central (US/CA)"
        if (x[i] == "Mountain Time (US & Canada)"):
            x[i] = "Mountain (US/CA)"
        if (x[i] == "Eastern Time (US & Canada)"):
            x[i] = "Eastern (US/CA)"
    global  ##name of output variable here   
    ##assign (name of output variable) the value of x



#pickling:
data_set_2.to_pickle('tweet_get_two_59.pkl')
data_set_2_prime = pd.read_pickle('tweet_get_two_59.pkl')














