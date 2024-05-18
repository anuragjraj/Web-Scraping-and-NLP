# BLACK COFFER ASSIGNMENT

# Libraries

import pandas as pd
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from textstat import syllable_count



# Input Sheet with URL link of Articles given

input_sheet= r"C:\Users\Anu\Desktop\black_coffer\Input.xlsx"
df = pd.read_excel(input_sheet)



# Data from the Input
URL=df["URL"]
URL_ID=df["URL_ID"]



# Output Sheet given
output_sheet = r"C:\Users\Anu\Desktop\black_coffer\output.xlsx"
df_1 = pd.read_excel(output_sheet)







# Extracting the articles from all the links
# Textual Analysing the articles
# Computing different variables



# Scraping the data with the link
for i, (url, url_id) in enumerate(zip(URL, URL_ID)):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    if response.status_code == 200:
        title_text = soup.find('title').get_text() if soup.find('title') else ""
        content_text = ""
        article = soup.find('article')
        if article:
            for paragraph in article.find_all('p'):
                content_text += paragraph.get_text() + '\n'
        else:
            print("")

        content_text = '\n'.join(line.strip() for line in content_text.split('\n') if line.strip())
        text=content_text+ title_text








# Computing different variables
        
        sid = SentimentIntensityAnalyzer()
        words = word_tokenize(text)
        sentences = sent_tokenize(text)
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word.lower() not in stop_words]



        word_count = len(filtered_words)
        sentence_count = len(sentences)

        # Calculate Positive Score, Negative Score, Polarity Score, Subjectivity Score
        positive_score = 0
        negative_score = 0

        for word in words:
            scores = sid.polarity_scores(word)
            positive_score += scores['pos']
            negative_score += scores['neg']
            
        polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
        subjectivity_score = (positive_score + negative_score)/ ((word_count) + 0.000001)



        # Calculate Complex Word Count, Personal Pronouns 
        


        complex_word_count = 0
        personal_pronouns  = 0

        for word in filtered_words:
            if syllable_count(word) >= 3:
                complex_word_count += 1
            else:
                continue

        for word in filtered_words:
            if word in['US']:
                continue
            elif word.lower() in ['i', 'my', 'we', 'us', 'ours']:
                personal_pronouns  += 1

                


        # Average Sentence length, Average word length, Complex word percentage, Fog Index

        avg_sentence_length = word_count / sentence_count
        avg_word_length = sum(len(word) for word in filtered_words) / word_count
        complex_word_percentage = (complex_word_count / word_count) * 100
        fog_index = 0.4 * (avg_sentence_length + complex_word_percentage)

        

        # Compute syllable per word
        syllables_per_word = sum(syllable_count(word) for word in filtered_words) / word_count




        
        #Add value into the output colomns

        df_1.at[i,'POSITIVE SCORE']=positive_score
        df_1.at[i,'NEGATIVE SCORE']=negative_score
        df_1.at[i,'POLARITY SCORE']=polarity_score
        df_1.at[i,'SUBJECTIVITY SCORE']=subjectivity_score
        df_1.at[i,'AVG SENTENCE LENGTH']=avg_sentence_length
        df_1.at[i,'PERCENTAGE OF COMPLEX WORDS']=complex_word_percentage
        df_1.at[i,'FOG INDEX']=fog_index
        df_1.at[i,'AVG NUMBER OF WORDS PER SENTENCE']=avg_sentence_length
        df_1.at[i,'COMPLEX WORD COUNT']=complex_word_count
        df_1.at[i,'WORD COUNT']=word_count
        df_1.at[i,'SYLLABLE PER WORD']=syllables_per_word
        df_1.at[i,'PERSONAL PRONOUNS']=personal_pronouns
        df_1.at[i,'AVG WORD LENGTH']=avg_word_length


        
        # Save the text file in desired location

        with open(f'C:/Users/Anu/Desktop/Black_coffer/{url_id}.txt', 'w', encoding='utf-8') as file:
            file.write(title_text + '\n')
            file.write(content_text)
    else:
        continue


# Convert dataframe to excel file
df_1.to_excel('C:/Users/Anu/Desktop/Black_coffer/output_new.xlsx', index=False)