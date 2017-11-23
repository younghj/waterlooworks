from bs4 import BeautifulSoup
import os
import pandas as pd
import re

ld = [ x for x in os.listdir('.') if x.endswith('html') and 'Waterloo' in x]
dfs = []

for page in ld:
    # page = ld[0]
    print page

    data = []
    with open(page) as f:
        s = f.read()

    soup = BeautifulSoup(s, 'html.parser')
    table = soup.find('table', attrs={'id':'postingsTable'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele.replace('\n','').replace('\t','').replace('NEW','').encode('ascii', 'ignore').decode('ascii') for ele in cols if ele]) # Get rid of empty values

    df = pd.DataFrame(data)
    df.drop(df.columns[[0, 1, 4, 5, 6, 8, 9, 10]], axis=1, inplace=True)

    dfs.append(df)

final = pd.concat(dfs).reset_index(drop=True)

companies = sorted(final[3].unique())
with open('out.txt','w') as f:
    for company in companies:
        f.write('{}\n'.format(company))

# html = final.to_html()
# csv = final.to_csv()

# with open('out.html', 'w') as f:
    # f.write(html)
# with open('out.csv', 'w') as f:
    # f.write(csv)
