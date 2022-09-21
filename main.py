import csv
import sqlite3
import requests
import streamlit as st
from bs4 import BeautifulSoup
url = "https://www.theverge.com/"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')


class ScrapAndStoreData:
    def __init__(self):    #initialization
        self.title = []
        self.urls = []
        self.author = []
        self.date = []

    def get_data(self):      #scrapping required data from theverge.com

        for i in soup.find_all("a", class_="group-hover:shadow-highlight-blurple"):
            self.title.append(i.text)
            self.urls.append(f"www.theverge.com{ i.get('href')}")
            self.author.append(i.find_next("a", class_="text-franklin hover:shadow-underline-inherit mr-8").text)
            self.date.append(i.find_next("a", class_="text-franklin hover:shadow-underline-inherit mr-8").find_next("span").text)

        for i in soup.find_all("a", class_="text-white hover:text-franklin"):
            self.title.append(i.text)
            self.urls.append("www.theverge.com" + i.get('href'))
            self.author.append(i.find_next("span", class_="mr-8 text-gray-ef").text)
            self.date.append(i.find_next("span", class_="mr-8 font-light text-gray-ef").text)

        for i in soup.find_all("a", class_="text-black hover:text-algae"):
            self.title.append(i.text)
            self.urls.append("www.theverge.com" + i.get('href'))
            self.author.append(i.find_next("span", class_="mr-8 text-gray-13").text)
            self.date.append(i.find_next("span", class_="mr-8 font-light text-gray-13").text)

        for i in soup.find_all("a", class_="hover:shadow-underline-franklin"):
            self.title.append(i.text)
            self.urls.append(f"www.theverge.com{i.get('href')}")
            self.author.append(i.find_next("a", class_="text-franklin hover:shadow-underline-inherit mr-8").text)
            self.date.append(i.find_next("a", class_="text-franklin hover:shadow-underline-inherit mr-8").find_next("span").text)

        for i in soup.find_all("a", class_="group-hover:shadow-underline-franklin"):
            self.title.append(i.text)
            self.urls.append(f"www.theverge.com{i.get('href')}")
            self.author.append(i.find_next("a", class_="text-franklin hover:shadow-underline-inherit mr-8").text)
            self.date.append(i.find_next("a", class_="text-franklin hover:shadow-underline-inherit mr-8").find_next("span").text)

        for i in soup.find_all("h2", class_="mb-4 font-polysans text-20 font-medium tracking-1 leading-110"):
            self.title.append(i.text)
            self.urls.append("www.theverge.com" + i.find_next("a").get('href'))
            self.author.append(i.find_next("span", class_="mr-8 text-franklin").text)
            self.date.append(i.find_next("span", class_="mr-8 text-gray-e9").text)

    def csv_store(self):                                       #storing the data in a csv file
        header = ['Id', 'URL', 'Headline', 'Author', 'Date']
        data = []
        for Id, link, headline, author, date in zip(range(len(self.urls)), self.urls, self.title, self.author, self.date):
            data.append(Id)
            data.append(link)
            data.append(headline)
            data.append(author)
            data.append(date)
        rows = [data[i:i + 5] for i in range(0, len(data), 5)]
        with open('ddmmyyy_verge.csv', 'w', encoding='utf-8', newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(header)
            csvwriter.writerows(rows)

    def sqlite_store(self):                             #creating and storing the data in sqlite database
        connection = sqlite3.connect('the_verge.db')
        cursor = connection.cursor()
        create_table = '''CREATE TABLE the_Verge(
                        Id TEXT PRIMARY KEY,
                        URL TEXT NOT NULL,
                        Headline TEXT NOT NULL,
                        Author TEXT NOT NULL,
                        Date TEXT NOT NULL);
                        '''
        delete = "DROP TABLE IF EXISTS the_Verge"
        cursor.execute(delete)

        cursor.execute(create_table)
        file = open('ddmmyyy_verge.csv')
        contents = csv.reader(file)
        insert_records = "INSERT INTO the_Verge (Id, URL, Headline, Author, Date) VALUES(?, ?, ?, ?, ?)"
        cursor.executemany(insert_records, contents)
        select_all = "SELECT * FROM the_Verge"
        rows = cursor.execute(select_all).fetchall()

        for r1 in rows:     # Output to the console screen to check
            print(r1)

        st.table(rows)

        connection.commit()
        connection.close()


#st.write("Scrapped Data from The Verge:")
st.markdown("<h1 style='text-align: center; color: black;'>Scrapped Data From 'The Verge'</h1>", unsafe_allow_html=True)
p1 = ScrapAndStoreData()
p1.get_data()
p1.csv_store()
p1.sqlite_store()


